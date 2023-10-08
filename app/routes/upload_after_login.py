from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Depends, status, Security
from fastapi.templating import Jinja2Templates
import cloudinary
from cloudinary.uploader import upload
from app.database.config import settings
from app.database.models import User, Chat
from app.services.auth import auth_service
from app.repository.user_profile import create_user_profile
from app.database.db import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from app.repository import users as repository_users
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer

security = HTTPBearer()

router = APIRouter(prefix="/upload-pdf", tags=["upload-pdf"])

templates = Jinja2Templates(directory="app/templates")

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.cloud_api_key,
    api_secret=settings.cloud_api_secret
)

@router.get("/")
async def display_upload_form(request: Request, current_user: User = Depends(auth_service.get_current_user)):
     return templates.TemplateResponse("upload.html", {"request": request, "logged_in": current_user is not None})


# @router.post("/submit/")
# async def handle_file_upload(file: UploadFile = File(...), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):

#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")

#     try:
#         upload_result = None
#         with file.file as f:
#             upload_result = upload(f, public_id=f"{file.filename}", folder="files", format="pdf")
#         new_profile =  await create_user_profile(upload_result['url'], file.filename, current_user.id, db) 
#         if new_profile is None:
#             raise HTTPException(status_code=400, detail="File not uploaded2")
#         return upload_result['url']
#         # return {"info": f"file '{file.filename}' uploaded successfully", "url": upload_result['url']}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="File not uploaded")


# @router.get("/")
# async def display_upload_form(request: Request):
#      return templates.TemplateResponse("index.html", {"request": request})


@router.post("/submit/", response_class=HTMLResponse)
async def crete_llm(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    # try:
    #     token = credentials.credentials
    #     email = await auth_service.decode_refresh_token(token)
    #     current_user = await repository_users.get_user_by_email(email, db)
    # except:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not found token!")
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    print("Ok2")
    with file.file as f:
        embeddings = OpenAIEmbeddings()
        new_memory = FAISS.aadd_documents([file], embeddings)
    if new_memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not save!")
    new_chat = Chat(user_id = current_user.id)
    if new_chat is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat not created in DB!")
    print("Ok3")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return templates.TemplateResponse("chat.html", {"request": request, "memory": new_memory, "chat_id": new_chat.id, "current_user": current_user})
    # return {"request": request, "memory": new_memory, "chat_id": new_chat.id, "user_id": current_user.id}


