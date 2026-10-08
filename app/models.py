"""Modèles SQLAlchemy."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column


from app.database import Base


class User(Base):
    """Utilisateur de l'API avec un rôle d'autorisation."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Identifiant utilisé lors du login.
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    # Seul le hash bcrypt est stocké.
    password_hash: Mapped[str] = mapped_column(String(100))

    # Le rôle détermine les actions autorisées.
    role: Mapped[str] = mapped_column(
        String(20),
        default="reader",
    )

class Frequentation(Base):
    __tablename__ = "frequentations"

    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mediatheque: Mapped[str] = mapped_column(String, nullable=False)
    mois: Mapped[str] = mapped_column(String(7), nullable=False)  
    visiteurs: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        
        CheckConstraint("visiteurs >= 0", name="check_visiteurs_positif"),
        
        CheckConstraint(
            "mois ~ '^[0-9]{4}-(0[1-9]|1[0-2])$'", name="check_format_mois"
        ),
    )


