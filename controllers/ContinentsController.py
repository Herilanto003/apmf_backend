# importation des packages
from sqlalchemy.orm import Session
from config.models import Continents
from config.schemas import ContinentSchema
from datetime import datetime
import fastapi as _fastapi


def create_new_continent(req: ContinentSchema, db: Session):
    if req.nom_continent == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "nom ne doit pas être vide"})
    
    new_continent = Continents(nom_continent=req.nom_continent)

    db.add(new_continent)
    db.commit()
    db.refresh(new_continent)

    return new_continent 


def api_all_continent(db: Session):
    all_continents = db.query(Continents).all()

    return all_continents


def api_one_continent(id_continent: int, db: Session):
    one_continent = db.query(Continents).filter(Continents.id_continent==id_continent)

    if not one_continent.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_continent.first()


def api_update_one_continent(req: ContinentSchema, id: int, db: Session):
    continent_select = db.query(Continents).filter(Continents.id_continent==id)
    
    if not continent_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    update_continent = dict(req)
    update_continent["updated_at"] = datetime.now()
    
    continent_select.update(update_continent)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_continent(id: int, db: Session):
    continent_select = db.query(Continents).filter(Continents.id_continent==id)

    if not continent_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    continent_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }