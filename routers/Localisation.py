import fastapi as _fast
import sqlalchemy.orm as _orm
import sqlalchemy.sql as _sql
from config.connexion_db import get_db
from geopy.geocoders import Nominatim


router = _fast.APIRouter(
    prefix="/api/localization",
    tags=["API LOCALIZATION"]
)


@router.get('/all')
async def get_all_position(db: _orm.Session = _fast.Depends(get_db)):
    geolocator = Nominatim(user_agent="MyApp")
    data_position = []

    request = "SELECT nom_port FROM ports WHERE apmf = true"

    request_exec = db.execute(_sql.text(request))

    for result in request_exec:
        try:
            location = geolocator.geocode(result[0], timeout=100)
        except Exception as e:
            print(e)
            raise _fast.HTTPException(_fast.status.HTTP_400_BAD_REQUEST, detail='SERVER_ERROR')
        data_position.append({
            'latitude': location.latitude,
            'longitude': location.longitude,
            'city': result[0]
        })
        print(data_position)    

    return data_position