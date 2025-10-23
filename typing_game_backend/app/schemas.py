from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class ParagraphBase(BaseModel):
    title: str
    content: str
    difficulty: str = "medium"

class ParagraphCreate(ParagraphBase):
    pass

class ParagraphOut(ParagraphBase):
    id: int 
    created_by: int | None = None

    class Config:
        model_config = ConfigDict(from_attributes=True)

class MatchOut(BaseModel):
    id: int
    player1_id: int
    player2_id: int
    winner_id: int | None
    player1_wpm: float
    player2_wpm: float
    created_at: datetime

    class Config:
        model_config = ConfigDict(from_attributes=True)