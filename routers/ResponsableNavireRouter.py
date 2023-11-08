import fastapi as _fastapi
import controllers.ResponsableNavireController as _control
import typing as _typing
from config.schemas import ResponsableNavireSchema, ShowRepsonsableNavire
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from config.models import ResponsableNavire
from datetime import datetime


router = _fastapi.APIRouter(
    tags=["API RESPONSABLE NAVIRE "],
    prefix="/api/resp-navire"
)


@router.get('/one/{id_resp}')
async def get_one_resp(id_resp: int, db: Session = _fastapi.Depends(get_db)):
    select_resp = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id_resp).first()

    if not select_resp:
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')

    return select_resp


@router.put('/edit/{id_resp}')
async def update_one_resp(req: ResponsableNavireSchema, id_resp: int, db: Session = _fastapi.Depends(get_db)):
    select_resp = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id_resp)

    if not select_resp.first():
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    
    update_resp = dict(req)
    update_resp['updated_at'] = datetime.now()

    try:
        select_resp.update(update_resp)
        db.commit()
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='ERR_RQST')

    return "SUCCESS"


@router.delete('/delete/{id_resp}')
async def delete_one_resp(id_resp: int, db: Session = _fastapi.Depends(get_db)):
    select_resp = db.query(ResponsableNavire).filter(ResponsableNavire.id_resp==id_resp)

    if not select_resp.first():
        raise _fastapi.HTTPException(_fastapi.status.HTTP_404_NOT_FOUND, detail='NOT_FOUND')
    
    try:
        select_resp.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='ERR_RQST')
    
    return "delete resp"


@router.get('/all')
async def get_all_resp(db: Session = _fastapi.Depends(get_db)):
    resp = db.query(ResponsableNavire).all()

    return resp