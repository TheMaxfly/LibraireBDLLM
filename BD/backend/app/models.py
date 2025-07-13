from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Comic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str                     # titre de la BD/manga
    note: Optional[float] = Field(default=None, description="Note moyenne")
    nb_notes: Optional[int] = Field(default=None, description="Nombre de notes")
    genre: Optional[str] = Field(default=None, description="Genre brut, avant normalisation")
    authors: Optional[str] = Field(default=None, description="Auteur(s)")
    publisher: Optional[str] = Field(default=None, description="Éditeur")
    synopsis: Optional[str] = Field(default=None, description="Résumé / synopsis")
    note_status: Optional[str] = Field(default=None, description="sufficient / insufficient")
    categories: Optional[str] = Field(default=None, description="Genres normalisés")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date d’insertion")

