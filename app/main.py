from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db.session import get_db, init_db
from . import models
from .schemas import user as user_schema
from .crud import user as crud_user

app = FastAPI(title="Caminho da Fé API")

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/users/", response_model=user_schema.UserOut)
def create_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db, user_in)

@app.get("/users/{user_id}", response_model=user_schema.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user