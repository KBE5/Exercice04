"""Crée les tables et les comptes de démonstration."""

from sqlalchemy import select

from app.models import User, Frequentation
# Importer User enregistre sa table dans Base.metadata.
from app.database import Base, SessionLocal, engine
from app.models import User
from app.security import hash_password

# Crée les tables déclarées par les modèles si nécessaire.
Base.metadata.create_all(bind=engine)

users_roles = [
    ("reader01", "Reader2026!", "reader"),
    ("analyst01", "Analyst2026!", "analyst"),
    
]

frequentations_data = [
    ("Médiathèque Centrale", "2026-01", 4500),
    ("Médiathèque Centrale", "2026-02", 4200),
    ("Médiathèque Nord", "2026-01", 1800),
    ("Médiathèque Nord", "2026-02", 2100),
    ("Médiathèque Centrale", "2026-01", 4501),
    ("Médiathèque Centrale", "2026-02", 4201),
    ("Médiathèque Nord", "2026-01", 1801),
    ("Médiathèque Nord", "2026-02", 2101),
    ("Médiathèque Centrale", "2026-01", 4502),
    ("Médiathèque Centrale", "2026-02", 4202),
    ("Médiathèque Nord", "2026-01", 1802),
    ("Médiathèque Nord", "2026-02", 2102),
    ("Médiathèque Centrale", "2026-01", 4503),
    ("Médiathèque Centrale", "2026-02", 4203),
    ("Médiathèque Nord", "2026-01", 1803),
    ("Médiathèque Nord", "2026-02", 2103),
    ("Médiathèque Centrale", "2026-01", 4504),
    ("Médiathèque Centrale", "2026-02", 4204),
    ("Médiathèque Nord", "2026-01", 1804),
    ("Médiathèque Nord", "2026-02", 2104),
    ("Médiathèque Centrale", "2026-01", 4505),
    ("Médiathèque Centrale", "2026-02", 4205),
    ("Médiathèque Nord", "2026-01", 1805),
    ("Médiathèque Nord", "2026-02", 2105),
]


with SessionLocal() as db:

#Création table des utilisateurs 
    for username, password, role in users_roles:

        existing_user = db.scalar(
            select(User).where(User.username == username)
        )

        if existing_user is not None:
            print(f"{username} existe déjà.")
            continue

        # Le mot de passe est haché avant son insertion.
        user = User(
            username=username,
            password_hash=hash_password(password),
            role=role,
        )

        db.add(user)
        print(f"{username} ajouté avec le rôle {role}.")

    
#Création table frequentations 

    for mediatheque, mois, visiteurs in frequentations_data:

        
        existing_frequentation = db.scalar(
            select(Frequentation).where(
                Frequentation.mediatheque == mediatheque,
                Frequentation.mois == mois,
            )
        )

        if existing_frequentation is not None:
            print(f"Fréquentation pour {mediatheque} ({mois}) existe déjà.")
            continue

        # Création de l'entité avec uniquement : mediatheque, mois, visiteurs
        frequentation = Frequentation(
            mediatheque=mediatheque,
            mois=mois,
            visiteurs=visiteurs,
        )

        db.add(frequentation)
        print(
            f"Fréquentation ajoutée : {mediatheque} | {mois} | {visiteurs} visiteurs"
        )
#tt enregistrer 
    db.commit()

print("Initialisation terminée.")
#  python -m scripts.init_db