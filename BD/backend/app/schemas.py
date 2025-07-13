# BD/backend/app/schemas.py

from pydantic import BaseModel
from typing import Optional, List


# ─── AUTHENTICATION ──────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─── COMICS ──────────────────────────────────────────────────────────────────

class ComicBase(BaseModel):
    title: str
    note: Optional[float]
    nb_notes: Optional[int]
    genre: Optional[str]
    authors: Optional[str]
    publisher: Optional[str]
    synopsis: Optional[str]
    note_status: Optional[str]
    categories: Optional[str]

class ComicCreate(ComicBase):
    pass

class ComicRead(ComicBase):
    id: int

    class Config:
        from_attributes = True

class ComicUpdate(BaseModel):
    title: Optional[str]
    note: Optional[float]
    nb_notes: Optional[int]
    genre: Optional[str]
    authors: Optional[str]
    publisher: Optional[str]
    synopsis: Optional[str]
    note_status: Optional[str]
    categories: Optional[str]

    class Config:
        orm_mode = True

