from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from db.hash import Hash


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = Hash.hash_password(user.password)
    db_user = models.User(nom=user.nom,
                          prenom=user.prenom,
                          email=user.email,
                          hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_livre(db: Session, livre: schemas.LivreCreate):
    db_livre = models.Livre(titre=livre.titre,
                            auteur=livre.auteur,
                            isbn=livre.isbn)
    db.add(db_livre)
    db.commit()
    db.refresh(db_livre)
    return db_livre


def get_livre(db: Session, livre_id: int):
    return db.query(models.Livre).filter(models.Livre.id == livre_id).first()


def create_emprunt(db: Session, emprunt: schemas.EmpruntCreate):
    db_emprunt = models.Emprunt(**emprunt.dict())
    db.add(db_emprunt)
    db.commit()
    db.refresh(db_emprunt)
    return db_emprunt


def get_emprunts_by_user(db: Session, user_id: int):
    return db.query(models.Emprunt).filter(models.Emprunt.lecteur_id == user_id).all()


def check_book_availability(db: Session, livre_id: int):
    return not db.query(models.Emprunt).filter(models.Emprunt.livre_id == livre_id,
                                               models.Emprunt.date_retour == None).first()
