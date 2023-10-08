from fastapi import APIRouter, Depends, status, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session
from app.database.config import settings
from app.services.auth import auth_service

from app.database.models import Chat, User, UserProfile
from app.repository import llm as repository_llm
from app.repository import memory as repository_memory
from app.repository import history as repository_history
from app.database.db import get_db
from typing import List
from sqlalchemy import and_
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket
from langchain.vectorstores import FAISS



router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory='app/templates')

@router.get("/")
async def start_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


