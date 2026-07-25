from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.database import SessionLocal


from app.auth import decode_access_token

from app.models import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()



def get_current_user(

        token: str = Depends(oauth2_scheme),

        db: Session = Depends(get_db)

):

    payload = decode_access_token(token)

    if payload is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token"

        )

    email = payload.get("sub")

    if email is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token"

        )

    user = db.query(User).filter(

        User.email == email

    ).first()

    if user is None:

        raise HTTPException(

            status_code=401,

            detail="User not found"

        )

    return user