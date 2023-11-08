import fastapi as _fastapi
import controllers.PortController as _control
import typing as _typing
from config.schemas import PortSchema, ShowPort, ShowPortSchema, UtilisateurToken
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from config.auth.token import get_current_active_user


router = _fastapi.APIRouter(
    tags=["API PORT"],
    prefix="/api/port"
)


@router.get('/all', response_model=_typing.List[ShowPortSchema])
async def get_all_port(db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_all_ports(db)


@router.get('/one/{id_port}')
async def get_one_port(id_port: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_one_port(id_port, db)


@router.post('/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_port(req: PortSchema, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.create_new_port(req, db)

@router.put('/edit/{id_port}')
async def update_one_port(req: PortSchema, id_port: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_update_one_port(req, id_port, db)


@router.delete('/delete/{id_port}')
async def delete_one_port(id_port: int, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_delete_one_port(id_port, db)


# @router.get('/pays/{id_port}')
# async def get_pays_of_port(id_port, db: Session = _fastapi.Depends(get_db)):
#     return _control.api_get_pays_port(id_port, db)


@router.get('/pays-continent/{id_port}')
async def get_pays_of_port(id_port, db: Session = _fastapi.Depends(get_db), user: UtilisateurToken = _fastapi.Depends(get_current_active_user)):
    return _control.api_get_continent_port(id_port, db)

