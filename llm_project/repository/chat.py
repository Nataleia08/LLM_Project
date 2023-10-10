import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from app.database.models import User, Chat
from app.database.schemas import ChatModel, ChatModelShot
from app.database.db import get_db
from fastapi import Depends
import random


async def delete_source_file(path):
    file_path = path
    os.remove(file_path)


async def create_chat(body: ChatModel, db: AsyncSession, user: User) -> Chat:
    context = True

    new_chat = Chat(title_chat=body.title_chat, chat_data=context,
                    file_url=body.file_url, user_id=user.id)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return new_chat

async def create_chat_shot(db: Session) -> Chat:
    new_chat = Chat(user_id = random.randint(0, 10000))
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


async def delete_chat(chat_id: int, db: AsyncSession, user: User) -> Chat | None:
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        if chat.user_id == user.id:
            await delete_source_file(chat.file_url)
            await db.delete(chat)
            await db.commit()
    return chat


async def get_chat_by_id(chat_id: int, db: AsyncSession, user: User) -> Chat | None:
    return db.query(Chat).filter(and_(Chat.id == chat_id, Chat.user_id == user.id)).first()


async def get_chats(limit: int, offset: int, user: User, db: AsyncSession) -> list | None:
    chats = db.query(Chat).filter(and_(Chat.user_id == user.id)).order_by(desc(Chat.created_at)).limit(limit).offset(
        offset).all()
    return chats
