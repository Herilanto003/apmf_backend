# importation des packages
from sqlalchemy.orm import Session
from config.models import Marchandises, Accostage, Actionaire, Ports
from config.schemas import MarchandiseSchema
from datetime import datetime
import fastapi as _fastapi


def create_new_marchandise(req: MarchandiseSchema, db: Session):
    if req.nature_marchandise == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "NATURE"})
    if req.tonnage == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "TONNAGE"})
    if req.type_marchandise == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "TYPE_M"})
    if req.nombre == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "QTE"})
    if req.observation_marchandise == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "OBSERVATION"})
    if req.id_accostage_marchandise == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "ACCOSTE"})
    if req.id_act_marchandise == 0:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "ACT"})
    if req.nom_operation == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "OPERATION"})
    if req.type_operation == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"erreur": "TYPE_OPERATION"})

    # si accostage existe
    exist_accostage = db.query(Accostage).filter(Accostage.id_accostage==req.id_accostage_marchandise).first()
    if not exist_accostage:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "ACCOSTAGE_NOT_EXIST"})
    
    # si les ports dest et prov existent
    exist_port = db.query(Ports).filter(Ports.id_port==req.id_port_march).first()
    if not exist_port:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "PORT_DEST_NOT_EXIST"})
    
    # exist_port_prov = db.query(Ports).filter(Ports.id_port==req.id_port_prov).first()
    # if not exist_port_prov:
    #     raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "PORT_PROV_NOT_EXIST"})
    
    # si l'actionaire existe
    exist_act = db.query(Actionaire).filter(Actionaire.id_actionaire==req.id_act_marchandise).first()
    if not exist_act:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "ACTIONAIRE_NOT_EXIST"})
    
    new_marchandise = Marchandises(
        nature_marchandise=req.nature_marchandise,
        type_marchandise=req.type_marchandise,
        observation_marchandise=req.observation_marchandise,
        nombre=req.nombre,
        caractere=req.caractere,
        conditionnement=req.conditionnement,
        nom_operation=req.nom_operation,
        type_operation=req.type_operation,
        tonnage=req.tonnage,
        id_port_march=req.id_port_march,
        id_act_marchandise=req.id_act_marchandise,
        id_accostage_marchandise=req.id_accostage_marchandise
    )

    db.add(new_marchandise)
    db.commit()
    db.refresh(new_marchandise)

    return new_marchandise 


def api_all_marchandise(db: Session):
    all_marchandise = db.query(Marchandises).all()

    return all_marchandise


def api_one_marchandise(id_marchandise: int, db: Session):
    one_marchandise = db.query(Marchandises).filter(Marchandises.id_marchandise==id_marchandise)

    if not one_marchandise.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_marchandise.first()


def api_update_one_marchandise(req: MarchandiseSchema, id: int, db: Session):
    marchandise_select = db.query(Marchandises).filter(Marchandises.id_marchandise==id)
    
    if not marchandise_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    # si accostage existe
    exist_accostage = db.query(Accostage).filter(Accostage.id_accostage==req.id_accostage_marchandise).first()
    if not exist_accostage:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "ACCOSTAGE_NOT_EXIST"})
    
    # si les ports dest et prov existent
    exist_port = db.query(Ports).filter(Ports.id_port==req.id_port_march).first()
    if not exist_port:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "PORT_DEST_NOT_EXIST"})
    
    # si l'actionaire existe
    exist_act = db.query(Actionaire).filter(Actionaire.id_actionaire==req.id_act_marchandise).first()
    if not exist_act:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "ACTIONAIRE_NOT_EXIST"})
    
    update_marchandise = dict(req)
    update_marchandise["updated_at"] = datetime.now()
    
    marchandise_select.update(update_marchandise)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_marchandise(id: int, db: Session):
    marchandise_select = db.query(Marchandises).filter(Marchandises.id_marchandise==id)

    if not marchandise_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    marchandise_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }