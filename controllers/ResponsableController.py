# importation des packages
from sqlalchemy.orm import Session
from config.models import ResponsableNavire, Navires
from datetime import datetime
import fastapi as _fastapi
import config.schemas as _sm


# création d'un responsable personne
def create_new_resp_person(req: _sm.ResponsableNavireSchema, db: Session):
    if req.role_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "ROLE_resp_RESP"})
    if req.nom_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "NOM_RESP"})
    if req.adresse_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "ADR_RESP"})
    if req.tel_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "TEL_RESP"})
    if req.email_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "EMAIL_RESP"})
    
    # vérifier le navire s'il existe
    exist_navire = db.query(Navires).filter(Navires.id_navire==req.id_navire_resp).first()
    if not exist_navire:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'erreur': "NAVIRE_NOT_EXIST"})
    
    new_resp = ResponsableNavire(
        role_resp=req.role_resp,
        nom_resp=req.nom_resp,
        adresse_resp=req.adresse_resp,
        tel_resp=req.tel_resp,
        email_resp=req.email_resp,
        personne=req.personne
    )

    db.add(new_resp)
    db.commit()
    db.refresh(new_resp)

    return new_resp 


# création d'un responsable entreprise
def create_new_resp_ent(req: _sm.ResponsableNavireEntrepriseSchema, db: Session):
    if req.role_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "ROLE_resp_RESP"})
    if req.nom_ent_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "NOM_ENT_RESP"})
    if req.localisation_ent_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "LOCALISATION_RESP"})
    if req.email_ent_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "EMAIL_ENT_RESP"})
    if req.id_navire_resp == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': "ID_NAVIRE"})
    
    # vérifier le navire s'il existe
    exist_navire = db.query(Navires).filter(Navires.id_navire==req.id_navire_resp).first()
    if not exist_navire:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'erreur': "NAVIRE_NOT_EXIST"})
    
    new_resp = ResponsableNavire(
        role_resp=req.role_resp,
        nom_ent_resp=req.nom_ent_resp,
        localisation_ent_resp=req.localisation_ent_resp,
        email_ent_resp=req.email_ent_resp,
        id_navire_resp=req.id_navire_resp,
        personne=False
    )

    db.add(new_resp)
    db.commit()
    db.refresh(new_resp)

    return new_resp 


# api pour les responsable personne
def api_all_resp(db: Session):
    all_resp = db.query(ResponsableNavire).all()

    return all_resp


def api_one_resp(id_resp: int, db: Session):
    one_resp = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id_resp)

    if not one_resp.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_resp.first()


def api_update_one_resp_ent(req: _sm.ResponsableNavireEntrepriseSchema, id: int, db: Session):
    resp_select = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id)
    
    if not resp_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    # vérifier le navire s'il existe
    exist_navire = db.query(Navires).filter(Navires.id_navire==req.id_navire_resp).first()
    if not exist_navire:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'erreur': "NAVIRE_NOT_EXIST"})
    
    update_resp = dict(req)
    update_resp["updated_at"] = datetime.now()
    
    resp_select.update(update_resp)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_update_one_resp_person(req: _sm.ResponsableNavirePersonSchema, id: int, db: Session):
    resp_select = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id)
    
    if not resp_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    # vérifier le navire s'il existe
    exist_navire = db.query(Navires).filter(Navires.id_navire==req.id_navire_resp).first()
    if not exist_navire:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'erreur': "NAVIRE_NOT_EXIST"})
    
    update_resp = dict(req)
    update_resp["updated_at"] = datetime.now()
    
    resp_select.update(update_resp)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_resp(id: int, db: Session):
    resp_select = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id)

    if not resp_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    resp_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }