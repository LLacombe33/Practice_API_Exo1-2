from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    emprunts = relationship("Emprunt", back_populates="lecteur")

class Livre(Base):
    __tablename__ = "livres"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    auteur = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    emprunts = relationship("Emprunt", back_populates="livre")

class Emprunt(Base):
    __tablename__ = "emprunts"
    id = Column(Integer, primary_key=True, index=True)
    lecteur_id = Column(Integer, ForeignKey('users.id'))
    livre_id = Column(Integer, ForeignKey('livres.id'))
    date_emprunt = Column(DateTime)
    date_retour = Column(DateTime, nullable=True)

    lecteur = relationship("User", back_populates="emprunts")
    livre = relationship("Livre", back_populates="emprunts")
