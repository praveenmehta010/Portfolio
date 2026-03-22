import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.contact import Contact
from app.config.mongo_db_connection import contacts, projects

from dotenv import load_dotenv

load_dotenv()
routes = APIRouter()
templates = Jinja2Templates(directory="app/templates")

PROFILE_IMAGE_URL = os.getenv("PROFILE_IMAGE_URL")
def fetch_projects():
    docs = list(projects.find({}))
    # print(docs)
    return docs

@routes.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # Fetch the projects data
    projects = fetch_projects()
    return templates.TemplateResponse(
        request=request, name="index.html",
        # Pass the data to the template in a context dictionary
        context={"projects": projects, "PROFILE_IMAGE_URL":PROFILE_IMAGE_URL}
    )
    
    

@routes.post('/contact', status_code=201)
def add_product(contactDetails : Contact):
    contacts.insert_one(dict(contactDetails))