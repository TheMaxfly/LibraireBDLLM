# backend/app/test_recommendation.py
from recommendation_pipeline import recommend

if __name__ == "__main__":
    q = "Je cherche un manga de l'auteur toriyama avec note minimale 4."
    print("Question :", q)
    print("Recommandation :", recommend(q))
