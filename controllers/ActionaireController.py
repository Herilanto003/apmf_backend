# importation des packages
from sqlalchemy.orm import Session
from config.models import Actionaire
from config.schemas import ActionaireSchema, ActionaireEntrepriseSchema, ActionairePersonSchema
from datetime import datetime
import fastapi as _fastapi


# si actionaire est une personne
def create_new_actionaire_person(req: ActionairePersonSchema, db: Session):
    if req.role == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "ROLE"})

    new_actionaire_person = Actionaire(
        role=req.role,
        personne=True,
        nom_act=req.nom_act,
        prenoms_act=req.prenoms_act,
        adresse_act=req.adresse_act,
        cin_act=req.cin_act,
        contact_act=req.contact_act,
        adresse_email_act=req.adresse_email_act
    )

    db.add(new_actionaire_person)
    db.commit()
    db.refresh(new_actionaire_person)

    return new_actionaire_person 


def create_new_actionaire_entreprise(req: ActionaireEntrepriseSchema, db: Session):
    if req.role == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "ROLE"})

    new_actionaire_entreprise = Actionaire(
        role=req.role,
        personne=False,
        nom_ent_act=req.nom_ent_act,
        localisation_ent_act=req.localisation_ent_act,
        email_ent_act=req.email_ent_act,
    )

    db.add(new_actionaire_entreprise)
    db.commit()
    db.refresh(new_actionaire_entreprise)

    return new_actionaire_entreprise 


def api_all_actionaire(db: Session):
    all_actionaire = db.query(Actionaire).all()

    return all_actionaire


def api_all_actionaire_ent(db: Session):
    all_actionaire = db.query(Actionaire).all()

    return all_actionaire


def api_one_actionaire(id_actionaire: int, db: Session):
    one_actionaire = db.query(Actionaire).filter(Actionaire.id_actionaire==id_actionaire)

    if not one_actionaire.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_actionaire.first()


def api_one_actionaire_ent(id_actionaire: int, db: Session):
    one_actionaire = db.query(Actionaire).filter(Actionaire.id_actionaire==id_actionaire)

    if not one_actionaire.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_actionaire.first()


def api_update_one_actionaire_person(req: ActionairePersonSchema, id: int, db: Session):
    actionaire_select = db.query(Actionaire).filter(Actionaire.id_actionaire==id)
    
    if not actionaire_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    update_pays = dict(req)
    update_pays["updated_at"] = datetime.now()
    
    actionaire_select.update(update_pays)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_update_one_actionaire_entreprise(req: ActionaireEntrepriseSchema, id: int, db: Session):
    actionaire_select = db.query(Actionaire).filter(Actionaire.id_actionaire==id)
    
    if not actionaire_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    update_pays = dict(req)
    update_pays["updated_at"] = datetime.now()
    
    actionaire_select.update(update_pays)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_actionaire(id: int, db: Session):
    actionaire_select = db.query(Actionaire).filter(Actionaire.id_actionaire==id)

    if not actionaire_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    actionaire_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }