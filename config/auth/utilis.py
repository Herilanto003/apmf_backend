from passlib.context import CryptContext
import config.schemas as _sm
import config.models as _md
import sqlalchemy.orm as _orm
import fastapi as _fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


PDW_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated="auto")


# fonction pour vérifier le password hasher
def verify_password(plain_password, hashed_password):
    return PDW_CONTEXT.verify(plain_password, hashed_password)


# fonction pour obtenir le hash d'un password
def get_password_hash(password):
    return PDW_CONTEXT.hash(password)


# fonction pour l'authentification d'un utilisateur
def authenticate_user(user: OAuth2PasswordRequestForm, db: _orm.Session):
    # vérifier l'email de l' utilisateur
    user_auth = db.query(_md.Utilisateur).filter(_md.Utilisateur.email == user.username).first()

    print("ok")
    if not user_auth:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="EMAIL_NOT_EXIST")
    
    # si l' email est vérifier, on va vérifier ensuite le mot de passe entré
    if not verify_password(user.password, user_auth.password):
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_401_UNAUTHORIZED, detail="PASS_ERROR")
    
    return user_auth


