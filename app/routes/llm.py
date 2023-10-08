from fastapi import APIRouter, Depends, status, HTTPException, Request, File, UploadFile
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
from starlette.websockets import WebSocket
from langchain.vectorstores import FAISS



router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory='app/templates')

@router.get("/")
async def start_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    new_memory = FAISS()
    new_memory.load_local("/LLM_PROJECT/Data/llm.yaml")
    await websocket.accept()
    await websocket.send_text("Welcome to the chat!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You question: {data}")
            # await repository_history.create_message(chat_id, user_id, data, db)
            answer = new_memory.embed_query(data)
            await websocket.send_text(f"Answer: {answer}")
    except:
        await websocket.remove()
        return templates.TemplateResponse("start_chat")