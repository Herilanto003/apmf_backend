import fastapi as _fastapi
import typing as _typin
from routers.ContinentsRouter import router as continent_router
from routers.PaysRouter import router as pays_router
from routers.PortRouter import router as port_router
from routers.NavireRouter import router as navire_router
from routers.AccostageRouter import router as accostage_router
# from routers.ActionaireRouter import router as actionaire_router
from routers.MarchandiseRouter import router as marchandise_router
# from routers.ResponsableRouter import router as resp_router
from routers.Dashboard import router as dash_router
from routers.ResponsableNavireRouter import router as resp_navire_router
from routers.UtilisateurRouter import router as user_router
from routers.RapportRouter import router as rapport_router
from routers.StatisticRouter import router as statistic_router
from routers.Localisation import router as loc_router
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from config.auth.utilis import authenticate_user
from config.auth.token import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, get_current_active_user, SECRET_KEY, ALGORITHM, oauth2_scheme
from sqlalchemy.orm import Session
from config.schemas import UtilisateurToken
from config.connexion_db import get_db
from jose import jwt

class EmailSchema(BaseModel):
    email: List[EmailStr]


current_token = {}


revoked_tokens = []


conf = ConnectionConfig(
    MAIL_USERNAME = "herilantolouis@gmail.com",
    MAIL_PASSWORD = "mnuzehstltequbpb",
    MAIL_FROM = "herilantolouis@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="STATISTIQUE PORTUAIRE",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
)


app = _fastapi.FastAPI(
    title="statistique - portuaire",
    description="Api pour la gestion de statistique portuaire",
    summary="FASTAPI",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Herilanto Louis Denis",
        "email": "herilantolouis@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.post("/api/token", response_model=Token)
async def login_for_access_token(
    form_data:  OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    global current_token
    user = authenticate_user(form_data, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    current_token = access_token
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/revoke-token")
async def logout_account(token: str = _fastapi.Depends(oauth2_scheme), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    payload["exp"] = 0

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


@app.get('/user/me')
async def end_point(user: UtilisateurToken = _fastapi.Depends(get_current_user)):
    return user


@app.post("/email")
async def simple_send() -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=["herilantodenis@gmail.com"],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})


# inclusion du route pour le continent
app.include_router(user_router)


# inclusion du route pour le continent
app.include_router(rapport_router)

# inclusion du route pour le continent
app.include_router(continent_router)

# inclusion du route pour le pays
app.include_router(pays_router) 

# inclusion du route pour le port
app.include_router(port_router)

# inclusion du route pour le navire
app.include_router(navire_router)

# inclusion du route pour le actionaire
app.include_router(marchandise_router)

# inclusion du route pour le responsable
app.include_router(resp_navire_router)

# inclusion du route pour le statistic
app.include_router(statistic_router)

# inclusion du route pour le statistic
app.include_router(accostage_router)

# inclusion du route pour le statistic
app.include_router(dash_router)

# inclusion du route pour le statistic
app.include_router(loc_router)
