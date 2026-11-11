from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User as UserModel
from app.schemas import UserCreate, UserResponse
from app.security import PasswordHasher, create_access_token, get_current_user_id

router = APIRouter(tags=["users"])


@router.post("", status_code=201, response_model = UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    statement = select(UserModel).where(UserModel.username == user.username)
    existing_username = db.scalars(statement).first()
    statement = select(UserModel).where(UserModel.email == user.email)
    existing_email = db.scalars(statement).first()

    if existing_username is not None:
        raise HTTPException(status_code=409, detail=f"Username {user.username} is already taken")
    if existing_email is not None:
        raise HTTPException(status_code=409, detail=f"Email {user.email} is already registered")

    new_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=PasswordHasher().hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", status_code=200)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    statement = select(UserModel).where(UserModel.username == username)
    user = db.scalars(statement).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    check_password = PasswordHasher().verify_password(password, user.hashed_password)

    if not check_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    statement = select(UserModel).where(UserModel.id == int(user_id))
    user = db.scalars(statement).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user
