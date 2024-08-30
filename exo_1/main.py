from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from db import models, crud
from db.database import engine, get_db
from auth import auth
from auth.auth import get_current_user
from db import schemas
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.UserDisplay)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/me/", response_model=schemas.UserDisplay)
def read_users_me(current_user: schemas.UserDisplay = Depends(get_current_user)):
    return current_user


@app.post("/livres/", response_model=schemas.LivreDisplay)
def create_livre(livre: schemas.LivreCreate, db: Session = Depends(get_db)):
    return crud.create_livre(db=db, livre=livre)


@app.get("/livres/{livre_id}", response_model=schemas.LivreDisplay)
def get_livre(livre_id: int, db: Session = Depends(get_db)):
    db_livre = crud.get_livre(db, livre_id=livre_id)
    if db_livre is None:
        raise HTTPException(status_code=404, detail="Livre not found")
    return db_livre


@app.post("/emprunts/", response_model=schemas.EmpruntDisplay)
def create_emprunt(emprunt: schemas.EmpruntCreate,
                   db: Session = Depends(get_db),
                   current_user: schemas.UserDisplay = Depends(get_current_user)):
    if not crud.check_book_availability(db, livre_id=emprunt.livre_id):
        raise HTTPException(status_code=400, detail="Livre already borrowed")
    emprunt.lecteur_id = current_user.id
    return crud.create_emprunt(db=db, emprunt=emprunt)


@app.get("/emprunts/", response_model=List[schemas.EmpruntDisplay])
def get_emprunts(db: Session = Depends(get_db),
                 current_user: schemas.UserDisplay = Depends(get_current_user)):
    return crud.get_emprunts_by_user(db, user_id=current_user.id)
