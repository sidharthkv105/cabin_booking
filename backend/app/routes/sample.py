from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, db

router = APIRouter()

def get_db():
    db_session = db.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

@router.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db_session: Session = Depends(get_db)):
    db_item = models.Item(name=item.name)
    db_session.add(db_item)
    db_session.commit()
    db_session.refresh(db_item)
    return db_item