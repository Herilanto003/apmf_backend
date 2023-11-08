import fastapi as _fastapi
import controllers.AccostageController as _control
import typing as _typing
from config.schemas import AccostageSchema, ShowAccostage
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from config.schemas import ShowAccostage


router = _fastapi.APIRouter(
    tags=["API ACCOSTAGE"],
    prefix="/api/accostage"
)


@router.get('/all', response_model=_typing.List[ShowAccostage])
async def get_all_accostage(db: Session = _fastapi.Depends(get_db)):
    return _control.api_all_accostage(db)


@router.get('/one/{id_accostage}')
async def get_one_accostage(id_accostage: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_one_accostage(id_accostage, db)


@router.post('/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_accostage(req: AccostageSchema, db: Session = _fastapi.Depends(get_db)):
    return _control.create_new_accostage(req, db)

@router.put('/edit/{id_accostage}')
async def update_one_accostage(req: AccostageSchema, id_accostage: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_accostage(req, id_accostage, db)


@router.delete('/delete/{id_accostage}')
async def delete_one_accostage(id_accostage: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_delete_one_accostage(id_accostage, db)