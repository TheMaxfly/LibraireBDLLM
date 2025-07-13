# BD/backend/app/crud.py
from typing import List, Optional
from sqlmodel import Session, select
from passlib.context import CryptContext

from .database import engine
from .models import User, Comic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─── UTILISATEURS ─────────────────────────────────────────────────────────────

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(username: str, password: str) -> User:
    user = User(
        username=username,
        hashed_password=get_password_hash(password)
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def authenticate_user(username: str, password: Optional[str]) -> Optional[User]:
    """
    Si password est None, on récupère simplement l'utilisateur sans le vérifier.
    Utile pour get_current_user().
    """
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.username == username)
        ).first()
        if not user:
            return None
        # Si password fourni, on vérifie
        if password is not None:
            if not pwd_context.verify(password, user.hashed_password):
                return None
        return user


# ─── COMICS ─────────────────────────────────────────────────────────────────

def get_comics() -> List[Comic]:
    """Récupère la liste de toutes les BD/mangas."""
    with Session(engine) as session:
        return session.exec(select(Comic)).all()

def get_comic(comic_id: int) -> Optional[Comic]:
    """Récupère une BD/manga par son identifiant."""
    with Session(engine) as session:
        return session.get(Comic, comic_id)

def create_comic(
    title: str,
    note: Optional[float],
    nb_notes: Optional[int],
    genre: Optional[str],
    authors: Optional[str],
    publisher: Optional[str],
    synopsis: Optional[str],
    note_status: Optional[str],
    categories: Optional[str],
) -> Comic:
    """Crée une nouvelle BD/manga."""
    comic = Comic(
        title=title,
        note=note,
        nb_notes=nb_notes,
        genre=genre,
        authors=authors,
        publisher=publisher,
        synopsis=synopsis,
        note_status=note_status,
        categories=categories,
    )
    with Session(engine) as session:
        session.add(comic)
        session.commit()
        session.refresh(comic)
    return comic

def update_comic(
    comic_id: int,
    **fields
) -> Optional[Comic]:
    """
    Met à jour les champs fournis d'une BD/manga existante.
    Ne modifie que les clés présentes dans **fields**.
    """
    with Session(engine) as session:
        comic = session.get(Comic, comic_id)
        if not comic:
            return None
        for key, value in fields.items():
            if hasattr(comic, key):
                setattr(comic, key, value)
        session.add(comic)
        session.commit()
        session.refresh(comic)
        return comic

def delete_comic(comic_id: int) -> bool:
    """Supprime une BD/manga par son ID."""
    with Session(engine) as session:
        comic = session.get(Comic, comic_id)
        if not comic:
            return False
        session.delete(comic)
        session.commit()
        return True

