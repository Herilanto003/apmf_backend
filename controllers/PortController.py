# importation des packages
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from config.models import Ports, Pays, Continents
from config.schemas import PortSchema
from datetime import datetime
import fastapi as _fastapi


def create_new_port(req: PortSchema, db: Session):
    if req.nom_port == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "nom ne doit pas être vide"})
    if req.apmf == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "interdit vide"})
    if req.id_pays_port == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "interdit vide"})
    if req.status == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "interdit vide"})
    
    exist_pays = db.query(Pays).filter(Pays.id_pays==req.id_pays_port)
    if not exist_pays.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "pays n' existe pas"})

    new_port = Ports(
        nom_port=req.nom_port,
        apmf=req.apmf,
        id_pays_port=req.id_pays_port,
        status=req.status
    )

    db.add(new_port)
    db.commit()
    db.refresh(new_port)

    return new_port 


def api_all_ports(db: Session):
    all_ports = db.query(Ports).all()

    return all_ports


def api_one_port(id_port: int, db: Session):
    one_port = db.query(Ports).filter(Ports.id_port==id_port)

    if not one_port.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_port.first()


def api_update_one_port(req: PortSchema, id: int, db: Session):
    port_select = db.query(Ports).filter(Ports.id_port==id)
    
    if not port_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    exist_pays = db.query(Pays).filter(Pays.id_pays==req.id_pays_port)
    if not exist_pays.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "pays n' existe pas"})
    
    update_port = dict(req)
    update_port["updated_at"] = datetime.now()
    
    port_select.update(update_port)
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_port(id: int, db: Session):
    port_select = db.query(Ports).filter(Ports.id_port==id)

    if not port_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    port_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }


# fonction permet de renvoyer le pays d'un port ainsi que le continent
# def api_get_pays_port(id_port, db: Session):
#     pays_select = db.query(Pays).join(Ports, Pays.id_pays==Ports.id_pays_port).filter(Ports.id_port==id_port)

#     if not pays_select.first():
#         raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
#     return pays_select.first()


def api_get_continent_port(id_port, db: Session):

    request = f"""
                    SELECT pays.nom_pays, continents.nom_continent 
                    FROM ports, pays, continents 
                    WHERE ports.id_pays_port=pays.id_pays 
                    AND pays.id_continent_pays=continents.id_continent 
                    AND ports.id_port={id_port}
                """
    req = db.execute(text(request)).first()
    print(req)
    return {
        'nom_pays': req[0],
        'nom_continent': req[1]
    }