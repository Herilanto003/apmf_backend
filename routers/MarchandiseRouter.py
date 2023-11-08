import fastapi as _fastapi
import controllers.MarchandiseController as _control
import typing as _typing
from config.schemas import MarchandiseSchema2, ShowActionaireSchema2, ShowMarchandiseSchema2, MarchandiseEdit, ActionaireSchemaEdit
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_
from config.models import Actionaire, Marchandises, ResponsableNavire
from datetime import datetime


router = _fastapi.APIRouter(
    tags=["API MARCHANDISE"],
    prefix="/api/marchandise"
)


# @router.get('/all', response_model=_typing.List[ShowMarchandise])
# async def get_all_marchandise(db: Session = _fastapi.Depends(get_db)):
#     return _control.api_all_marchandise(db)


# @router.get('/one/{id_marchandise}')
# async def get_one_marchandise(id_marchandise: int, db: Session = _fastapi.Depends(get_db)):
#     return _control.api_one_marchandise(id_marchandise, db)


# @router.post('/new', status_code=_fastapi.status.HTTP_201_CREATED)
# async def post_new_marchandise(req: MarchandiseSchema, db: Session = _fastapi.Depends(get_db)):
#     return _control.create_new_marchandise(req, db)

# @router.put('/edit/{id_marchandise}')
# async def update_one_marchandise(req: MarchandiseSchema, id_marchandise: int, db: Session = _fastapi.Depends(get_db)):
#     return _control.api_update_one_marchandise(req, id_marchandise, db)


# @router.delete('/delete/{id_marchandise}')
# async def delete_one_marchandise(id_marchandise: int, db: Session = _fastapi.Depends(get_db)):
#     return _control.api_delete_one_marchandise(id_marchandise, db)

@router.post('/new')
async def post_new_marchandise(req: MarchandiseSchema2, db: Session = _fastapi.Depends(get_db)):
    try:
        with db.begin():
            nouveau_act = Actionaire(
                nom_act = req.nom_act,
                adresse_act = req.adresse_act,
                tel_act = req.tel_act,
                email_act = req.email_act,
                personne = req.personne,
                role = req.role_act
            )
            db.add(nouveau_act)
            db.flush()

            nouveau_marchandise = Marchandises(
                nature_marchandise = req.nature_marchandise,
                tonnage = req.tonnage,
                caractere = req.caractere,
                conditionnement = req.conditionnement,
                nombre = req.nombre,
                observation_marchandise = req.observation_marchandise,
                id_accostage_marchandise = req.id_accostage_marchandise,
                nom_operation = req.nom_operation,
                type_operation = req.type_operation,
                id_port_march = req.id_port_march,
                type_marchandise = req.type_marchandise,
                id_act_marchandise = nouveau_act.id_actionaire 
            )
            db.add(nouveau_marchandise)
            db.flush()

            nouveau_manu = ResponsableNavire(
                nom_resp = req.nom_manu,
                role_resp = req.role_manu,
                tel_resp = req.tel_manu,
                email_resp = req.email_mau,
                personne = req.peronne_manu,
                id_accoste_resp = nouveau_marchandise.id_accostage_marchandise
            )
            db.add(nouveau_manu)
            db.flush()

            db.commit() 
            db.close()

    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='ERR_REQUEST')

    return 'SUCCESS'


@router.get('/all')
async def get_all_marchandise(db: Session = _fastapi.Depends(get_db)):
    marchandises = db.query(Marchandises).all()
    actionaires = db.query(Actionaire).all()

    return {
        "marchandises": marchandises,
        "actionaires": actionaires
    }


@router.get('/one/act/{id_act}', response_model=ShowActionaireSchema2)
async def get_one_actionaire(id_act: int, db: Session = _fastapi.Depends(get_db)):
    select_act = db.query(Actionaire).filter(Actionaire.id_actionaire == id_act).first()

    if not select_act:
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    
    return select_act


@router.get('/one/{id_march}', response_model=ShowMarchandiseSchema2)
async def get_one_marchandise(id_march: int, db: Session = _fastapi.Depends(get_db)):
    select_march = db.query(Marchandises).filter(Marchandises.id_marchandise == id_march).first()

    if not select_march:
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')

    return select_march


@router.delete('/delete/one/{id_march}')
async def delete_one_marchandise(id_march: int, db: Session = _fastapi.Depends(get_db)):
    select_march = db.query(Marchandises).filter(Marchandises.id_marchandise == id_march)
    select_march_first = select_march.first()

    if not select_march.first():
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')

    select_manu = db.query(ResponsableNavire).filter(and_(ResponsableNavire.id_accoste_resp==select_march_first.id_accostage_marchandise, ResponsableNavire.role_resp=='MANUTENTIONAIRE'))

    select_manu.delete(synchronize_session=False)
    select_march.delete(synchronize_session=False)
    db.commit()

    return "SUCCESS"


@router.put('/edit/one/{id_march}')
async def update_one_marchandise(req: MarchandiseEdit, id_march: int, db: Session = _fastapi.Depends(get_db)):
    select_march = db.query(Marchandises).filter(Marchandises.id_marchandise == id_march)

    if not select_march.first():
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    
    select_act = db.query(Actionaire).filter(Actionaire.id_actionaire == select_march.first().id_act_marchandise)

    try:

        if req.nom_operation == 'SORTIE':
            select_act.update({
                'updated_at': datetime.now(),
                'role': 'EXPORTATEUR'
            })
            print('EXPORTATEUR')
        if req.nom_operation == 'ENTREE':
            select_act.update({
                'updated_at': datetime.now(),
                'role': 'DESTINATAIRE'
            })
            print('DESTINATAIRE')

        maj_march = dict(req)
        maj_march['updated_at'] = datetime.now()
        select_march.update(maj_march)
        db.commit()
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='REQUEST_ERROR')

    return "SUCCESS"


@router.post('/new/exist-act')
async def create_marchandise_exist_act(req: MarchandiseEdit, db: Session = _fastapi.Depends(get_db)):
    try:
        new_march = Marchandises(
            nature_marchandise = req.nature_marchandise,
            tonnage = req.tonnage,
            type_marchandise = req.type_marchandise,
            caractere = req.caractere,
            conditionnement = req.conditionnement,
            nombre = req.nombre,
            observation_marchandise = req.observation_marchandise,
            id_accostage_marchandise = req.id_accostage_marchandise,
            id_act_marchandise = req.id_act_marchandise,
            nom_operation = req.nom_operation,
            type_operation = req.type_operation,
            id_port_march = req.id_port_march
        )
        db.add(new_march)
        db.commit()

    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='REQUEST_ERROR')
    
    return "SUCCESS"


# pour l' actionnaire
@router.post('/actionaire/new')
async def create_new_acitonaire(req: ActionaireSchemaEdit, db: Session = _fastapi.Depends(get_db)):
    try:
        new_actionaire = Actionaire(
            nom_act = req.nom_act,
            adresse_act = req.adresse_act,
            tel_act = req.tel_act,
            email_act = req.email_act,
            personne = req.personne,
            role = req.role
        )
        db.add(new_actionaire)
        db.commit()
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='REQUEST_ERROR')
    
    return 'SUCCESS'


@router.put('/edit/one-act/{id_act}')
async def update_one_act(req: ActionaireSchemaEdit, id_act: int, db: Session = _fastapi.Depends(get_db)):
    select_act = db.query(Actionaire).filter(Actionaire.id_actionaire == id_act)

    if not select_act.first():
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    
    try:
        update_act = dict(req)
        update_act['updated_at'] = datetime.now()
        select_act.update(update_act)
        db.commit()
    except Exception as e: 
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='REQUEST_ERROR')
    
    return 'SUCCESS'


@router.delete('/delete/one-act/{id_act}')
async def delete_one_act(id_act: int, db: Session = _fastapi.Depends(get_db)):
    select_act = db.query(Actionaire).filter(Actionaire.id_actionaire == id_act)

    if not select_act.first():
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail="NOT_FOUND")
    
    select_act.delete(synchronize_session=False)
    db.commit()

    return "SUCCESS"


