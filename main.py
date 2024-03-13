import os
from dotenv import load_dotenv
from mail_gen import EmailGenFromGemini 
from google.cloud import storage
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Request, Form
app = FastAPI()

# Define folder paths
product_description_folder = "uploads/product_description/"
target_company_folder = "uploads/target/target_company/"
target_person_folder = "uploads/target/target_person/"

# Ensure upload folders exist
os.makedirs(product_description_folder, exist_ok=True)
os.makedirs(target_company_folder, exist_ok=True)
os.makedirs(target_person_folder, exist_ok=True)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Defining the variables for google-cloud
key_path = "/workspace/LLM-Emails/gcp_service_account.json"
project_id = "ck-eams"
bucket_name = "email_gen_llm"
upload_company_folder = "Company_Data/"
upload_person_folder = "Person_Data/"
storage_Client = storage.Client.from_service_account_json(key_path)



# Checking if the service account is correctly authenticated or not
def authenticate() -> bool:
    try:
        temp_project_id = storage_Client.project
        return temp_project_id == project_id
    except Exception(e):
        print(f"Exception:\n{e}")
        return False



# change_file_name
def change_file_name(filepath : str = None) -> str:
    original_file_path = filepath
    file_list = filepath.split('/')
    file_list[-1] = file_list[-1].replace(" ","_")
    result_path = ""
    for string in file_list:
        result_path += string
        result_path += "/"
    result_path = result_path[0:-1]
    os.rename(original_file_path,result_path)
    return result_path



# Function to check if upload file exists in cloud bucket or not:
def check_exists(folder_name : str = None, file_path : str = None) -> bool:
    file_name = file_path.split('/')[-1]
    bucket = storage_Client.get_bucket("email_gen_llm")
    blobs = bucket.list_blobs(prefix = folder_name)
    blob = any(blob.name == f"{folder_name}{file_name}" for blob in blobs)
    if blob:
        return True
    return False
    


# Upload file to the bucket:
def upload_file(folder_name : str = None, file_path : str = None):
    file_name = file_path.split('/')[-1]
    bucket = storage_Client.get_bucket("email_gen_llm")
    blob = bucket.blob(f"{folder_name}{file_name}")
    blob.upload_from_filename(file_path)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request, message: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": message})


@app.post("/")
async def upload_files(request: Request,
                       productDescription: UploadFile = File(...),
                       targetCompany: UploadFile = File(...),
                       targetPerson: UploadFile = File(...),
                       tone: str = Form(...)):

    product_path = os.path.join(product_description_folder, productDescription.filename)
    target_company_path = os.path.join(target_company_folder, targetCompany.filename)
    target_person_path = os.path.join(target_person_folder, targetPerson.filename)

    # List of filepaths and fileobjects
    path_list = [product_path, target_company_path, target_person_path]
    object_list = [productDescription, targetCompany, targetPerson]

    # Storing the uploaded files in their respective folders.
    for i in range(3):
        with open(path_list[i], "wb") as buffer:
            buffer.write(await object_list[i].read())

    # Authenticating for gcp bucket
    if authenticate():
        # Uploading the target and source company's description
        for i in range(2):
            path_list[i] = change_file_name(path_list[i])
            if not check_exists(upload_company_folder, path_list[i]):
                print(f"{path_list[i]} doesn't exist.")
                upload_file(upload_company_folder, path_list[i])
            else:
                print(f"{path_list[i]} already exists")

        # Uploading the target person's description
        path_list[2] = change_file_name(path_list[2])
        if not check_exists(upload_person_folder, target_company_path):
            folder_name = target_company_path.split('/')[-1].split('.')[0]
            bucket = storage_Client.get_bucket(bucket_name)
            blob = bucket.blob(f"{upload_person_folder}{folder_name}/")
            blob.upload_from_string('')
            upload_file(f"{upload_person_folder}{folder_name}/", target_person_path)

        # Generating the mail
        mail_gen_instance = EmailGenFromGemini(model_name = 'gemini-pro',
                    source_path = product_path,
                    target_company_path = target_company_path,
                    target_person_path = target_person_path)
        mail = mail_gen_instance.email_generation()
        # print(mail)
        
        html_response = f"<!DOCTYPE html>\
        <html>\
        <head>\
        <style>\
        body \
        {{font-family: Arial, sans-serif;line-height: 1.6;}}\
        </style>\
        </head>\
        <body>\
        <h3>Generated Email</h3>\
        <div>\
        {mail['email']}\
        </div>\
        </body>\
        </html>"
        
        print(mail['timestamp'])
        return templates.TemplateResponse("index.html", {"request": request, "message":  "Files uploaded successfully", "text":mail['email']})

    return templates.TemplateResponse("index.html", {"request": request, "message": "Error occurred!", "text": "Email is not generated."})