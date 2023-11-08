from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, DateTime, func, Enum, Date, Text, Double
from sqlalchemy.orm import relationship
from config.connexion_db import Base


"""
   ************ T A B L E    U T I L I S A T E U R  ************************
"""
class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String,nullable=False)
    prenoms = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="UTILISATEUR")
    code_activation = Column(String, nullable=False)
    status_compte = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())


"""
   ************** T A B L E    C O N T I N E N T S ***********************
"""
class Continents(Base):
    __tablename__ = "continents"

    id_continent = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_continent = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    pays = relationship('Pays', back_populates= 'continent', passive_deletes=True, passive_updates=True) 


"""
   ************** T A B L E    P A Y S ***********************
"""
class Pays(Base):
    __tablename__ = "pays"

    id_pays = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_pays = Column(String, nullable=False)
    id_continent_pays = Column(Integer, ForeignKey('continents.id_continent', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    continent = relationship('Continents', back_populates='pays')
    port = relationship('Ports', back_populates='pays', passive_deletes=True, passive_updates=True)
    navire = relationship('Navires', back_populates='pays', passive_deletes=True, passive_updates=True)


"""
   ************** T A B L E    A C C O S T A G E ***********************
"""
class Accostage(Base):
    __tablename__ = "accostage"

    id_accostage = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_enreg = Column(Date, nullable=False)
    date_heure_arrive = Column(DateTime, nullable=False)
    date_heure_depart = Column(DateTime, nullable=False)
    numero_escale = Column(String, nullable=False)
    type_desserte = Column(String, nullable=False)
    passage_embarque = Column(Integer, nullable=False)
    passage_debarque = Column(Integer, nullable=False)
    id_navire_accoste = Column(Integer, ForeignKey('navires.id_navire', ondelete='cascade', onupdate='cascade'))
    id_port_accoste = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'))
    id_port_prov = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_port_dest = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    port_prov = relationship('Ports', foreign_keys=[id_port_prov], back_populates='navire_prov', passive_deletes=True, passive_updates=True)
    port_dest = relationship('Ports', foreign_keys=[id_port_dest], back_populates='navire_dest', passive_deletes=True, passive_updates=True)
    navire = relationship('Navires', back_populates='accostage', passive_deletes=True, passive_updates=True)
    port = relationship('Ports', back_populates='accostage', foreign_keys=[id_port_accoste], passive_deletes=True, passive_updates=True)
    marchandise = relationship('Marchandises', back_populates='accostage')
    responsable_navire = relationship('ResponsableNavire', back_populates='accostage')


"""
   ************** T A B L E    N A V I R E S ***********************
"""
class Navires(Base):
    __tablename__ = "navires"

    id_navire = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_navire = Column(String, nullable=False)
    immatricule_navire = Column(String, nullable=False, unique=True)
    type_navire = Column(String, nullable=False)
    observation_navire = Column(Text, nullable=False)
    id_pays_navire = Column(Integer, ForeignKey('pays.id_pays', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    accostage = relationship('Accostage', back_populates='navire',)
    pays = relationship('Pays', back_populates='navire')
 

"""
   ************** T A B L E    R E S P O N S A B L E S    N A V I R E ***********************
"""
class ResponsableNavire(Base):
    __tablename__ = "responsable_navire"

    id_resp = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_resp = Column(String, nullable=True)
    tel_resp = Column(String, nullable=False)
    email_resp = Column(String, nullable=False)
    role_resp = Column(String, nullable=False)
    personne = Column(Boolean, nullable=False)
    id_accoste_resp = Column(Integer, ForeignKey('accostage.id_accostage', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())
 
    accostage = relationship('Accostage', back_populates='responsable_navire', passive_deletes=True, passive_updates=True)


"""
   ************** T A B L E    M A R C H A N D I S E S ***********************
"""
class Marchandises(Base):
    __tablename__ = "marchandises"

    id_marchandise = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nature_marchandise = Column(String, nullable=False)
    tonnage = Column(Double, nullable=False)
    type_marchandise = Column(String, nullable=False)
    caractere = Column(String, nullable=True)
    conditionnement = Column(String, nullable=True)
    nombre = Column(Integer, nullable=False)
    observation_marchandise = Column(Text, nullable=False)
    id_port_march = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=True)
    id_accostage_marchandise = Column(Integer, ForeignKey('accostage.id_accostage', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_act_marchandise = Column(Integer, ForeignKey('actionaire.id_actionaire', ondelete='cascade', onupdate='cascade'))
    nom_operation = Column(String, nullable=False)
    type_operation = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    port = relationship('Ports', back_populates='marchandise_port', passive_deletes=True, passive_updates=True)
    actionaire = relationship('Actionaire', back_populates='marchandise', passive_deletes=True, passive_updates=True)
    accostage = relationship('Accostage', back_populates='marchandise', passive_deletes=True, passive_updates=True)


"""
   ************** T A B L E    P O R T S ***********************
"""
class Ports(Base):
    __tablename__ = "ports"

    id_port = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_port = Column(String, nullable=False)
    apmf = Column(Boolean, nullable=False)
    status = Column(String, nullable=False)
    id_pays_port = Column(Integer, ForeignKey('pays.id_pays', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    pays = relationship('Pays', back_populates='port')
    navire_prov = relationship('Accostage', foreign_keys=[Accostage.id_port_prov], back_populates='port_prov')
    navire_dest = relationship('Accostage', foreign_keys=[Accostage.id_port_dest], back_populates='port_dest')

    marchandise_port = relationship('Marchandises',  back_populates='port')
    accostage = relationship('Accostage', foreign_keys=[Accostage.id_port_accoste], back_populates='port')


"""
   ************** T A B L E    A C T I O N A I R E S  ***********************
"""
class Actionaire(Base):
    __tablename__ = "actionaire"

    id_actionaire = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    role = Column(String, nullable=False)
    nom_act = Column(String, nullable=True)
    adresse_act = Column(String, nullable=True)
    tel_act = Column(String, nullable=True)
    email_act = Column(String, nullable=True)
    personne = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    marchandise = relationship('Marchandises', back_populates='actionaire', passive_deletes=True, passive_updates=True)


class Rapport(Base):
    __tablename__ = "rapport"

    id_rapport = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    fichier = Column(String, nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
