import fastapi as _fastapi
import controllers.UtilisateurController as _control
import typing as _typing
from config.schemas import UtilisateurSchema, ShowUtilisateur, Code
from config.connexion_db import get_db
from sqlalchemy.orm import Session


router = _fastapi.APIRouter(
    tags=["API UTILISATEUR"],
    prefix="/api/user"
)


@router.get('/all', response_model=_typing.List[ShowUtilisateur])
async def get_all_users(db: Session = _fastapi.Depends(get_db)):
    return _control.api_all_users(db)


@router.get('/one/{id_utilisateur}')
async def get_one_user(id_utilisateur: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_one_user(id_utilisateur, db)


@router.post('/new/{code}', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_user(req: UtilisateurSchema, code: str, db: Session = _fastapi.Depends(get_db)):
    return await _control.create_new_user(req, code, db)


@router.post('/signup', status_code=_fastapi.status.HTTP_201_CREATED)
async def signup_user(req: UtilisateurSchema, db: Session = _fastapi.Depends(get_db)):
    return await _control.api_before_signup_user(req, db)


@router.put('/edit/{id_utilisateur}')
async def update_one_user(req: UtilisateurSchema, id_utilisateur: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_user(req, id_utilisateur, db)


@router.delete('/delete/{id_utilisateur}')
async def delete_one_user(id_utilisateur: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_delete_one_user(id_utilisateur, db)


@router.post("/activate/{email}")
async def activate_account(code: Code, email: str, db: Session = _fastapi.Depends(get_db)):
    return _control.activation_account(code, email, db)


@router.post("/deactivate/{email}")
async def deactivate_account(email: str, db: Session = _fastapi.Depends(get_db)):
    return _control.deactivate_acccount(email, db)


@router.post("/refresh-account/{email}")
async def reactivation_account(email: str, db: Session = _fastapi.Depends(get_db)):
    return await _control.reactive_account(email, db)


