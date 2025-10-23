from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    elo = Column(Integer, default=1000) 
    seasonal_points = Column(Integer, default=0)

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

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"))
    player2_id = Column(Integer, ForeignKey("users.id"))
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id"), nullable=True)
    player1_wpm = Column(Float)
    player2_wpm = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
