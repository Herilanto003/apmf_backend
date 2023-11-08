# importation des packages
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from config.models import Navires, Pays, Ports
from config.schemas import NavireSchema
from datetime import datetime
import fastapi as _fastapi

def create_new_port(req: NavireSchema, db: Session):
    if req.nom_navire == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'NOM_NAVIRE'})
    if req.immatricule_navire == "":
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'IM_NAVIRE'})
    if req.type_navire == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'TYPE_NAVIRE'})
    if req.id_pays_navire == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'PAVILLON'})
    if req.observation_navire == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={'erreur': 'OBS_NAVIRE'}) 
    

    # création de l'instance du navire
    try:
        new_navire = Navires(
            nom_navire=req.nom_navire,
            type_navire=req.type_navire,
            immatricule_navire=req.immatricule_navire,
            observation_navire=req.observation_navire,
            id_pays_navire=req.id_pays_navire
        )

        db.add(new_navire)
        db.commit()
        db.refresh(new_navire)
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='ERR-REQ')

    return new_navire



def api_all_navires(db: Session):
    all_navires = db.query(Navires).all()

    return all_navires


def api_one_navire(id_navire: int, db: Session):
    one_navire = db.query(Navires).filter(Navires.id_navire==id_navire)

    if not one_navire.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
    return one_navire.first()


def api_update_one_navire(req: NavireSchema, id: int, db: Session):
    navire_select = db.query(Navires).filter(Navires.id_navire==id)

    if not navire_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail='NOT_FOUND')
    
    update_navire = dict(req)
    update_navire["updated_at"] = datetime.now()
    
    try:
        navire_select.update(update_navire)
    except Exception as e: 
        print(e)
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail='ERR_RQUST')
    
    db.commit()
    
    return {
        'detail': {
            'success': True
        }
    }


def api_delete_one_navire(id: int, db: Session):
    navire_select = db.query(Navires).filter(Navires.id_navire==id)

    if not navire_select.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
    navire_select.delete(synchronize_session=False)

    db.commit()

    return {
        'detail': {
            'success': True
        }
    }


# # fonction permet de renvoyer le pays d'un port ainsi que le continent
# # def api_get_pays_port(id_port, db: Session):
# #     pays_select = db.query(Pays).join(Ports, Pays.id_pays==Ports.id_pays_port).filter(Ports.id_port==id_port)

# #     if not pays_select.first():
# #         raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
# #     return pays_select.first()


# def api_get_continent_port(id_port, db: Session):

#     request = f"""
#                     SELECT pays.nom_pays, continents.nom_continent 
#                     FROM ports, pays, continents 
#                     WHERE ports.id_pays_port=pays.id_pays 
#                     AND pays.id_continent_pays=continents.id_continent 
#                     AND ports.id_port={id_port}
#                 """
#     req = db.execute(text(request)).first()
#     print(req)
#     return {
#         'nom_pays': req[0],
#         'nom_continent': req[1]
#     }