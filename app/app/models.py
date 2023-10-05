import enum

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func, Boolean, Text, Date, Float, Enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    username = Column(String(50))
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)


class UserProfile(Base):
    __tablename__ = 'users_profiles'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    # date_of_birth = Column(Date)
    date_of_birth = Column(String(50))
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    user = relationship('User', backref='user_profiles')

class UserRole(str, enum.Enum):
    admin: str = 'admin'
    user: str = 'user'


class MessageHistory(Base):
    __tablename__ = 'message_history'
    id = Column(Integer, primary_key=True)
    text_message = Column(String(255), nullable=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    user = relationship('User', backref='message_history')
    chat_id = Column('chat_id', ForeignKey('chat.id', ondelete='CASCADE'), unique=True, nullable=False)
    chat = relationship('Chat', backref='message_history')

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    user = relationship('User', backref='chat')