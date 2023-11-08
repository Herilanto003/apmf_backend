import fastapi as _fast
import fastapi.responses as _resp
import sqlalchemy.orm as _orm
import sqlalchemy.sql as _sql
from config.schemas import RapportSchema

def api_download_rapport(db: _orm.Session):
    req_sql = f"""
                SELECT p.nom_port,
                    EXTRACT('MONTH' FROM a.date_heure_arrive) AS mois,
                    SUM(CASE WHEN a.type_desserte = 'ci' THEN 1 ELSE 0 END) AS "total_ci",
                    SUM(CASE WHEN a.type_desserte = 'cir' THEN 1 ELSE 0 END) AS total_cir,
                    SUM(CASE WHEN a.type_desserte = 'bo' THEN 1 ELSE 0 END) AS total_bo,
                    SUM(CASE WHEN a.type_desserte = 'cr' THEN 1 ELSE 0 END) AS total_cr,
                    COUNT(*) AS total_general
                FROM
                    ports p
                INNER JOIN 
                    accostage a ON a.id_port_accoste = p.id_port
                WHERE (a.date_heure_arrive BETWEEN '2023-9-23' AND '2023-10-23')
                    OR (a.date_heure_arrive BETWEEN '2023-10-23' AND '2023-11-23')
                GROUP BY p.nom_port, mois;           
            """
    # execution de la requete sql
    # port - mois - CI - CIR - BO - CR - TOTAL
    """
        [
            {
                "lieux" : "Toliara",
                "type_desserte" : ["ci", "cir", "cr, "bo", "Total"],
                "mois_1" : [16, 8, 0, 0, 0],
                "mois_2" : [16, 8, 0, 0, 0],
                "mois_3" : [16, 8, 0, 0, 0],
                "observation" : "obs erv ation"
            }
        ]
    """
    all_data = []
    req_exec = db.execute(_sql.text(req_sql)).all()
    # enregistrement
    for result in req_exec:
        all_data.append(
            {
                "port": result[0],
                "type_desserte": ["CI", "cIR", "cr", "BO", "Total"],
                "mois_1": {
                    "titre": result[1],
                    "nombre": [result[2], result[3], result[4], result[5], result[6]]
                }
            } 
        )
    print(req_exec)
    return all_data