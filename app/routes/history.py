from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from langchain.memory import PostgresChatMessageHistory
from app.database.config import settings
from app.services.auth import auth_service

from app.api.models import MessageHistory, User
from app.api.schemas import HistoryResponse
from app.repository import history as repository_history
from app.database.db import get_db
from typing import List
from sqlalchemy import and_


router = APIRouter(prefix="/history", tags=["history"])


@router.post("/save_massegas")
async def save_messages(text: str, chat_id: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    history = PostgresChatMessageHistory(connection_string= settings.sqlalchemy_database_url, session_id=chat_id, table_name='message_history')
    history.add_user_message(text)
    return None


@router.get("/save_massages/chat_id", response_model= List[HistoryResponse])
async def get_history_messages(chat_id: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    chat_history = await repository_history.chat_history(chat_id, db)
    if chat_history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found!')
    return chat_history
    
@router.get("/save_massages/user_id", response_model= List[HistoryResponse])
async def get_history_messages(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    chat_history = await repository_history.user_history(user_id, db)
    if chat_history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found!')
    return chat_history   

@router.delete("/save_massages/message_id")
async def get_history_messages(chat_id:str, message_id: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    delete_message = db.query(MessageHistory).filter(and_(MessageHistory.chat_id == chat_id, MessageHistory.message_id == message_id)).first()
    if delete_message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Message not found!')
    db.delete(delete_message)
    db.commit()