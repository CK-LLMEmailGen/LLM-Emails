from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
import os
from dotenv import load_dotenv
from my_lib import wrap_text
from fastapi.responses import Response

load_dotenv()
# Create an instance of the FastAPI class
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

#get apikey
api_key = os.getenv("API_KEY")
openai.api_key = api_key


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate_text(data: dict):
    source = data.get("source")
    destination = data.get("destination")
    target = data.get("target")
    prompt = data.get("prompt")

    

    # Use the received values as needed, for example:
    document_files = [source+".txt", destination+".txt"]
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
        "Source": all_documents[1],
        "Destination": all_documents[0],
        # Add more information retrieved from PDFs
    }

    default_prompt=f'Generate an personalized email in about 200-250 words saying that how {pdf_information["Source"]} \
    services can be useful for {pdf_information["Destination"]}.\
            The information regarding the source and destination are obtained from text files and \
            stored as follows{pdf_information}.Utilize this information and provide me an \
            appropriate mail in a short and sweet manner saying that how the source services are useful to destination.\
            By reading the mail you have generated, the reader should show willingness to use the services.The email should always \
            written from the source to the destination and the recipient is {target}.The source and the destination are given in {pdf_information}'

    
    output=generate_email(default_prompt)
    
    return {"output": output}


def generate_email(prompt):
  response = openai.ChatCompletion.create(
      model="gpt-4-1106-preview", temperature=0,
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
  return wrap_text(generated_email)