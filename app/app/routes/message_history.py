from fastapi import APIRouter, Depends, status, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from langchain.memory import PostgresChatMessageHistory
from app.database.config import setting
from app.services.auth import auth_service

from app.api.models import MessageHistory


router = APIRouter(prefix="/history", tags=["history"])


@router.post("/save_massegas", response_class=HTMLResponse)
async def save_messages(text: str, chat_id: str, current_user: User = Depends(auth_service.get_current_user)):
    history = PostgresChatMessageHistory(connection_string= setting.sqlalchemy_database_url, session_id=chat_id, table_name=)
    history.add_user_message(text)
    return None


@router.get("/save_massages/chat_id")
async def get_history_messages():
    
    

@router.delete("/save_massages/chat_id")
async def get_history_messages()