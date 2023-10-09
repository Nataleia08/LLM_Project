import enum

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func, Boolean, Text, Date, Float, Enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=True, unique=True)
    password = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    username = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)


class UserProfile(Base):
    __tablename__ = 'users_profiles'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    phone = Column(String(50), nullable=True)
    file_url = Column(Text, nullable=False)
    file_name = Column(String, nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), unique=False, nullable=False)
    user = relationship('User', backref='user_profiles')

class UserRole(str, enum.Enum):
    admin: str = 'admin'
    user: str = 'user'


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True)
    text_message = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user = relationship('User', backref='message_history')
    # chat_id = Column('chat_id', ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    # chat = relationship('Chat', backref='message_history')
    chat_id = Column(Integer)

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    title_chat = Column(String, nullable=True)
    file_url = Column(String, nullable=True)
    chat_data = Column(String, nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', backref='chat')

