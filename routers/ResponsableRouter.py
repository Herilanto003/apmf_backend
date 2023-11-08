import fastapi as _fastapi
import controllers.ResponsableController as _control
import typing as _typing
import config.schemas as _sm
from config.connexion_db import get_db
from sqlalchemy.orm import Session


router = _fastapi.APIRouter(
    tags=["API RESPONSABLE"],
    prefix="/api/resp"
)


# obtenir tous les responsable personne
@router.get('/all', response_model=_typing.List[_sm.ResponsableNavireSchema])
async def get_all_resp(db: Session = _fastapi.Depends(get_db)):
    return _control.api_all_resp(db)


# # obtenir tous les responsable entreprise
# @router.get('/entreprise/all', response_model=_typing.List[_sm.ShowResponsableNavireEntreprise])
# async def get_all_resp_ent(db: Session = _fastapi.Depends(get_db)):
#     return _control.api_all_resp_ent(db)


# obtenir un responsable personne
@router.get('/one/{id_resp}', response_model=_sm.ResponsableNavireSchema)
async def get_one_resp(id_resp: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_one_resp(id_resp, db)


# route pour ajouter un nouveau responsable personne
@router.post('/person/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_pays_person(req: _sm.ResponsableNavirePersonSchema, db: Session = _fastapi.Depends(get_db)):
    return _control.create_new_resp_person(req, db)


# route pour ajouter un nouveau responsable entreprise
@router.post('/entreprise/new', status_code=_fastapi.status.HTTP_201_CREATED)
async def post_new_pays_ent(req: _sm.ResponsableNavireEntrepriseSchema, db: Session = _fastapi.Depends(get_db)):
    return _control.create_new_resp_ent(req, db)


# route pour modifier un responsable person
@router.put('/person/edit/{id_resp}')
async def update_one_resp_person(req: _sm.ResponsableNavirePersonSchema, id_resp: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_resp_person(req, id_resp, db)


# route pour modifier un responsable entreprise
@router.put('/entreprise/edit/{id_resp}')
async def update_one_resp_ent(req: _sm.ResponsableNavireEntrepriseSchema, id_resp: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_update_one_resp_ent(req, id_resp, db)


# route pour supprimer un responsable soit personne ou entreprise
@router.delete('/delete/{id_resp}')
async def delete_one_resp(id_resp: int, db: Session = _fastapi.Depends(get_db)):
    return _control.api_delete_one_resp(id_resp, db)