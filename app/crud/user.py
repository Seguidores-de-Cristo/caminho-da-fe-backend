from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from passlib.context import CryptContext
from ..schemas.user import UserUpdate

# Use Argon2 to avoid bcrypt's 72-byte password truncation limit and
# backend-detection complications. Argon2 provides strong, modern hashing
# without the fixed 72-byte limit.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed, nome=user_in.nome)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str, include_inactive: bool = True):
    if (not include_inactive):
        return db.query(User).filter(User.email == email, User.is_active == True).first()
    return db.query(User).filter(User.email == email).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:

    if user_in.nome is not None:
        db_user.nome = user_in.nome

    if user_in.telefone is not None:
        db_user.telefone = user_in.telefone

    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active

    db.commit()
    db.refresh(db_user)
    return db_user