from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import os
from dotenv import load_dotenv
from my_lib import wrap_text
from fastapi.responses import Response
import pandas as pd
import math

load_dotenv()
# Create an instance of the FastAPI class
app = FastAPI()

app.mount("/", StaticFiles(directory="react-app/build", html = True), name="static")

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="react-app")
react_Templates = Jinja2Templates(directory="react-app/build")

#get apikey
api_key = os.getenv("API_KEY")
openai.api_key = api_key

@app.get("/")
async def show_Prospects(request: Request):
    return react_Templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def fetch_Prospects(request: Request, filters: dict):
    sample_Companies = [
        ['google', 'Google', 'Mountain View, California', 10001, 80000, 'past1Month', ['Series A'], 10000000, 800000000], 
        ['amazon', 'Amazon', 'Seattle, Washington', 1300, 40000, 'past3Months', ['Series A'], 5000000, 500000000], 
        ['cstrike', 'CrowdStrike', 'Austin, Texas', 800, 20000, 'past1Year', ['Series C'], 700000, 4000000], 
        ['mondee', 'Mondee', 'Austin, Texas', 300, 5000, 'past1Year', ['Series D'], 500000, 1000000], 
        ['citi', 'Citi', 'New York, New York', 4400, 30000, 'past9Months', ['Series B'], 4000000, 60000000]
    ]
    company_Atrributes = ['id', 'name', 'location', 'employees', 'webTraffic', 'lastFundingDate', 'lastFundingType', 'lastFundingAmount', 'totalFunding']
    company_Df = pd.DataFrame(sample_Companies, columns = company_Atrributes)
    
    return JSONResponse(content = {'companies': company_Df.to_dict(orient = 'records'), 'employees': []})


@app.get("/generate", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_text(data: dict):
    source = data.get("source")
    target = data.get("destination")
    target_person = data.get("target")
    prompt = data.get("prompt")
    tone=data.get("tone")

    
    # Use the received values as needed, for example:
    document_files = [source+".txt",target+".txt",target_person+".txt"]
    all_documents=[]
    # Load multiple documents
    for file_path in document_files:
        loader = TextLoader(file_path)
        documents = loader.load()
        all_documents.extend(documents)

    # Split the combined documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(all_documents)
    
    # Assuming you've obtained information and answers from the PDFs
    pdf_information = {
        "Source": all_documents[0],
        "target": all_documents[1],
        "target_person":all_documents[2]
        
        # Add more information retrieved from PDFs
    }
    

    # default_prompt=f'Generate an personalized email in about 200-250 words saying that how .\
    #         The information regarding the source and destination are obtained from text files and \
    #         stored as follows{pdf_information}.Utilize this information and provide me an \
    #         appropriate mail in a short and sweet manner saying that how the source services are helpful to destination platform.\
    #         By reading the mail you have generated, the reader should show willingness to use the services.The email should always be \
    #         written from the source to the destination explaining how services offered by source company is useful for the destination company\
    #         and the recipient is {target}.The source and the destination are given in {pdf_information}.The specifications on how the mail \
    #         should be are given in {prompt}.Include these requirements/specifications while generating your response'

    default_prompt=f"Find {source} mail address and {target_person} mail address from {pdf_information}.\
        From {source} mail address, send a personalized mail to {target_person} mail address in about 200-250 words\
        saying that how {source} services can be useful for {target}.Do not include content related to {source} in the \
        email subject.Start the email subject with topic related to {target_person} and praising {target} for its services. \
        The information regarding the {source} ,{target} and {target_person} are obtained from text files and \
        stored as follows{pdf_information}.use the {target_person} information while generating your response and provide me an \
        appropriate mail saying that how the {source} services are useful to {target}\
        and the response should be short and sweet.By reading the mail you have generated, \
        the reader should show willingness to use the services.Start the email as if you are talking to the {target_person}\
        and include their information for example about their university or working experiences or any other information \
        available at {pdf_information['target_person'] }.Add additional information about their information for example \
        the places or any experiences with their universityand then start saying about how the{source} services are useful for \
        the {target}.T"
    
    email_content=generate_email(default_prompt)
    changed_tone=changeTone(email_content,tone)
    formatted_email_content = email_content.replace("\n", "<br>")  # Replace newlines with HTML line breaks
    
    # Construct HTML response to display formatted email content
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
    {formatted_email_content}\
    </div>\
    </body>\
    </html>"
    
    return html_response
    
    


def generate_email(prompt):
  response = openai.ChatCompletion.create(
      model="gpt-4-1106-preview", temperature=1,
      messages=[
          {
              "role": "system",
              "content": prompt
          }
      ],
      max_tokens=500 # Adjust the desired length of the email generated
  )

  # Get the generated email text
  generated_email = response['choices'][0]['message']['content']
  
  return (generated_email)


def changeTone(info,tone):
    prompt1=f"Identify the tone of the{info} and classify it whether it is formal or semi formal or informal.\
    Just give me the answer only do not give any reasons or description"
    print(generate_email(prompt1))
    prompt=f"Change the {info} into the tone specified here {tone}"
    toned_mail = generate_email(prompt)
    prompt2=f"what is the tone of {toned_mail}.Is it formal or informal or semi formal\
    Just give me the answer only do not give any reasons or description"
    print(generate_email(prompt2))
    return toned_mail