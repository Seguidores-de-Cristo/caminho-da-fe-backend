"""Router para autenticação (JWT)."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.crud import user as crud_user
from app.core import security
from app.core.security import create_access_token
from app.models import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    from jose import JWTError

    try:
        payload = security.decode_access_token(token)
        email: Optional[str] = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = crud_user.get_user_by_email(db, email=email, include_inactive=False)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud_user.get_user_by_email(
        db,
        email=form_data.username,
        include_inactive=False
    )

    if not user or not crud_user.verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
