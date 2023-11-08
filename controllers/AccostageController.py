# importation des packages
from sqlalchemy.orm import Session
from config.models import Accostage, Ports, Navires
from config.schemas import AccostageSchema
from datetime import datetime
import fastapi as _fastapi


def create_new_accostage(req: AccostageSchema, db: Session):
    if req.numero_escale == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NUM_ESCALE'})
    if req.type_desserte == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'TYPE_DESSERTE'})
    if req.date_heure_arrive == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'DATE_ARRIVE'})
    if req.date_heure_depart == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'DATE_DEPART'})
    if req.id_port_accoste == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PORT_ACCOSTE'})
    if req.id_navire_accoste == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NAVIRE_ACCOSTE'})
    if req.date_enreg == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'DATE_ENREG'})
    if req.passage_debarque == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PASSAGE_DEBARQUE'})
    if req.passage_embarque == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PASSAGE_EMBARQUE'})
    if req.id_port_prov == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PASSAGE_EMBARQUE'})
    if req.id_port_dest == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PASSAGE_EMBARQUE'})
    
    # vérifier si le port existe ou pas
    exist_port = db.query(Ports).filter(Ports.id_port==req.id_port_accoste).first()
    if not exist_port:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'erreur': 'PORT_NOT_EXIST'})     

    # vérifier si le navire existe ou pas
    exist_navire = db.query(Navires).filter(Navires.id_navire==req.id_navire_accoste).first()
    if not exist_navire:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NAVIRE_NOT_EXIST'}) 

    new_accoste = Accostage(
        numero_escale=req.numero_escale,
        type_desserte=req.type_desserte,
        passage_embarque=req.passage_embarque,
        passage_debarque=req.passage_debarque,
        date_enreg=req.date_enreg,
        date_heure_arrive=req.date_heure_arrive,
        date_heure_depart=req.date_heure_depart,
        id_navire_accoste=req.id_navire_accoste,
        id_port_accoste=req.id_port_accoste,
        id_port_porv=req.id_port_prov,
        id_port_dest=req.id_port_dest,
    )

    db.add(new_accoste)
    db.commit()
    db.refresh(new_accoste)

    return new_accoste


def api_all_accostage(db: Session):
    all_accostage = db.query(Accostage).all()

    return all_accostage


def api_one_accostage(id_accostage: int, db: Session):
    one_accostage = db.query(Accostage).filter(Accostage.id_accostage==id_accostage)

    if not one_accostage.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_accostage.first()


def api_update_one_accostage(req: AccostageSchema, id: int, db: Session):
    accostage_select = db.query(Accostage).filter(Accostage.id_accostage==id)

    if req.numero_escale == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NUM_ESCALE'})
    if req.type_desserte == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'TYPE_DESSERTE'})
    if req.date_heure_arrive == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'DATE_ARRIVE'})
    if req.date_heure_depart == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'DATE_DEPART'})
    if req.id_port_accoste == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PORT_ACCOSTE'})
    if req.id_navire_accoste == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NAVIRE_ACCOSTE'})
    if req.date_enreg == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'DATE_ENREG'})
    if req.passage_debarque == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PASSAGE_DEBARQUE'})
    if req.passage_embarque == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PASSAGE_EMBARQUE'})
    
    if not accostage_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    # vérifier si le port existe ou pas
    exist_port = db.query(Ports).filter(Ports.id_port==req.id_port_accoste).first()
    if not exist_port:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'erreur': 'PORT_NOT_EXIST'})     

    # vérifier si le navire existe ou pas
    exist_navire = db.query(Navires).filter(Navires.id_navire==req.id_navire_accoste).first()
    if not exist_navire:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NAVIRE_NOT_EXIST'}) 
    
    update_accostage = dict(req)
    update_accostage["updated_at"] = datetime.now()
    
    accostage_select.update(update_accostage)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_accostage(id: int, db: Session):
    accostage_select = db.query(Accostage).filter(Accostage.id_accostage==id)

    if not accostage_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    accostage_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }