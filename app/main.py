import os
import write_to_log as wtl
from share import gcp, mail
from dotenv import load_dotenv 
from google.cloud import storage
from mail_gen import EmailGenFromGemini
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, File, UploadFile, Request, Form
app = FastAPI()

# List of folder paths
folder_path_list = [
    "/workspace/LLM-Emails/app/uploads/product_description/",
    "/workspace/LLM-Emails/app/uploads/source_company/",
    "/workspace/LLM-Emails/app/uploads/target/target_company/",
    "/workspace/LLM-Emails/app/uploads/target/target_person/" 
]
file_path_list = []                                                                                                     # list of file paths

# Ensure upload folders are created
for i in range(4):
    os.makedirs(folder_path_list[i], exist_ok = True)

# Initialize templates
templates = Jinja2Templates(directory="/workspace/LLM-Emails/app/templates")

# Checking if the service account is correctly authenticated or not
def authenticate(storage_client : storage.Client = None) -> bool:
    try:
        temp_project_id = storage_client.project
        return temp_project_id == gcp.project_id
    except Exception as e:
        # print(f"Exception:\n{e}")
        wtl.write_to_file(wtl.gcp_log, e)
        return False



# change_file_name
def change_file_name(filepath : str = None) -> str:
    original_file_path = filepath
    file_list = filepath.split('/')
    file_name = file_list[-1].replace(" ", "_")
    file_name = file_name[0].upper() + file_name[1:]
    result_path = "/".join([*file_list[:-1], file_name])
    os.rename(original_file_path,result_path)
    return result_path
        



# Function to check if upload file exists in cloud bucket or not:
def check_exists(storage_client : storage.Client = None, folder_name : str = None, file_path : str = None) -> bool:
    file_name = file_path.split('/')[-1]
    bucket = storage_client.get_bucket(gcp.bucket_name)
    blobs = bucket.list_blobs(prefix = folder_name)
    blob = any(blob.name == f"{folder_name}{file_name}" for blob in blobs)
    if blob:
        return True
    return False
    


# Upload file to the bucket:
def upload_file(storage_client : storage.Client = None, folder_name : str = None, file_path : str = None):
    file_name = file_path.split('/')[-1]
    bucket = storage_client.get_bucket(gcp.bucket_name)
    blob = bucket.blob(f"{folder_name}{file_name}")
    blob.upload_from_filename(file_path)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request, message: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "message": message})


@app.post("/")
async def upload_files(request: Request,
                       productDescription: UploadFile = File(...),
                       sourceCompany: UploadFile = File(...),
                       targetCompany: UploadFile = File(...),
                       targetPerson: UploadFile = File(...),
                        tone: str = Form(...)):
        try:
            file_objects_list = [productDescription, sourceCompany, targetCompany, targetPerson]                                            # list of file objects
            
            for i in range(4):  
                file_path_list.append(os.path.join(folder_path_list[i], file_objects_list[i].filename))
            
            # Storing the uploaded files in their respective folders.
            for i in range(4):
                with open(file_path_list[i], "wb") as buffer:
                    buffer.write(await file_objects_list[i].read())

        except Exception as e:
            wtl.write_to_file(wtl.data_upload_log, e)


        try:
            # storage_Client object
            storage_client = storage.Client.from_service_account_json(gcp.key_path)

            # Authenticating for gcp bucket
            if authenticate(storage_client):
                # Uploading the target and source company's description
                for i in range(3):
                    file_path_list[i] = change_file_name(file_path_list[i])
                    if not check_exists(storage_client, gcp.upload_company_folder, file_path_list[i]):
                        print(f"{file_path_list[i]} doesn't exist.")
                        upload_file(storage_client, gcp.upload_company_folder, file_path_list[i])
                    else:
                        print(f"{file_path_list[i]} already exists")

                # Uploading the target person's description
                file_path_list[3] = change_file_name(file_path_list[3])
                target_company_name = f"{file_path_list[1].split('/')[-1].split('.')[0]}"
                folder_name = gcp.upload_person_folder + target_company_name + "/"
                if not check_exists(storage_client, gcp.upload_person_folder, target_company_name + "/"):                       # Check if company folder for target person exists or not.
                    bucket = storage_client.get_bucket(gcp.bucket_name)
                    blob = bucket.blob(f"{target_company_name}/")
                    bolb.upload_from_string('')
                if not check_exists(storage_client, folder_name, file_path_list[3]):
                    upload_file(storage_client, f"{folder_name}", file_path_list[3])
                    print(f"{file_path_list[2]} doesn't exist.")
                else:
                    print(f"{file_path_list[2]} already exists.")
        
        except Exception as e:
            print(f"{e}")
            # wtl.write_to_file(wtl.gcp_log, e)
        
        try:
            # Generating the mail
            mail_gen_instance = EmailGenFromGemini(model_name = 'gemini-pro',
                        product_path = file_path_list[0],
                        source_path = file_path_list[1],
                        target_company_path = file_path_list[2],
                        target_person_path = file_path_list[3],
                        source_company = "Mondee",
                        target_company = "Accenture",
                        target_person = "Karan Gupta")
            mail_obj = mail_gen_instance.email_generation()
            
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

            print(mail_obj["email_chat"]["formal"].rstrip(mail.delimiter),end="\n\n")
            print(mail_obj["email_chat"]["semi-formal"].rstrip(mail.delimiter),end="\n\n")
            print(mail_obj["email_chat"]["jovial"].rstrip(mail.delimiter),end="\n\n")
            return templates.TemplateResponse("index.html", {"request": request, "message":  "Files uploaded successfully", "text":mail_obj["email_chat"]["jovial"].strip(f"{mail.delimiter}")})
        
        except Exception as e:
            wtl.write_to_file(wtl.generated_mails_log, e)

        return templates.TemplateResponse("index.html", {"request": request, "message": "Error occurred!", "text": "Email is not generated."})