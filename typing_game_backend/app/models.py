import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Paragraph(Base):
    __tablename__ = "paragraphs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    difficulty = Column(String, default="medium") #easy | medium | hard
    created_by = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", backref="paragraphs")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, ForeignKey("users.id"))
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"))
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id"), nullable=True)
    player1_wpm = Column(float)
    player2_wpm = Column(float)
    created_at = Column(DateTime, default=datetime.utc)
