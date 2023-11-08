# importation des packages
from sqlalchemy.orm import Session
from config.models import ResponsableNavire, Navires
from config.schemas import ResponsableNavireSchema
from datetime import datetime
import fastapi as _fastapi


def create_new_pays(req: ResponsableNavireSchema, db: Session):
    # tester si les valeurs sont vides
    if req.nom_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="NOM_RESP")
    if req.adresse_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="ADRESSE_RESP")
    if req.email_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="EMAIL_RESP")
    if req.tel_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="CONTACT_RESP")
    if req.personne == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="IS_PERSON")
    if req.role_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="ROLE_RESP")
    if req.id_navire_resp == '':
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="NAVIRE_RESP")
    
    navire_exist = db.query(Navires).filter(Navires.id_continent==req.id_continent_pays)
    if not navire_exist.first():
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail="NAVIRE_NOT_EXIST")
    
    new_resp = ResponsableNavire(
        nom_resp = req.nom_resp,
        adresse_resp = req.adresse_resp,
        email_resp = req.email_resp,
        tel_resp = req.tel_resp,
        peronne = req.peronne,
        role_resp = req.role_resp,
        id_navire_resp = req.id_navire_resp
    )

    db.add(new_resp)
    db.commit()
    db.refresh(new_resp)

    return new_resp 


# def api_all_pays(db: Session):
#     all_pays = db.query(Pays).all()

#     return all_pays


# def api_one_pays(id_pays: int, db: Session):
#     one_pays = db.query(Pays).filter(Pays.id_pays==id_pays)

#     if not one_pays.first():
#         raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={"erreur": "404"})
    
#     return one_pays.first()


# def api_update_one_pays(req: ResponsableNavireSchema, id: int, db: Session):
#     pays_select = db.query(Pays).filter(Pays.id_pays==id)
    
#     if not pays_select.first():
#         raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
#     exist_continent = db.query(Continents).filter(Continents.id_continent==req.id_continent_pays)
#     if not exist_continent.first():
#         raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail={"error": "continent n' existe pas"})
    
#     update_pays = dict(req)
#     update_pays["updated_at"] = datetime.now()
    
#     pays_select.update(update_pays)
    
#     db.commit()
    
#     return {
#         'detail': {
#             'success': True
#         }
#     }


# def api_delete_one_pays(id: int, db: Session):
#     pays_select = db.query(Pays).filter(Pays.id_pays==id)

#     if not pays_select.first():
#         raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail={'message': '404'})
    
#     pays_select.delete(synchronize_session=False)

#     db.commit()

#     return {
#         'detail': {
#             'success': True
#         }
#     }