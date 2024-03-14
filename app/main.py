import os
from dotenv import load_dotenv
from mail_gen import EmailGenFromGemini 
from google.cloud import storage
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Request, Form
app = FastAPI()

# List of folder paths
folder_path_list = [
    "/workspace/LLM-Emails/app/uploads/product_description/",
    "/workspace/LLM-Emails/app/uploads/target/target_company/",
    "/workspace/LLM-Emails/app/uploads/target/target_person/" 
]
file_path_list = []                                                             # list of file paths

# Ensure upload folders are created
for i in range(3):
    os.makedirs(folder_path_list[i], exist_ok = True)

# Initialize templates
templates = Jinja2Templates(directory="/workspace/LLM-Emails/app/templates")

# Defining the variables for google-cloud
key_path = "/workspace/LLM-Emails/Secrets/gcp_service_account.json"
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
    file_objects_list = [productDescription, targetCompany, targetPerson]                       # list of file objects
    
    for i in range(3):  
        file_path_list.append(os.path.join(folder_path_list[i], file_objects_list[i].filename))
    
    # Storing the uploaded files in their respective folders.
    for i in range(3):
        with open(file_path_list[i], "wb") as buffer:
            buffer.write(await file_objects_list[i].read())

    # Authenticating for gcp bucket
    if authenticate():
        # Uploading the target and source company's description
        for i in range(2):
            file_path_list[i] = change_file_name(file_path_list[i])
            if not check_exists(upload_company_folder, file_path_list[i]):
                print(f"{file_path_list[i]} doesn't exist.")
                upload_file(upload_company_folder, file_path_list[i])
            else:
                print(f"{file_path_list[i]} already exists")

        # Uploading the target person's description
        file_path_list[2] = change_file_name(file_path_list[2])
        if not check_exists(upload_person_folder, file_path_list[2]):
            folder_name = file_path_list[2].split('/')[-1].split('.')[0]
            bucket = storage_Client.get_bucket(bucket_name)
            blob = bucket.blob(f"{upload_person_folder}{folder_name}/")
            blob.upload_from_string('')
            upload_file(f"{upload_person_folder}{folder_name}/", file_path_list[2])

        # Generating the mail
        mail_gen_instance = EmailGenFromGemini(model_name = 'gemini-pro',
                    source_path = file_path_list[0],
                    target_company_path = file_path_list[1],
                    target_person_path = file_path_list[2])
        mail_obj = mail_gen_instance.email_generation()
        # print(mail)
        print(type(mail_obj))
        
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
        {mail_obj["email_chat"]["formal"]}\
        </div>\
        </body>\
        </html>"
        #{mail_obj["email_chat"]["formal"]}
        print(mail_obj["email_chat"]["formal"])
        return templates.TemplateResponse("index.html", {"request": request, "message":  "Files uploaded successfully", "text":mail_obj["email_chat"]["formal"]})

    return templates.TemplateResponse("index.html", {"request": request, "message": "Error occurred!", "text": "Email is not generated."})