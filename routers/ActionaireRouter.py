import fastapi as _fastapi
import controllers.ActionaireController as _control
import typing as _typing
from config.schemas import ActionaireSchema, ShowActionaire, ActionairePersonSchema, ActionaireEntrepriseSchema, ShowActionaireEntreprise, ShowActionairePerson
from config.connexion_db import get_db
from sqlalchemy.orm import Session


router = _fastapi.APIRouter(
    tags=["API ACTIONAIRE"],
    prefix="/api/actionaire"
)


@router.get('/person/all', response_model=_typing.List[ShowActionairePerson])
async def get_all_actionaire(db: Session = _fastapi.Depends(get_db)):
    return _control.api_all_actionaire(db)


@router.get('/person/one/{id_actionaire}', response_model=ShowActionairePerson)
async def get_one_actionaire(id_actionaire: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_one_actionaire(id_actionaire, db)


@router.get('/entreprise/all', response_model=_typing.List[ShowActionaireEntreprise])
async def get_all_actionaire(db: Session = _fastapi.Depends(get_db)):
    return _control.api_all_actionaire_ent(db)


@router.get('/entreprise/one/{id_actionaire}', response_model=ShowActionaireEntreprise)
async def get_one_actionaire(id_actionaire: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_one_actionaire_ent(id_actionaire, db)


@router.post('/person/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_actionaire_person(req: ActionairePersonSchema, db: Session = _fastapi.Depends(get_db)):
    return _control.create_new_actionaire_person(req, db)


@router.post('/entreprise/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_actionaire_entreprise(req: ActionaireEntrepriseSchema, db: Session = _fastapi.Depends(get_db)):
    return _control.create_new_actionaire_entreprise(req, db)


@router.put('/person/edit/{id_actionaire}')
async def update_one_actionaire(req: ActionairePersonSchema, id_actionaire: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_actionaire_person(req, id_actionaire, db)


@router.put('/entreprise/edit/{id_actionaire}')
async def update_one_actionaire(req: ActionaireEntrepriseSchema, id_actionaire: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_actionaire_entreprise(req, id_actionaire, db)


@router.delete('/delete/{id_actionaire}')
async def delete_one_actionaire(id_actionaire: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_delete_one_actionaire(id_actionaire, db)