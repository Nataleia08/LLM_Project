import logging

from sqlalchemy.orm import Session, Query

from llm_project.database.models import UserProfile
from llm_project.database.schemas import UserProfileCreate


async def create_user_profile(file_path: str, file_name: str, user_id: str, db: Session):
    new_profile = UserProfile(file_url = file_path, file_name = file_name, user_id = user_id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile