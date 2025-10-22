from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...app import models, schemas
from ..database import get_db


router = APIRouter(prefix="/paragraphs", tags=["Paragraphs"])

#Create paragraph
@router.post("/", response_model=schemas.ParagraphOut)
def create_paragraph(paragraph:schemas.ParagraphCreate, db: Session = Depends(get_db)):
    new_paragraph = models.Paragraph(
        title = paragraph.title, 
        content = paragraph.content,
        difficulty = paragraph.difficulty,
        created_by = None #later will be user_id after authentication
    )

    db.add(new_paragraph)
    db.commit()
    db.refresh(new_paragraph)
    return new_paragraph

# Get All paragraphs
@router.get("/", response_model=list[schemas.ParagraphOut])
def get_paragraphs(db: Session = Depends(get_db)):
    paragraphs = db.query(models.Paragraph).all()
    return paragraphs

# Get single paragraph by id
@router.get("/{id}", response_model=schemas.ParagraphOut)
def get_paragraph(id: int, db: Session = Depends(get_db)):
    paragraph = db.query(models.Paragraph).filter(models.Paragraph.id == id).first()
    if not paragraph:
        raise HTTPException(status_code=404, detail="Paragraph not found")
    return paragraph

#Delete paragraph
@router.delete("{id}")
def delete_paragraph(id: int, db: Session = Depends(get_db)):
    paragraph = db.query(models.Paragraph).filter(models.Paragraph.id == id).first()
    if not paragraph:
        raise HTTPException(status_code=404, detail="Paragraph not found")
    db.delete(paragraph)
    db.commit()
    return{"message": "Paragraph deleted"}