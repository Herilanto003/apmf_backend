from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, DateTime, func, Enum, Date, Text, Double
from sqlalchemy.orm import relationship
from config.connexion_db import Base


"""
   ************ T A B L E    U T I L I S A T E U R  ************************
"""
class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="UTILISATEUR")
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


# """
#    ************** T A B L E    P O R T S ***********************
# """
# class Ports(Base):
#     __tablename__ = "ports"

#     id_port = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     nom_port = Column(String, nullable=False)
#     apmf = Column(Boolean, nullable=False)
#     id_pays_port = Column(Integer, ForeignKey('pays.id_pays', ondelete='cascade', onupdate='cascade'), nullable=False)

#     pays = relationship('Pays', back_populates='port')
#     navire_prov = relationship('Navires', foreign_keys=[Navires.id_port_prov], back_populates='port_prov')
#     navire_dest = relationship('Navires', foreign_keys=[Navires.id_port_dest], back_populates='port_dest')
#     navire_accoste = relationship('Navires', foreign_keys=[Navires.id_port_accoste], back_populates='port_accoste')

#     marchandise = relationship('Marchandises', back_populates='port')


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
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    navire = relationship('Navires', back_populates='accostage')


"""
   ************** T A B L E    N A V I R E S ***********************
"""
class Navires(Base):
    __tablename__ = "navires"

    id_navire = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_navire = Column(String, nullable=False)
    immatricule_navire = Column(String, nullable=False, unique=True)
    type_navire = Column(nullable=False)
    observation_navire = Column(Text, nullable=False)
    id_port_prov = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_port_dest = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_port_accoste = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_accostage_navire = Column(Integer, ForeignKey('accostage.id_accostage'))
    id_pays_navire = Column(Integer, ForeignKey('pays.id_pays', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    port_prov = relationship('Ports', foreign_keys=[id_port_prov], back_populates='navire_prov', passive_deletes=True, passive_updates=True)
    port_dest = relationship('Ports', foreign_keys=[id_port_dest], back_populates='navire_dest', passive_deletes=True, passive_updates=True)
    port_accoste = relationship('Ports', foreign_keys=[id_port_accoste], back_populates='navire_accoste', passive_deletes=True, passive_updates=True)
    accostage = relationship('Accostage', back_populates='navire', passive_deletes=True, passive_updates=True)
    pays = relationship('Pays', back_populates='navire')
    responsable_navire = relationship('ResponsableNavire', back_populates='navire')
    marchandise = relationship('Marchandises', back_populates='navire')
 

"""
   ************** T A B L E    R E S P O N S A B L E S    N A V I R E ***********************
"""
class ResponsableNavire(Base):
    __tablename__ = "responsable_navire"

    id_resp = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_resp = Column(String, nullable=True)
    role_resp = Column(nullable=False)
    prenoms_resp = Column(String, nullable=True)
    adresse = Column(String, nullable=True)
    cin_resp = Column(String, nullable=True)
    contact_resp = Column(String, nullable=True)
    adresse_email_resp = Column(String, nullable=True)
    nom_ent_resp = Column(String, nullable=True)
    localisation_ent_resp = Column(String, nullable=True)
    email_ent_resp = Column(String, nullable=True)
    id_navire_resp = Column(Integer, ForeignKey('navires.id_navire', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    navire = relationship('Navires', back_populates='responsable_navire', passive_deletes=True, passive_updates=True)


"""
   ************** T A B L E    O P E R A T I O N S ***********************
"""
class Operation(Base):
    __tablename__ = "operation"

    id_operation = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_operation = Column(String, nullable=False)
    type_operation = Column(nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    marchandise = relationship('Marchandises', back_populates='operation')


"""
   ************** T A B L E    M A R C H A N D I S E S ***********************
"""
class Marchandises(Base):
    __tablename__ = "marchandises"

    id_marchandise = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nature_marchandise = Column(String, nullable=False)
    tonnage = Column(Double, nullable=False)
    type_marchandise = Column(nullable=False)
    caractere = Column(nullable=False)
    conditionnement = Column(nullable=False)
    nombre = Column(Integer, nullable=False)
    observation_marchandise = Column(Text, nullable=False)
    id_navire_marchandise = Column(Integer, ForeignKey('navires.id_navire', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_operation_marchandise = Column(Integer, ForeignKey('operation.id_operation', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_port_prov = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_port_dest = Column(Integer, ForeignKey('ports.id_port', ondelete='cascade', onupdate='cascade'), nullable=False)
    id_actionaire_marchandise = Column(Integer, ForeignKey('actionaire.id_actionaire', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    navire = relationship('Navires', back_populates='marchandise', passive_deletes=True, passive_updates=True)
    operation = relationship('Operation', back_populates='marchandise', passive_deletes=True, passive_updates=True)
    port_prov = relationship('Ports', foreign_keys=[id_port_prov], back_populates='marchandise_prov', passive_deletes=True, passive_updates=True)
    port_dest = relationship('Ports', foreign_keys=[id_port_dest], back_populates='marchandise_dest', passive_deletes=True, passive_updates=True)
    actionaire = relationship('Actionaire', back_populates='marchandise')


"""
   ************** T A B L E    P O R T S ***********************
"""
class Ports(Base):
    __tablename__ = "ports"

    id_port = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    nom_port = Column(String, nullable=False)
    apmf = Column(Boolean, nullable=False)
    id_pays_port = Column(Integer, ForeignKey('pays.id_pays', ondelete='cascade', onupdate='cascade'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    pays = relationship('Pays', back_populates='port')
    navire_prov = relationship('Navires', foreign_keys=[Navires.id_port_prov], back_populates='port_prov')
    navire_dest = relationship('Navires', foreign_keys=[Navires.id_port_dest], back_populates='port_dest')
    navire_accoste = relationship('Navires', foreign_keys=[Navires.id_port_accoste], back_populates='port_accoste')

    marchandise_prov = relationship('Marchandises', foreign_keys=[Marchandises.id_port_prov], back_populates='port_prov')
    marchandise_dest = relationship('Marchandises', foreign_keys=[Marchandises.id_port_dest], back_populates='port_dest')


"""
   ************** T A B L E    A C T I O N A I R E S  ***********************
"""
class Actionaire(Base):
    __tablename__ = "actionaire"

    id_actionaire = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    role = Column(nullable=False)
    nom_act = Column(String, nullable=True)
    prenoms_act = Column(String, nullable=True)
    adresse_act = Column(String, nullable=True)
    cin_act = Column(String, nullable=True)
    contact_act = Column(String, nullable=True)
    adresse_email_act = Column(String, nullable=True)
    nom_ent_act = Column(String, nullable=True)
    localisation_ent_act = Column(String, nullable=True)
    email_ent_act = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now())

    marchandise = relationship('Marchandises', back_populates='actionaire')

