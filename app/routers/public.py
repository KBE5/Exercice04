"""Inscription et authentification."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

import math
from app.database import get_db
from app.models import User, Frequentation
from app.schemas import LoginRequest, TokenResponse, FrequentationPageResponse
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="", tags=["Public"])



@router.post("/auth/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """Vérifie les identifiants puis délivre un JWT."""

    user = db.scalar(
        select(User).where(User.username == data.username)
    )

    # Même message pour ne pas révéler si le compte existe.
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Le rôle est ajouté au JWT comme claim applicatif.
    token = create_access_token(
        username=user.username,
        role=user.role,
    )

    return TokenResponse(
        access_token=token,
        role=user.role,
    )



@router.get("/frequentations", response_model=FrequentationPageResponse)
def get_frequentations(
    page: int = Query(1, ge=1, description="Numéro de page"),
    page_size: int = Query(10, ge=1, le=50, description="Nombre d'éléments par page"),
    db: Session = Depends(get_db),
):
    total = db.query(func.count(Frequentation.id)).scalar() or 0
    pages = math.ceil(total / page_size) if total > 0 else 1

    offset = (page - 1) * page_size
    
    items = (
        db.query(Frequentation)
        .order_by(Frequentation.id.asc()) 
        .offset(offset)
        .limit(page_size)
        .all()
    )
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": pages,
    }
