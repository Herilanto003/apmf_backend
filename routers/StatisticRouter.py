import fastapi as _fastapi
from config.schemas import StatisticSchema, StatisticWithNavireSchema
from config.connexion_db import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text, and_
from config.models import Accostage, Navires, ResponsableNavire
import psycopg2
from datetime import datetime


router = _fastapi.APIRouter(
    tags=["API STATISTICS"],
    prefix="/api/statistic"
)


@router.post('/new')
async def new_statistic_router(req: StatisticSchema, db: Session = _fastapi.Depends(get_db)):
    try:
        # utilisation de transaction avec sqlalchemy
        with db.begin():
            # ajout pour le nouveau navire
            nouveau_navire = Navires(
                nom_navire = req.nom_navire,
                immatricule_navire = req.immatricule_navire,
                type_navire = req.type_navire,
                observation_navire = req.observation_navire,
                id_pays_navire = req.id_pays_navire
            )
            db.add(nouveau_navire)
            db.flush()

            # ajout pour le nouveau accostage
            nouveau_accost = Accostage(
                numero_escale = req.numero_escale,
                type_desserte = req.type_desserte,
                passage_embarque = req.passage_embarque,
                passage_debarque = req.passage_debarque,
                id_port_accoste = req.id_port_accost,
                date_enreg = datetime.now(),
                date_heure_arrive = req.date_heure_arrive,
                date_heure_depart = req.date_heure_depart,
                id_port_prov = req.id_port_prov,
                id_port_dest = req.id_port_dest,
                id_navire_accoste = nouveau_navire.id_navire
            )
            db.add(nouveau_accost)
            db.flush()

            # ajout pour le nouveau consignataire
            nouveau_cons = ResponsableNavire(
                nom_resp = req.nom_cons,
                role_resp = req.role_cons,
                personne = req.personne_cons,
                tel_resp = req.tel_cons,
                email_resp = req.email_cons,
                id_accoste_resp = nouveau_accost.id_accostage
            )
            db.add(nouveau_cons)
            db.flush()

            # ajout pour le nouveau armateur
            nouveau_armateur = ResponsableNavire(
                nom_resp = req.nom_armateur,
                role_resp = req.role_armateur,
                personne = req.personne_armateur,
                tel_resp = req.tel_armateur,
                email_resp = req.email_armateur,
                id_accoste_resp = nouveau_accost.id_accostage
            )
            db.add(nouveau_armateur)
            db.flush()
            
            # commit avec la base de donnée
            
            db.commit()
            db.close()
            # db.add_all([nouveau_navire, nouveau_armateur, nouveau_cons, nouveau_accost])

    except Exception as err:
        db.rollback()
        print(f"Unexpected {err=}, {type(err)=}")
        print(psycopg2.errors.UniqueViolation)
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail='REQUEST_ERR')
    return 'SUCESS'


# avec navire près-existant
@router.post('/navire-exist/new')
async def new_statistic_navire_exist_router(req: StatisticWithNavireSchema, db: Session = _fastapi.Depends(get_db)):
    try:
        # utilisation de transaction avec sqlalchemy
        with db.begin():
            # ajout pour le nouveau accostage
            nouveau_accost = Accostage(
                numero_escale = req.numero_escale,
                type_desserte = req.type_desserte,
                passage_embarque = req.passage_embarque,
                passage_debarque = req.passage_debarque,
                id_port_accoste = req.id_port_accost,
                date_enreg = datetime.now(),
                date_heure_arrive = req.date_heure_arrive,
                date_heure_depart = req.date_heure_depart,
                id_port_prov = req.id_port_prov,
                id_port_dest = req.id_port_dest,
                id_navire_accoste = req.id_navire
            )
            db.add(nouveau_accost)
            db.flush()

            # ajout pour le nouveau consignataire
            nouveau_cons = ResponsableNavire(
                nom_resp = req.nom_cons,
                role_resp = req.role_cons,
                personne = req.personne_cons,
                tel_resp = req.tel_cons,
                email_resp = req.email_cons,
                id_accoste_resp = nouveau_accost.id_accostage
            )
            db.add(nouveau_cons)
            db.flush()

            # ajout pour le nouveau armateur
            nouveau_armateur = ResponsableNavire(
                nom_resp = req.nom_armateur,
                role_resp = req.role_armateur,
                personne = req.personne_armateur,
                tel_resp = req.tel_armateur,
                email_resp = req.email_armateur,
                id_accoste_resp = nouveau_accost.id_accostage
            )
            db.add(nouveau_armateur)
            db.flush()
            
            # commit avec la base de donnée
            
            db.commit()
            db.close()
            # db.add_all([nouveau_navire, nouveau_armateur, nouveau_cons, nouveau_accost])

    except Exception as err:
        db.rollback()
        print(f"Unexpected {err=}, {type(err)=}")
        print(psycopg2.errors.UniqueViolation)
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_400_BAD_REQUEST, detail='REQUEST_ERR')
    return 'SUCESS'




@router.get('/list')
async def list_statistic_router(db: Session = _fastapi.Depends(get_db)):
    data = []
    try: 
        request = """
                    SELECT accostage.id_accostage, navires.nom_navire, navires.immatricule_navire, accostage.numero_escale, accostage.date_enreg
                    FROM accostage, navires
                    WHERE accostage.id_navire_accoste = navires.id_navire
                """        
        request_exec = db.execute(text(request)).all()
        for result in request_exec:
            data.append({
                "id": result[0],
                "nom_navire": result[1],
                "immatricule_navire": result[2],
                "numero_escale": result[3],
                "date_enreg": result[4]
            })

        for elem in data:
            request_cons = f"SELECT nom_resp FROM responsable_navire WHERE id_accoste_resp={elem['id']} AND role_resp='CONSIGNATAIRE'"
            request_cons_exec = db.execute(text(request_cons)).first()

            request_arma = f"SELECT nom_resp FROM responsable_navire WHERE id_accoste_resp={elem['id']} AND role_resp='ARMATEUR'"
            request_arma_exec = db.execute(text(request_arma)).first()
            elem['nom_cons'] = request_cons_exec[0]
            elem['nom_arma'] = request_arma_exec[0]

            print(request_cons_exec, request_arma_exec)

    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='SERVEUR_ERROR')

    return data


@router.get('/one/{id}')
async def get_one_statistic_router(id: int, db: Session = _fastapi.Depends(get_db)):
    try:
        request_navire = f"""
            SELECT * FROM accostage, navires
            WHERE accostage.id_navire_accoste = navires.id_navire AND accostage.id_accostage={id}
        """
        request_navire_exec = db.execute(text(request_navire)).all()
        navire_data = {}
        for res in request_navire_exec:
            navire_data = {
                "id": res[0],
                "numero_escale": res[1],
                "type_desserte": res[2],
                "passage_embarque": res[3],
                "passage_debarque": res[4],
                "id_navire_accoste": res[7],
                "id_port_accoste": res[8],
                "date_enreg": res[9],
                "date_heure_arrive": res[10],
                "date_heure_depart": res[11],
                "id_port_prov": res[12],
                "id_port_dest": res[13],
                "nom_navire": res[15],
                "immatricule_navire": res[16],
                "type_navire": res[17],
                "observation_navire": res[18],
                "id_pays_navire": res[19],
            }
        print(request_navire_exec)

        # obtenir le pays du navire ou le pavillon
        request_pavillon = f"SELECT nom_pays FROM pays WHERE id_pays = {navire_data['id_pays_navire']}"
        request_pavillon_exec = db.execute(text(request_pavillon)).first()
        
        # obtenir le port de accost
        request_port_accost = f"SELECT nom_port FROM ports WHERE id_port={navire_data['id_port_accoste']}"
        request_port_accost_exec = db.execute(text(request_port_accost)).first()

        # obtenir le port de provenance
        request_port_prov = f"SELECT nom_port FROM ports WHERE id_port={navire_data['id_port_prov']}"
        request_port_prov_exec = db.execute(text(request_port_prov)).first()

        # obtenir le port de destination
        request_port_dest = f"SELECT nom_port FROM ports WHERE id_port={navire_data['id_port_dest']}"
        request_port_dest_exec = db.execute(text(request_port_dest)).first()

        # obtenir le consignataire
        request_cons = f"""
            SELECT * FROM accostage, responsable_navire
            WHERE accostage.id_accostage=responsable_navire.id_accoste_resp
            AND accostage.id_accostage={id} AND responsable_navire.role_resp='CONSIGNATAIRE'
        """
        request_cons_exec = db.execute(text(request_cons)).first()
        
        # obtenir l' armateur
        request_arma = f"""
            SELECT * FROM accostage, responsable_navire
            WHERE accostage.id_accostage=responsable_navire.id_accoste_resp
            AND accostage.id_accostage={id} AND responsable_navire.role_resp='ARMATEUR'
        """
        request_arma_exec = db.execute(text(request_arma)).first()

        print(request_pavillon_exec, request_port_prov_exec, request_port_dest_exec, request_cons_exec, request_arma_exec)

        navire_data['id_pays_navire'] = request_pavillon_exec[0]
        navire_data['id_port_prov'] = request_port_prov_exec[0]
        navire_data['id_port_dest'] = request_port_dest_exec[0]
        navire_data['nom_armateur'] = request_arma_exec[15]
        navire_data['personne_armateur'] = request_arma_exec[19]
        navire_data['tel_armateur'] = request_arma_exec[20]
        navire_data['email_armateur'] = request_arma_exec[21]
        navire_data['nom_cons'] = request_arma_exec[15]
        navire_data['personne_cons'] = request_cons_exec[19]
        navire_data['tel_cons'] = request_cons_exec[20]
        navire_data['email_cons'] = request_cons_exec[21]
        navire_data['id_port_accoste'] = request_port_accost_exec[0]
        print(request_port_accost_exec)
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='SERVER_ERROR')
    
    return navire_data


@router.get('/resp/{id}/{role}')
async def get_one_resp(id: int, role: str, db: Session = _fastapi.Depends(get_db)):
    try:
        resp = db.query(ResponsableNavire).filter(and_(ResponsableNavire.id_accoste_resp==id, ResponsableNavire.role_resp==role)).first()
    except Exception as e:
        print(e)
        raise _fastapi.HTTPException(_fastapi.status.HTTP_400_BAD_REQUEST, detail='SERVER_ERROR')

    return resp