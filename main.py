from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from mail_gen import EmailGenFromGemini 
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
    
    # Now you can access the selected tone using the 'tone' variable
    print("Selected tone:", tone)
    text="Hi!!!!!!"
    mail_gen_instance = EmailGenFromGemini(model_name = 'gemini-pro',
                 source_path = product_path,
                 target_company_path = target_company_path,
                 target_person_path = target_person_path)
    mail = mail_gen_instance.email_generation()
    print(mail)
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
    
    print(mail['email'])
    return templates.TemplateResponse("index.html", {"request": request, "message":  "Files uploaded successfully","text":mail['email']})
