from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.database.models import User
from app.repository import chat as repository_chats
from app.database.schemas import ChatModel
from app.services.auth import auth_service

router = APIRouter(prefix='/new_chats', tags=["new_chats"])


@router.post("/ask", status_code=status.HTTP_201_CREATED)
async def post_question(request: Request, question: str = Form(...)):
    path_to_file = request.session.get("current_path_document")
    print(path_to_file)

    if not path_to_file:
        raise HTTPException(status_code=400, detail="Error path_to_file.")
    response = '_____________________________________________________________________'
    return {"response": response}


@router.post("/", response_model=ChatModel, status_code=status.HTTP_201_CREATED)
async def create_chat(body: ChatModel, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    new_chat = await repository_chats.create_chat(body, db, current_user)
    return new_chat


@router.get("/", response_model=List[ChatModel], status_code=status.HTTP_200_OK)
async def get_chats(limit: int = Query(10, le=50), offset: int = 0,
                    current_user: User = Depends(
                        auth_service.get_current_user),
                    db: AsyncSession = Depends(get_db)):
    chats = await repository_chats.get_chats(limit, offset, current_user, db)
    if chats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return chats


@router.get("/{chat_id}", response_model=ChatModel)
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    chat = await repository_chats.get_chat_by_id(chat_id, db, current_user)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Chat not found")
    return chat


@router.delete("/{chat_id}", response_model=ChatModel)
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    deleted_chat = await repository_chats.delete_chat(chat_id, db, current_user)
    if deleted_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Chat not found")
    return deleted_chat