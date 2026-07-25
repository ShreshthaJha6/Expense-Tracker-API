from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_current_user
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)

):

    db_user = db.query(User).filter(

        User.email == form_data.username

    ).first()

    if not db_user:

        raise HTTPException(

            status_code=401,

            detail="Invalid Credentials"

        )

    if not verify_password(

        form_data.password,

        db_user.password

    ):

        raise HTTPException(

            status_code=401,

            detail="Invalid Credentials"

        )

    token = create_access_token(

        {

            "sub": db_user.email

        }

    )

    return {

        "access_token": token,

        "token_type": "bearer"

    }


@router.get("/me", response_model=UserResponse)
def read_me(
    current_user: User = Depends(get_current_user)
):
    return current_user