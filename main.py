import os
from dotenv import load_dotenv

from google.cloud import storage
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI,Request
app = FastAPI()

#
# Initialize templates
templates = Jinja2Templates(directory="templates")




@app.get("/", response_class=HTMLResponse)
async def home(request: Request, message: str = None):
    return templates.TemplateResponse("main.html", {"request": request})

