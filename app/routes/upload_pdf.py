from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.templating import Jinja2Templates
import cloudinary
from cloudinary.uploader import upload
from config import CLOUDINARY

router = APIRouter(prefix="/upload_pdf", tags=["upload_pdf"])

templates = Jinja2Templates(directory="templates")

cloudinary.config(
    cloud_name=CLOUDINARY["cloud_name"],
    api_key=CLOUDINARY["api_key"],
    api_secret=CLOUDINARY["api_secret"]
)

@router.get("/from")
async def display_upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/submit")
async def handle_file_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")

    try:
        upload_result = None
        with file.file as f:
            upload_result = upload(f, resource_type="raw", public_id=f"{file.filename}", folder="files", format="pdf")
        return {"info": f"file '{file.filename}' uploaded successfully", "url": upload_result['url']}
    except Exception as e:
        raise HTTPException(status_code=400, detail="File not uploaded")


