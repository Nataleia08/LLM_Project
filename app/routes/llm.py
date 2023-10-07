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
from fastapi import FastAPI, WebSocket
import aspose.words as aw
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders.pdf import OnlinePDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import pickle
from langchain.llms import OpenAI
from fastapi.responses import HTMLResponse
import asyncio
from websockets.sync.client import connect


router = APIRouter(prefix="/chat", tags=["chat"])
templates = Jinja2Templates(directory='app/templates')

@router.get("/")
async def start_chat(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
#     user_pr = db.query(UserProfile).filter(UserProfile.user_id== current_user.id)
#     new_memory = await repository_memory.create_memmory(user_pr.file_url)
#     new_llm = await repository_llm.create_llm(new_memory)
#     new_chat = Chat(user_id = current_user.id)
#     db.add(new_chat)
#     db.commit()
#     db.refresh(new_chat)
#     if new_llm is None:
#         raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="LLM not created!")
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"You question: {data}")
#         await repository_history.create_message(new_chat.id, current_user.id, data, db)
#         answer = await repository_llm.question_from_llm(new_llm, data)
#         await websocket.send_text(f"Answer: {answer}")


@router.post("/start")
async def crete_llm(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user_pr = db.query(UserProfile).filter(UserProfile.user_id== current_user.id).first()
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
    return new_chat


@router.post("/start3")
async def crete_llm(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user_pr = db.query(UserProfile).filter(UserProfile.user_id== current_user.id).first()
    doc = aw.Document(user_pr.file_url)
    new_memory = await repository_memory.create_memmory2(doc.get_text())
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
    return new_chat

@router.post("/start2")
async def crete_llm(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    doc = aw.Document(file)
    new_memory = await repository_memory.create_memmory2(doc.get_text())
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
    return new_chat

@router.post("/start4")
async def crete_llm(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    with file.file as f:
        f_pic = pickle.load(f)
        loader = PyPDFLoader(file_path=f_pic)
        pages = loader.load_and_split()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(pages)
        embeddings = OpenAIEmbeddings()
        new_memory = FAISS.from_documents(docs, embeddings).as_retriever()
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
    return 


@router.post("/start5")
async def crete_llm(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    with file.file as f:
        embeddings = OpenAIEmbeddings()
        new_memory = FAISS.aadd_documents([file], embeddings)
    if new_memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not save!")
    new_chat = Chat(user_id = current_user.id)
    if new_chat is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat not created in DB!")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


@router.post("/start6", response_class=HTMLResponse)
async def crete_llm(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    with file.file as f:
        embeddings = OpenAIEmbeddings()
        new_memory = FAISS.aadd_documents([file], embeddings)
    if new_memory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Memory not save!")
    new_chat = Chat(user_id = current_user.id)
    if new_chat is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat not created in DB!")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    with connect("ws://localhost:8000/chat") as websocket:
        await websocket.accept()
        await websocket.send_text("Welcome to the chat!")
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"You question: {data}")
            await repository_history.create_message(new_chat.idid, current_user.id, data, db)
            answer = new_memory.embed_query(data)
            await websocket.send_text(f"Answer: {answer}")




# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
#     if not file.filename.endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
#     with file.file as f:
#         embeddings = OpenAIEmbeddings()
#         new_memory = FAISS.aadd_documents([file], embeddings)
#     new_chat = Chat(user_id = current_user.id)
#     if new_chat is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Chat not created in DB!")
#     db.add(new_chat)
#     db.commit()
#     db.refresh(new_chat)
#     await websocket.accept()
#     await websocket.send_text("Welcome to the chat!")
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"You question: {data}")
#         await repository_history.create_message(new_chat.id, current_user.id, data, db)
#         answer = new_memory.embed_query(data)
#         await websocket.send_text(f"Answer: {answer}")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, memory, chat_id: int, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    await websocket.send_text("Welcome to the chat!")
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You question: {data}")
        await repository_history.create_message(chat_id, user_id, data, db)
        answer = memory.embed_query(data)
        await websocket.send_text(f"Answer: {answer}")