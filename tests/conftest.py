"""Fixtures de test d'intégration pour l'API."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.database import get_db
from app.main import app
from app.security import create_access_token

# Engine de test connecté à la base PostgreSQL de test
engine_test = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionTest = sessionmaker(
    bind=engine_test,
    autoflush=False,
    autocommit=False
)


@pytest.fixture()
def db_session():
    
    connexion = engine_test.connect()
    transaction = connexion.begin()

    session = SessionTest(bind=connexion)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connexion.close()


@pytest.fixture()
def client(db_session):
    
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def entete(token: str) -> dict:
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def token_reader():
    
    return create_access_token(username="reader01", role="reader")


@pytest.fixture
def token_analyst():
    
    return create_access_token(username="analyst01", role="analyst")