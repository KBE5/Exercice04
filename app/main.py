"""Point d'entrée principal de l'API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import public, secur



app = FastAPI(
    title="API Mediathèque - JWT, Rôles",
    description="Authentification, autorisation par rôles",
    version="1.0.0",
)

# Autorise explicitement la page HTML servie sur le port 5500.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],

    # Autorise les credentials si le client en utilise.
    allow_credentials=True,

    # Toutes les méthodes sont autorisées pour cette démonstration.
    allow_methods=["*"],

    # Autorise notamment l'en-tête Authorization.
    allow_headers=["*"],
)

app.include_router(public.router)
app.include_router(secur.router)


@app.get("/", tags=["Accueil"])
def root():
    """Confirme que l'API fonctionne."""

    return {
        "message": "API démarrée",
        "documentation": "/docs",
    }
