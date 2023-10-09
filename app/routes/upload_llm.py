from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Depends, status, Security
from fastapi.templating import Jinja2Templates
import cloudinary
from cloudinary.uploader import upload
from app.database.config import settings
from app.database.models import User, Chat, UserProfile
from app.services.auth import auth_service
from app.repository.user_profile import create_user_profile
from app.database.db import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms.openai import OpenAIChat
from langchain.vectorstores import FAISS
from app.repository import users as repository_users
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from app.database.config import OPENAI_API_KEY
from fastapi.staticfiles import StaticFiles
from typing import List

security = HTTPBearer()

router = APIRouter(prefix="/upload-pdf", tags=["upload-pdf"])

templates = Jinja2Templates(directory="app/templates")
router.mount('/static', StaticFiles(directory='app/static'), name='static')

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.cloud_api_key,
    api_secret=settings.cloud_api_secret
)

@router.get("/")
async def display_upload_form(request: Request,):
     return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/submit/", response_class=HTMLResponse)
async def crete_llm(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    new_user = User()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    with file.file as f:
        upload_result = upload(f, resource_type="raw", public_id=f"{file.filename}", folder="files", format="pdf")
        new_profile = UserProfile(file_name = file.filename, file_url = upload_result['url'], user_id = new_user.id)
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        loader = PyPDFLoader(upload_result['url'])
        pages = loader.load_and_split()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(pages)
        embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
        new_memory = FAISS.from_documents(docs, embeddings)
        new_memory.save_local("/LLM_PROJECT/Data/llm.yaml")

    if new_memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not save!")
    return templates.TemplateResponse("chat_ws.html", {"request": request})


@router.post("/submit2/", response_class=HTMLResponse)
async def handle_file_upload(request: Request, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):

    uploaded_files = []
    new_user = User()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only PDF allowed.")
        try:
            with file.file as f:
                upload_result = upload(f, resource_type="raw", public_id=f"{file.filename}", folder="files", format="pdf")
                uploaded_files.append({"info": f"file '{file.filename}' uploaded successfully", "url": upload_result['url']})
                new_profile = UserProfile(file_name = file.filename, file_url = upload_result['url'], user_id = new_user.id)
                db.add(new_profile)
                db.commit()
                db.refresh(new_profile)
                loader = PyPDFLoader(upload_result['url'])
                pages = loader.load_and_split()
                text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                docs = text_splitter.split_documents(pages)
                embeddings = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY)
                new_memory = FAISS.from_documents(docs, embeddings)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File {file.filename} not uploaded")
    new_memory.save_local("/LLM_PROJECT/Data/llm.yaml")

    if new_memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not save!")
    return templates.TemplateResponse("chat_ws.html", {"request": request})