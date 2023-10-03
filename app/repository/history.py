from typing import List

from sqlalchemy.orm import Session


from app.api.models import User, MessageHistory
from app.api.schemas import HistoryResponse

async def chat_history(chat_id: str, db: Session) -> List[HistoryResponse] | None:
    return db.query(MessageHistory).filter(MessageHistory.chat_id == chat_id).all()


async def user_history(user_id: str, db: Session) -> List[HistoryResponse] | None:
    return db.query(MessageHistory).filter(MessageHistory.user_id== user_id).all()