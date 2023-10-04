from fastapi import APIRouter, Depends, status, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.app.models import User
from app.repository import users as repository_users
from app.services.auth import auth_service
# from src.services.upload_avatar import UploadService
from app.app.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory='templates')


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.get("/profile", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('test_form.html', {"request": request, "email": None, "text": None})


@router.post("/profile", response_class=HTMLResponse)
async def root(request: Request, email=Form(), text=Form()):
    print(email, text)
    return templates.TemplateResponse('test_form.html', {"request": request, "email": email, "text": text})