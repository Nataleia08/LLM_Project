from fastapi import APIRouter, File, UploadFile, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from cloudinary.uploader import upload
from app.database.config import config_cloudinary
from app.database.models import User
from app.services.auth import auth_service
from typing import List


router = APIRouter(prefix="/upload-pdf", tags=["upload-pdf"])

templates = Jinja2Templates(directory="app/templates")

config_cloudinary()


@router.get("/")
async def display_upload_form(request: Request, current_user: User = Depends(auth_service.get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "logged_in": current_user is not None})


@router.post("/submit/")
async def handle_file_upload(files: List[UploadFile] = File(...), current_user: User = Depends(auth_service.get_current_user)):

    uploaded_files = []

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only PDF allowed.")
        try:
            with file.file as f:
                upload_result = upload(f, resource_type="raw", public_id=f"{file.filename}", folder="files", format="pdf")
                uploaded_files.append({"info": f"file '{file.filename}' uploaded successfully", "url": upload_result['url']})
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File {file.filename} not uploaded")

    return uploaded_files


