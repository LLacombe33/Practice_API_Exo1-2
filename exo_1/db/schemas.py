from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserDisplay(UserBase):
    id: int

    class Config:
        from_attributes = True


class LivreBase(BaseModel):
    titre: str
    auteur: str
    isbn: str


class LivreCreate(LivreBase):
    pass


class LivreDisplay(LivreBase):
    id: int

    class Config:
        from_attributes = True


class EmpruntBase(BaseModel):
    date_emprunt: datetime
    date_retour: Optional[datetime] = None


class EmpruntCreate(EmpruntBase):
    lecteur_id: int
    livre_id: int


class EmpruntDisplay(EmpruntBase):
    id: int
    lecteur: UserDisplay
    livre: LivreDisplay

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
