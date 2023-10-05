from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session
from app.database.config import settings
from app.services.auth import auth_service

from app.app.models import Chat, User
from app.repository import chat as repository_chat
from app.repository import history as repository_history
from app.database.db import get_db
from typing import List
from sqlalchemy import and_
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def start_chat():
    return templates.TemplateResponse("chat.html")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    new_llm = await repository_chat.start_chat(current_user.id, db)
    new_chat = Chat(user_id = current_user.id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    if new_llm is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="LLM not created!")
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You question: {data}")
        await repository_history.create_message(new_chat.id, current_user.id, data, db)
        answer = await repository_chat.question(new_llm, data)
        await websocket.send_text(f"Answer: {answer}")
