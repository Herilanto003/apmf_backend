# importation des packages
from sqlalchemy.orm import Session
from config.models import Utilisateur
from config.schemas import UtilisateurSchema, EmailSchema, Code
from datetime import datetime
import fastapi as _fastapi
from config.auth.utilis import get_password_hash
from sqlalchemy.sql import text
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from starlette.responses import JSONResponse
from config.email_conf import fm
from config.connexion_db import get_db
import uuid
from sqlalchemy import and_


DATA_BASE: Session = _fastapi.Depends(get_db)


# fonction pour vérifier l'email exitant
def is_email_exist(email: str, db: Session):
    exist_email = db.query(Utilisateur).filter(Utilisateur.email==email).first()

    if not exist_email:
        return False

    return True 


async def create_new_user(req: UtilisateurSchema, code: str, db: Session):
    if req.nom == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "NOM"})
    if req.email == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "EMAIL"})
    if req.password == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "PASSWORD"})

    new_user = Utilisateur(
        nom=req.nom,
        prenoms=req.prenoms,
        password=get_password_hash(req.password),
        email=req.email,
        status_compte=False,
        code_activation=code.upper()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 


def api_all_users(db: Session):
    all_users = db.query(Utilisateur).all()

    return all_users


def api_one_user(id_utilisateur: int, db: Session):
    one_user = db.query(Utilisateur).filter(Utilisateur.id_utilisateur==id_utilisateur)

    if not one_user.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_user.first()


def api_update_one_user(req: UtilisateurSchema, id: int, db: Session):
    user_select = db.query(Utilisateur).filter(Utilisateur.id_utilisateur==id)
    
    if not user_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    update_user = dict(req)
    update_user["updated_at"] = datetime.now()
    
    user_select.update(update_user)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_user(id: int, db: Session):
    user_select = db.query(Utilisateur).filter(Utilisateur.id_utilisateur==id)

    if not user_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    user_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }


# def active_account( db: Session):
#     select_user = db.query(Utilisateur).filter(Utilisateur.email == email).first()


# envoie du code d' activation vers l' email inscri
async def send_code(email: str, code: str):    
    html = f"""
                <div>
                    <p>Veuillez copier ce code d'activation dans le formulaire d'activation pour activer votre compte</p>
                    <br/>
                    <strong>{code}</strong>
                </div>
            """

    message = MessageSchema(
        subject="CODE D' ACTIVATION",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    try:
        response = await fm.send_message(message)
    except:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_405_METHOD_NOT_ALLOWED, detail='INTERNET_CONNECTION_NOT_AVAILABLE')
    
    return JSONResponse(content={"message": "email has been sent"})
    # print("mmmm")


# fonction permet d'activer le compte utilisateur
def activation_account(code: Code, email: str, db: Session):
    select_user = db.query(Utilisateur).filter(and_(Utilisateur.email == email, Utilisateur.code_activation == code.code_activation))
    if not select_user.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "ACTIVATION_NOT_ACCEPT"})
    select_user_up = dict(code)
    select_user_up['status_compte'] = True

    select_user.update(select_user_up)
    db.commit()

    return "COMPTE_ACTIVE"


# fonction qui permet de desactiver le compte utilisateur
def deactivate_acccount(email: str, db: Session):
    select_user_by_email = db.query(Utilisateur).filter(Utilisateur.email==email)
    if not select_user_by_email.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "EMAIL_NOT_FOUND"})
    
    select_user_by_email.update({
        'status_compte': False,
        'code_activation': str(uuid.uuid1()).upper()
    })

    db.commit()
    
    return 'ACCOUNT_DISABLE'

# fonction qui permet d'envoyer le code de réactivation du compte
async def reactive_account(email: str, db: Session):
    select_user_by_email = db.query(Utilisateur).filter(Utilisateur.email==email).first()
    if not select_user_by_email:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "EMAIL_NOT_FOUND"})
    
    response = await send_code(email, code=select_user_by_email.code_activation)

    return "EMAIL_SENT"
    

async def api_before_signup_user(req: UtilisateurSchema, db: Session):
    
    if req.nom == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "NOM"})
    if req.email == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "EMAIL"})
    if req.password == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "PASSWORD"})
    
    if is_email_exist(req.email, db):
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_406_NOT_ACCEPTABLE, detail={"erreur": "EMAIL_EXIST"})
    
    code = str(uuid.uuid1()).upper()

    new_user = Utilisateur(
        nom=req.nom,
        prenoms=req.prenoms,
        password=get_password_hash(req.password),
        email=req.email,
        status_compte=False,
        code_activation=code.upper()
    )
    try:

        response = await send_code(
            req.email,
            code=code
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='SERVER_ERROR')

    return new_user   