import os
import json
import re

# Désactive totalement la télémétrie LangChain AVANT tout import de langchain
os.environ["LANGCHAIN_TELEMETRY_DISABLED"] = "true"

from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langgraph.graph import StateGraph

# -----------------------------------------------------------------------------
# Configuration LLM et Embeddings
# -----------------------------------------------------------------------------
BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM = ChatOllama(model="mistral", base_url=BASE_URL, temperature=0.2)
EMBED = OllamaEmbeddings(model="mxbai-embed-large", base_url=BASE_URL)

# -----------------------------------------------------------------------------
# Retriever Chroma (vectorstore déjà construit)
# -----------------------------------------------------------------------------
RETRIEVER = Chroma(
    collection_name="bd_rag",
    persist_directory="vectorstore/chroma_db",
    embedding_function=EMBED
).as_retriever(search_kwargs={"k": 50})

# -----------------------------------------------------------------------------
# 1. Extraction des préférences utilisateur
# -----------------------------------------------------------------------------
PREFS_PROMPT = ChatPromptTemplate.from_template(
    "Analyse la requête utilisateur, qui porte UNIQUEMENT sur des bandes dessinées ou mangas, et renvoie un JSON STRICT avec les clés : "
    "genres (liste de strings), auteurs (liste de strings), annees ('YYYY-YYYY' ou vide), "
    "ton (string), min_note (float). Aucune explication ni champ supplémentaire.\n\n"
    "Requête : {query}"
)

def extract_prefs(state: dict) -> dict:
    query = state.get("user_input")
    if not query:
        raise ValueError("Clé 'user_input' manquante dans l'état initial")
    response = LLM.invoke(PREFS_PROMPT.format_messages(query=query))
    match = re.search(r"\{.*\}", response.content, re.S)
    prefs = json.loads(match.group(0)) if match else {}
    state["prefs"] = prefs
    return state

# -----------------------------------------------------------------------------
# 2. Recherche initiale via embeddings
# -----------------------------------------------------------------------------

def retrieve_docs(state: dict) -> dict:
    prefs = state.get("prefs", {})
    terms = prefs.get("genres", []) + prefs.get("auteurs", [])
    query = " ".join(terms)
    state["docs"] = RETRIEVER.get_relevant_documents(query)
    return state

# -----------------------------------------------------------------------------
# 3. Filtrage + tri heuristique
# -----------------------------------------------------------------------------

def filter_docs(state: dict) -> dict:
    prefs = state.get("prefs", {})
    min_note = float(prefs.get("min_note", 0) or 0)
    genres = [g.lower() for g in prefs.get("genres", [])]
    auteurs = [a.lower() for a in prefs.get("auteurs", [])]

    filtered = []
    for doc in state.get("docs", []):
        md = doc.metadata
        note = float(md.get("note") or 0)
        cat = (md.get("categories") or "").lower()
        auth = (md.get("authors") or "").lower()
        if note < min_note:
            continue
        if genres and not any(g in cat for g in genres):
            continue
        if auteurs and not any(a in auth for a in auteurs):
            continue
        filtered.append(doc)

    filtered.sort(key=lambda d: float(d.metadata.get("note") or 0), reverse=True)
    state["filtered"] = filtered[:5]
    return state

# -----------------------------------------------------------------------------
# 4. Narration par LLM
# -----------------------------------------------------------------------------
NARR_PROMPT = ChatPromptTemplate.from_template(
    "En te basant STRICTEMENT sur la sélection JSON ci-dessous (extraits de notre base BD/Manga), "
    "rédige une recommandation engageante en français (≤150 mots). "
    "Cite uniquement ces titres avec leur note entre parenthèses. Ne mentionne jamais d'autres médias.\n\n"
    "Préférences : {prefs}\nSélection : {works}"
)

def narrate(state: dict) -> dict:
    works = [
        {"title": d.metadata.get("title"), "note": d.metadata.get("note"), "categories": d.metadata.get("categories")} 
        for d in state.get("filtered", [])
    ]
    prefs = state.get("prefs", {})
    msg = NARR_PROMPT.format_messages(
        prefs=json.dumps(prefs, ensure_ascii=False),
        works=json.dumps(works, ensure_ascii=False)
    )
    state["answer"] = LLM.invoke(msg).content.strip()
    return state

# -----------------------------------------------------------------------------
# Construction du StateGraph avec un dict natif
# -----------------------------------------------------------------------------

graph = StateGraph(dict)
graph.add_node("prefs", extract_prefs)
graph.add_node("retrieve", retrieve_docs)
graph.add_node("filter", filter_docs)
graph.add_node("narrate", narrate)

graph.set_entry_point("prefs")
graph.add_edge("prefs", "retrieve")
graph.add_edge("retrieve", "filter")
graph.add_edge("filter", "narrate")
graph.set_finish_point("narrate")

RECOMMENDER = graph.compile()

def recommend(user_query: str) -> str:
    """Renvoie une recommandation BD/Manga en fonction de la requête utilisateur."""
    return RECOMMENDER.invoke({"user_input": user_query})["answer"]

# -----------------------------------------------------------------------------
# Test rapide
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print(recommend("Je cherche un manga de l'auteur hojo avec note minimale 4"))





