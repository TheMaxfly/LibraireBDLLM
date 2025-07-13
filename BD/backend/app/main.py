# BD/backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .database import create_db_and_tables
from .auth import router as auth_router, get_current_user
from .crud import (
    create_user, get_comics, get_comic,
    create_comic, update_comic, delete_comic
)
from .schemas import (
    UserCreate, UserRead, ComicRead, Token
)
from .recommendation_pipeline import recommend

app = FastAPI(title="BD RAG API")

# CORS (ajustez les origines selon vos besoins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Création des tables au démarrage
def on_startup():
    create_db_and_tables()
app.add_event_handler("startup", on_startup)

# 2. Routes utilisateurs
@app.post("/users", response_model=UserRead, summary="Créer un nouvel utilisateur")
def register(user_in: UserCreate):
    user = create_user(user_in.username, user_in.password)
    return user

# 3. Route token (importée depuis auth)
app.include_router(auth_router, tags=["auth"])

# 4. CRUD Comics (toutes protégées par JWT)
@app.get("/comics", response_model=list[ComicRead], summary="Lister les BD")
def read_comics(current_user=Depends(get_current_user)):
    return get_comics()

@app.get("/comics/{comic_id}", response_model=ComicRead, summary="Récupérer une BD")
def read_comic(comic_id: int, current_user=Depends(get_current_user)):
    comic = get_comic(comic_id)
    if not comic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comic non trouvé")
    return comic

@app.post("/comics", response_model=ComicRead, summary="Créer une BD")
def create_new_comic(comic: ComicRead, current_user=Depends(get_current_user)):
    return create_comic(**comic.dict())

@app.patch("/comics/{comic_id}", response_model=ComicRead, summary="Mettre à jour une BD")
def patch_comic(comic_id: int, comic: ComicRead, current_user=Depends(get_current_user)):
    updated = update_comic(comic_id, **comic.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comic non trouvé")
    return updated

@app.delete("/comics/{comic_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer une BD")
def remove_comic(comic_id: int, current_user=Depends(get_current_user)):
    success = delete_comic(comic_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comic non trouvé")
    return

# 5. Endpoint de recommandation RAG
class RecoRequest(BaseModel):
    prompt: str

class RecoResponse(BaseModel):
    recommendation: str

@app.post("/recommend", response_model=RecoResponse, summary="Obtenir une recommandation BD/Manga")
def post_recommend(req: RecoRequest, current_user=Depends(get_current_user)):
    result = recommend(req.prompt)
    return RecoResponse(recommendation=result)

