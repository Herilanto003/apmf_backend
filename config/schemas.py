# tous les schemas de tous les tables
import pydantic as _pydantic
import typing as _typing
from datetime import datetime, date


# ----------------------------------------------------------------------------------
# début pour le schema pour la table continent

class PaysSchema(_pydantic.BaseModel):
    nom_pays: str
    id_continent_pays: int

    class Config:
        from_attributes = True


class ShowPays(PaysSchema):
    created_at: datetime
    updated_at: datetime
    id_pays: int

# fin pour le schema pour la table continent
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table continent

class ContinentSchema(_pydantic.BaseModel):
    nom_continent: str

    class Config:
        from_attributes = True


class ShowContinent(ContinentSchema):
    created_at: datetime
    updated_at: datetime
    id_continent: int

# fin pour le schema pour la table continent
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table port

class PortSchema(_pydantic.BaseModel):
    nom_port: str
    id_pays_port: int
    apmf: bool
    status: str

    class Config:
        from_attributes = True


class ShowPort(PortSchema):
    created_at: datetime
    updated_at: datetime
    id_port: int


# fin pour le schema pour la table port
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table navire

class NavireSchema(_pydantic.BaseModel):
    nom_navire: str
    immatricule_navire: str
    type_navire: str
    observation_navire: str
    id_pays_navire: int

    class Config:
        from_attributes = True


class ShowNavire(NavireSchema):
    created_at: datetime
    updated_at: datetime
    id_navire: int
    pays: PaysSchema


# fin pour le schema pour la table navire
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table accostage

class AccostageSchema(_pydantic.BaseModel):
    numero_escale: str
    type_desserte: str
    passage_embarque: int
    passage_debarque: int
    id_navire_accoste: int
    id_port_accoste: int
    date_enreg: date
    id_port_prov: int
    id_port_dest: int
    date_heure_arrive: datetime
    date_heure_depart: datetime

    class Config:
        from_attributes = True


class ShowAccostage(AccostageSchema):
    created_at: datetime
    updated_at: datetime
    id_accostage: int


# fin pour le schema pour la table accostage
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table actionnaire pour les marchandises

class ActionaireSchema(_pydantic.BaseModel):
    role_act: _typing.Optional[str]
    nom_act: _typing.Optional[str]
    adresse_act: _typing.Optional[str]
    tel_act: _typing.Optional[str]
    email_act: _typing.Optional[str]
    personne: bool

    class Config:
        from_attributes = True


class ShowActionnaire(ActionaireSchema):
    id_resp: int
    created_at: datetime
    updated_at: datetime

class ActionairePersonSchema(_pydantic.BaseModel):
    role: str
    nom_act: _typing.Optional[str]
    prenoms_act: _typing.Optional[str]
    cin_act: _typing.Optional[str]
    adresse_act: _typing.Optional[str]
    contact_act: _typing.Optional[str]
    adresse_email_act: _typing.Optional[str]

    class Config:
        from_attributes = True

    
class ActionaireEntrepriseSchema(_pydantic.BaseModel):
    role: str
    nom_ent_act: _typing.Optional[str]
    localisation_ent_act: _typing.Optional[str]
    email_ent_act: _typing.Optional[str]

    class Config:
        from_attributes = True


class ShowActionaire(ActionaireSchema):
    created_at: datetime
    updated_at: datetime
    id_actionaire: int


class ShowActionairePerson(ActionairePersonSchema):
    created_at: datetime
    updated_at: datetime
    id_actionaire: int


class ShowActionaireEntreprise(ActionaireEntrepriseSchema):
    created_at: datetime
    updated_at: datetime
    id_actionaire: int


# fin pour le schema pour la table actionnaire pour les marchandises
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table accostage

class MarchandiseSchema(_pydantic.BaseModel):
    nature_marchandise: str
    tonnage: float
    caractere: _typing.Optional[str]
    type_marchandise: str
    conditionnement: _typing.Optional[str]
    nombre: int
    observation_marchandise: str
    id_port_march: int
    id_accostage_marchandise: int
    nom_operation: str
    type_operation: str
    id_act_marchandise: int

    class Config:
        from_attributes = True


class ShowMarchandise(MarchandiseSchema):
    created_at: datetime
    updated_at: datetime
    id_marchandise: int


# fin pour le schema pour la table accostage
# ------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# début pour le schema pour la table actionnaire pour les responsable navire

class ResponsableNavireSchema(_pydantic.BaseModel):
    role_resp: _typing.Optional[str]
    nom_resp: _typing.Optional[str]
    tel_resp: _typing.Optional[str]
    email_resp: _typing.Optional[str]
    personne: bool
    id_accoste_resp: int

    class Config:
        from_attributes = True


class ShowRepsonsableNavire(ResponsableNavireSchema):
    id_resp: int
    created_at: datetime
    updated_at: datetime

class ResponsableNavirePersonSchema(_pydantic.BaseModel):
    role_resp: _typing.Optional[str]
    nom_resp: _typing.Optional[str]
    prenoms_resp: _typing.Optional[str]
    cin_resp: _typing.Optional[str]
    adresse: _typing.Optional[str]
    contact_resp: _typing.Optional[str]
    adresse_email_resp: _typing.Optional[str]
    personne: bool = True
    id_navire_resp: int

    class Config:
        from_attributes = True

    
class ResponsableNavireEntrepriseSchema(_pydantic.BaseModel):
    role_resp: _typing.Optional[str]
    nom_ent_resp: _typing.Optional[str]
    localisation_ent_resp: _typing.Optional[str]
    email_ent_resp: _typing.Optional[str]
    personne: bool = False
    id_navire_resp: int

    class Config:
        from_attributes = True
 

class ShowResponsableNavirePerson(ResponsableNavirePersonSchema):
    created_at: datetime
    updated_at: datetime
    id_resp: int
 

class ShowResponsableNavireEntreprise(ResponsableNavireEntrepriseSchema):
    created_at: datetime
    updated_at: datetime
    id_resp: int


# fin pour le schema pour la table actionnaire pour les responsable navire
# ------------------------------------------------------------------------------------


# *****************************************************************************************************************************


# ----------------------------------------------------------------------------------
# début pour le schema pour la table UTILISATEUR

class UtilisateurSchema(_pydantic.BaseModel):
    nom: str
    prenoms: str
    email: str
    password: str

    class Config:
        from_attributes = True


class ShowUtilisateur(_pydantic.BaseModel):
    nom: str
    prenoms: str
    email: str
    created_at: datetime
    updated_at: datetime
    id_utilisateur: int
    status_compte: bool

    class Config:
        from_attributes = True


class UtilisateurToken(_pydantic.BaseModel):
    nom: str
    prenoms: str
    email: str
    status_compte: bool
    created_at: datetime
    updated_at: datetime
    id_utilisateur: int

    class Config:
        from_attributes = True


# fin pour le schema pour la table UTILISATEUR
# ------------------------------------------------------------------------------------


class EmailSchema(_pydantic.BaseModel):
    email: _typing.List[_pydantic.EmailStr]


class Code(_pydantic.BaseModel):
    code_activation: str


class RapportSchema(_pydantic.BaseModel):
    nom_port: str
    mois: int
    total_ci: int
    total_bo: int
    total_cir: int
    total_cr: int
    total_general: int

    class Config:
        from_attributes = True

# ------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# début pour le schema pour le statistique

class StatisticSchema(_pydantic.BaseModel):
    # INFORMATION POUR LE NAVIRE
    nom_navire: str
    immatricule_navire: str
    type_navire: str
    observation_navire: str
    id_pays_navire: int
    id_port_prov: int
    id_port_dest: int
    date_heure_arrive: datetime
    date_heure_depart: datetime
    numero_escale: str
    nom_armateur: str
    role_armateur: str = "ARMATEUR"
    tel_armateur: str
    email_armateur: str
    personne_armateur: bool

    # INFORMATION POUR L'ACCOSTAGE
    id_port_accost: int
    type_desserte: str
    passage_embarque: int
    passage_debarque: int

    # INFORMATION DU CONSIGNATAIRE
    nom_cons: str
    role_cons: str = "CONSIGNATAIRE"
    tel_cons: str
    email_cons: str
    personne_cons: bool
    

class StatisticWithNavireSchema(_pydantic.BaseModel):
    # INFORMATION POUR LE NAVIRE
    id_navire: int
    id_port_prov: int
    id_port_dest: int
    date_heure_arrive: datetime
    date_heure_depart: datetime
    numero_escale: str
    nom_armateur: str
    role_armateur: str = "ARMATEUR"
    tel_armateur: str
    email_armateur: str
    personne_armateur: bool

    # INFORMATION POUR L'ACCOSTAGE
    id_port_accost: int
    type_desserte: str
    passage_embarque: int
    passage_debarque: int

    # INFORMATION DU CONSIGNATAIRE
    nom_cons: str
    role_cons: str = "CONSIGNATAIRE"
    tel_cons: str
    email_cons: str
    personne_cons: bool

# fin pour le schema pour le statistique
# ------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# début pour le schema pour le marchandise

class MarchandiseSchema2(_pydantic.BaseModel):
    nature_marchandise: str
    tonnage: float
    type_marchandise: str
    caractere: str
    conditionnement: str
    nombre: int
    observation_marchandise: str
    id_accostage_marchandise: int
    nom_operation: str
    type_operation: str
    id_port_march: int
    nom_act: str
    adresse_act: str
    tel_act: str
    email_act: str
    role_act: str
    personne: bool
    nom_manu: str
    tel_manu: str
    email_mau: str
    role_manu: str
    peronne_manu: bool


class MarchandiseEdit(_pydantic.BaseModel):
    nature_marchandise: str
    tonnage: float
    type_marchandise: str
    caractere: str
    conditionnement: str
    nombre: int
    observation_marchandise: str
    id_accostage_marchandise: int
    nom_operation: str
    type_operation: str
    id_port_march: int   


class ShowActionaireSchema1(_pydantic.BaseModel):
    nom_act: str
    adresse_act: str
    tel_act: str
    email_act: str
    role: str
    personne: bool
    id_actionaire: int  
class ShowMarchandiseSchema2(_pydantic.BaseModel):
    nature_marchandise: str
    tonnage: float
    type_marchandise: str
    caractere: str
    conditionnement: str
    nombre: int
    observation_marchandise: str
    id_accostage_marchandise: int
    nom_operation: str
    type_operation: str
    id_port_march: int
    actionaire: ShowActionaireSchema1
    accostage: ShowAccostage


class ShowActionaireSchema2(_pydantic.BaseModel):
    nom_act: str
    adresse_act: str
    tel_act: str
    email_act: str
    role: str
    personne: bool   
    marchandise: _typing.Optional[_typing.List[ShowMarchandiseSchema2]] 

    class Config():
        orm_mode = True


class ActionaireSchemaEdit(_pydantic.BaseModel):
    nom_act: str
    adresse_act: str
    tel_act: str
    email_act: str
    role: str
    personne: bool   

# fin pour le schema pour le marchandise
# ------------------------------------------------------------------------------------

# affichage port
class ShowPortSchema(_pydantic.BaseModel):
    id_port: int
    apmf: bool
    status: str
    nom_port: str
    pays: PaysSchema

    class config():
        from_attributes = True



class RapportExcel(_pydantic.BaseModel):
    date_debut: date
    date_milieu: date
    date_fin: date