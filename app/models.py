import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(length=16), unique=True, nullable=False)
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    phone_number = Column(String(length=11), nullable=False)
    messages_out = relationship(
        "Message", back_populates="author", foreign_keys="Message.author_id"
    )
    messages_in = relationship(
        "Message", back_populates="receiver", foreign_keys="Message.receiver_id"
    )


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey("user.id"))
    receiver_id = Column(Integer, ForeignKey("user.id"))
    author = relationship(
        "User", back_populates="messages_out", foreign_keys=[author_id]
    )
    receiver = relationship(
        "User", back_populates="messages_in", foreign_keys=[receiver_id]
    )
