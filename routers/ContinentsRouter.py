import fastapi as _fastapi
import controllers.ContinentsController as _control
import typing as _typing
from config.schemas import ContinentSchema, ShowContinent
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from config.schemas import ShowContinent


router = _fastapi.APIRouter(
    tags=["API CONTINENT"],
    prefix="/api/continent"
)


@router.get('/all', response_model=_typing.List[ShowContinent])
async def get_all_continents(db: Session = _fastapi.Depends(get_db)):
    return _control.api_all_continent(db)


@router.get('/one/{id_continent}')
async def get_one_continent(id_continent: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_one_continent(id_continent, db)


@router.post('/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_continent(req: ContinentSchema, db: Session = _fastapi.Depends(get_db)):
    return _control.create_new_continent(req, db)


@router.put('/edit/{id_continent}')
async def update_one_continent(req: ContinentSchema, id_continent: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_continent(req, id_continent, db)


@router.delete('/delete/{id_continent}')
async def delete_one_continent(id_continent: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_delete_one_continent(id_continent, db)