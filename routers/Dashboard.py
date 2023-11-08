import fastapi as _fast
import sqlalchemy.orm as _orm
import sqlalchemy.sql as _sql
from config.connexion_db import get_db


router = _fast.APIRouter(
    prefix="/api/dash",
    tags=["API DASHBOARD"]
)


@router.get('/first-data')
async def get_type_desserte(db: _orm.Session = _fast.Depends(get_db)):
    request = """
        SELECT p.nom_port,
            SUM(CASE WHEN a.type_desserte = 'CN' THEN 1 ELSE 0 END) AS CN,
            SUM(CASE WHEN a.type_desserte = 'CILC' THEN 1 ELSE 0 END) AS CILC,
            SUM(CASE WHEN a.type_desserte = 'BO' THEN 1 ELSE 0 END) AS BO,
            SUM(CASE WHEN a.type_desserte = 'CIR' THEN 1 ELSE 0 END) AS CIR
            
        FROM
            ports p
        INNER JOIN 
            accostage a ON a.id_port_accoste = p.id_port
        GROUP BY p.nom_port LIMIT 3;
    """    
    desserte_type = []
    request_exec = db.execute(_sql.text(request)).all()
    for result in request_exec:
        desserte_type.append({
            'portName': result[0],
            'data': [
                {'label': "CN", "value": result[1]},
                {'label': "CILC", "value": result[2]},
                {'label': "BO", "value": result[3]},
                {'label': "CIR", "value": result[4]},
            ]
        })

    return desserte_type


@router.get('/second-data')
async def get_tonnage(db: _orm.Session = _fast.Depends(get_db)):
    request = """
        SELECT ports.nom_port, sum(marchandises.tonnage) as tonnage
        FROM accostage, ports, marchandises WHERE accostage.id_port_accoste = ports.id_port AND accostage.id_accostage = marchandises.id_accostage_marchandise
        GROUP BY nom_port
    """
    data = []
    request_exec = db.execute(_sql.text(request))
    for result in request_exec:
        data.append({
            "name": result[0],
            "tonnage": result[1]
        })

    return data