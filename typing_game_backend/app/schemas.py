from pydantic import BaseModel, EmailStr, ConfigDict

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