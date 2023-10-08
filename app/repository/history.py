from typing import List

from sqlalchemy.orm import Session


from app.database.models import MessageHistory
from app.database.schemas import HistoryResponse

async def chat_history(chat_id: str, db: Session) -> List[HistoryResponse] | None:
    return db.query(MessageHistory).filter(MessageHistory.chat_id == chat_id).all()

async def user_history(user_id: str, db: Session) -> List[HistoryResponse] | None:
    return db.query(MessageHistory).filter(MessageHistory.user_id== user_id).all()

async def create_message(chat_id: str, user_id: str, text: str, db: Session) -> HistoryResponse|None:
    new_message = MessageHistory(text_message = text, user_id = user_id, chat_id = chat_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message