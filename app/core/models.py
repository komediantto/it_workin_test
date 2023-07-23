import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=16), unique=True, nullable=False)
    hashed_password = Column(String)
    first_name = Column(String(length=30), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    phone_number = Column(String(length=11), nullable=False)
    messages_out = relationship(
        "Message", back_populates="author", foreign_keys="Message.author_id"
    )


class Room(Base):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), unique=True, nullable=False)
    messages = relationship("Message", back_populates="room")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship(
        "User", back_populates="messages_out", foreign_keys=[author_id]
    )
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship("Room", back_populates="messages")
