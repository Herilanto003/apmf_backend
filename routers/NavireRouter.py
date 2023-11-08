import fastapi as _fastapi
import controllers.NavireController as _control
import typing as _typing
from config.schemas import NavireSchema, ShowNavire, UtilisateurToken
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from config.auth.token import get_current_active_user


router = _fastapi.APIRouter(
    tags=["API NAVIRE"],
    prefix="/api/navire"
)


@router.get('/all', response_model=_typing.List[ShowNavire])
async def get_all_navire(db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_all_navires(db)


@router.get('/one/{id_navire}')
async def get_one_port(id_navire: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_one_navire(id_navire, db)


@router.post('/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_navire(req: NavireSchema, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.create_new_port(req, db)

@router.put('/edit/{id_navire}')
async def update_one_navire(req: NavireSchema, id_navire: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_update_one_navire(req, id_navire, db)


@router.delete('/delete/{id_navire}')
async def delete_one_navire(id_navire: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_delete_one_navire(id_navire, db)


# @router.get('/pays/{id_navire}')
# async def get_pays_of_navire(id_navire, db: Session = _fastapi.Depends(get_db)):
#     return _control.api_get_pays_navire(id_navire, db)


# @router.get('/pays-continent/{id_navire}')
# async def get_pays_of_navire(id_navire, db: Session = _fastapi.Depends(get_db)):
#     return "_control.api_get_continent_navire(id_navire, db)"

