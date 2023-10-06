from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
import cloudinary
from cloudinary.uploader import upload
from app.database.config import settings
from app.app.models import User
from app.services.auth import auth_service
from app.repository.user_profile import create_user_profile
from app.database.db import get_db
from sqlalchemy.orm import Session



router = APIRouter(prefix="/upload-pdf", tags=["upload-pdf"])

templates = Jinja2Templates(directory="templates")

cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.cloud_api_key,
    api_secret=settings.cloud_api_secret
)

@router.get("/")
async def display_upload_form(request: Request, current_user: User = Depends(auth_service.get_current_user)):
     return templates.TemplateResponse("index.html", {"request": request, "logged_in": current_user is not None})


@router.post("/submit/")
async def handle_file_upload(file: UploadFile = File(...), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")

    try:
        upload_result = None
        with file.file as f:
            upload_result = upload(f, public_id=f"{file.filename}", folder="files", format="pdf")
        new_profile =  await create_user_profile(upload_result['url'], file.filename, current_user.id, db) 
        if new_profile is None:
            raise HTTPException(status_code=400, detail="File not uploaded2")
        return upload_result['url']
        # return {"info": f"file '{file.filename}' uploaded successfully", "url": upload_result['url']}
    except Exception as e:
        raise HTTPException(status_code=400, detail="File not uploaded")


