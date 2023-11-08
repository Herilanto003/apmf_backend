import fastapi as _fastapi
import controllers.PaysController as _control
import typing as _typing
from config.schemas import PaysSchema, ShowPays, UtilisateurToken
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from config.auth.token import get_current_active_user


router = _fastapi.APIRouter(
    tags=["API PAYS"],
    prefix="/api/pays"
)


@router.get('/all', response_model=_typing.List[ShowPays])
async def get_all_pays(db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_all_pays(db)


@router.get('/one/{id_pays}')
async def get_one_pays(id_pays: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_one_pays(id_pays, db)


@router.post('/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_pays(req: PaysSchema, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.create_new_pays(req, db)

@router.put('/edit/{id_pays}')
async def update_one_pays(req: PaysSchema, id_pays: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_update_one_pays(req, id_pays, db)


@router.delete('/delete/{id_pays}')
async def delete_one_pays(id_pays: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_delete_one_pays(id_pays, db)