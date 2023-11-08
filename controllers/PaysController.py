# importation des packages
from sqlalchemy.orm import Session
from config.models import Pays, Continents
from config.schemas import PaysSchema
from datetime import datetime
import fastapi as _fastapi


def create_new_pays(req: PaysSchema, db: Session):
    if req.nom_pays == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "nom ne doit pas être vide"})
    if req.id_continent_pays == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "id continent ne doit pas être vide"})
    
    exist_continent = db.query(Continents).filter(Continents.id_continent==req.id_continent_pays)
    if not exist_continent.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "continent n' existe pas"})

    new_pays = Pays(
        nom_pays=req.nom_pays,
        id_continent_pays=req.id_continent_pays
    )

    db.add(new_pays)
    db.commit()
    db.refresh(new_pays)

    return new_pays 


def api_all_pays(db: Session):
    all_pays = db.query(Pays).all()

    return all_pays


def api_one_pays(id_pays: int, db: Session):
    one_pays = db.query(Pays).filter(Pays.id_pays==id_pays)

    if not one_pays.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_pays.first()


def api_update_one_pays(req: PaysSchema, id: int, db: Session):
    pays_select = db.query(Pays).filter(Pays.id_pays==id)
    
    if not pays_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    exist_continent = db.query(Continents).filter(Continents.id_continent==req.id_continent_pays)
    if not exist_continent.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "continent n' existe pas"})
    
    update_pays = dict(req)
    update_pays["updated_at"] = datetime.now()
    
    pays_select.update(update_pays)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_pays(id: int, db: Session):
    pays_select = db.query(Pays).filter(Pays.id_pays==id)

    if not pays_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    pays_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }