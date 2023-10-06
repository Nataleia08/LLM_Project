from fastapi import APIRouter, Depends, status, HTTPException, Request, File
from sqlalchemy.orm import Session
from app.database.config import settings
from app.services.auth import auth_service

from app.app.models import Chat, User, UserProfile
from app.repository import llm as repository_llm
from app.repository import memory as repository_memory
from app.repository import history as repository_history
from app.database.db import get_db
from typing import List
from sqlalchemy import and_
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, WebSocket


router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory='app/templates')

@router.get("/")
async def start_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user_pr = db.query(UserProfile).filter(UserProfile.user_id== current_user.id)
    new_memory = await repository_memory.create_memmory(user_pr.file_url)
    new_llm = await repository_llm.create_llm(new_memory)
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
        answer = await repository_llm.question_from_llm(new_llm, data)
        await websocket.send_text(f"Answer: {answer}")


@router.post("/start")
async def crete_llm(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user_pr = db.query(UserProfile).filter(UserProfile.user_id== current_user.id).first()
    if user_pr is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found!")
    new_memory = await repository_memory.create_memmory(user_pr.file_url)
    if new_memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not save!")
    new_llm = await repository_llm.create_llm(new_memory)
    if new_llm is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="LLM not created!")
    new_chat = Chat(user_id = current_user.id)
    if new_chat is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat not created in DB!")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return "Ok!"