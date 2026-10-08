"""Schémas Pydantic."""

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str





# --- SCHÉMAS FREQUENTATION  ---

class FrequentationCreate(BaseModel):
    mediatheque: str = Field(..., max_length=100)
    mois: str = Field(..., pattern=r"^\d{4}-(0[1-9]|1[0-2])$", description="Format AAAA-MM")
    visiteurs: int = Field(..., ge=0, description="Entier positif ou nul")


class FrequentationResponse(FrequentationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class FrequentationPageResponse(BaseModel):
    items: list[FrequentationResponse]
    page: int
    page_size: int
    total: int
    pages: int
