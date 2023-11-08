from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.models import Utilisateur
from config.connexion_db import get_db
from config.schemas import UtilisateurToken


SECRET_KEY = "d96f16672e55f6caaa2c7405024b81cba9e3736511b8570319ece09ea4e4bdb3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7200


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


# création d' un nouveau token 
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# fonction return l' utilisateur courant
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(Utilisateur).filter(Utilisateur.email == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


# fonction return un utilisateur activé
async def get_current_active_user(current_user: UtilisateurToken = Depends(get_current_user)):
    if not current_user.status_compte:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="NOT_ACTIVE")
    return current_user


