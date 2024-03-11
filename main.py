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



# # get_file_name
# def get_file_name(filepath : str = None) -> str:
#     return filepath.split('/')[-1]



# change_file_name
def change_file_name(filepath : str = None) -> None:
    original_file_path = filepath
    file_list = filepath.split('/')
    file_list[-1] = file_list[-1].lower().replace(" ","_")
    result_path = ""
    for string in file_list:
        result_path += string
        result_path += "/"
    result_path = result_path[0:-1]
    os.rename(original_file_path,result_path)



# Function to check if upload file exists in cloud bucket or not:
def check_file_exists(folder_name : str = None, file_path : str = None) -> bool:
    file_name = file_path.split('/')[-1]
    bucket = storage_Client.get_bucket("email_gen_llm")
    blob = bucket.blob(f"{folder_name}{file_name}")
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

    product_path=os.path.join(product_description_folder, productDescription.filename)
    target_company_path=os.path.join(target_company_folder, targetCompany.filename)
    target_person_path=os.path.join(target_person_folder, targetPerson.filename)
    print(product_path,target_company_path,target_person_path)
    # Save product description file
    with open(product_path, "wb") as buffer:
        buffer.write(await productDescription.read())
    
    # Save target company file
    with open(target_company_path, "wb") as buffer:
        buffer.write(await targetCompany.read())
    
    # Save target person file
    with open(target_person_path, "wb") as buffer:
        buffer.write(await targetPerson.read())

    if authenticate():

        change_file_name(product_path)
        change_file_name(target_company_path)
        change_file_name(target_person_path)

        if not check_file_exists(upload_company_folder, product_path):
            upload_file(upload_company_folder, product_path)
        
        if not check_file_exists(upload_company_folder, target_company_path):
            upload_file(upload_company_folder, target_company_path)

        if not check_file_exists(upload_person_folder, target_person_path):
            upload_file(upload_person_folder, target_person_path)
        # # Now you can access the selected tone using the 'tone' variable
        # print("Selected tone:", tone)
        # text="Hi!!!!!!"
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
        
        # print(mail['email'])
        return templates.TemplateResponse("index.html", {"request": request, "message":  "Files uploaded successfully", "text":mail['email']})

    return templates.TemplateResponse("index.html", {"request": request, "message": "Error occurred!", "text": "Email is not generated."})
