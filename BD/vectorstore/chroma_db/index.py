#!/usr/bin/env python3
"""
BD/vectorstore/chroma_db/index.py
Script pour importer les données dans PostgreSQL et construire Chroma
Usage:
    python index.py
"""
import sys
from pathlib import Path

# Ajouter le chemin vers backend/app pour permettre les imports
REPO_ROOT = Path(__file__).resolve().parents[2]     # BD/
APP_PATH = REPO_ROOT / "backend" / "app"
sys.path.insert(0, str(APP_PATH))

# Importer les fonctions depuis index_data.py
from index_data import import_comics_to_db, build_vector_store

if __name__ == "__main__":
    print("🔄 Import des données dans PostgreSQL...")
    import_comics_to_db()
    print("🔄 Construction du vectorstore ChromaDB...")
    build_vector_store()
    print("✅ Indexation terminée.")





