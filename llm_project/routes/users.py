from fastapi import APIRouter, Depends, status, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from llm_project.database.db import get_db
from llm_project.database.models import User
from llm_project.repository import users as repository_users
from llm_project.services.auth import auth_service
# from src.services.upload_avatar import UploadService
from llm_project.database.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory='templates')


@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user