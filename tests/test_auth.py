"""Tests de l'endpoint d'authentification (/auth/login)."""

import pytest


@pytest.mark.parametrize(
    "username, password, expected_status",
    [
        ("reader01", "Reader2026!", 200),
        ("analyst01", "Analyst2026!", 200),
        ("reader01", "MauvaisPass!", 401),
        ("utilisateur_inconnu", "Reader2026!", 401),
    ],
)
def test_login(client, username, password, expected_status):
    response = client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"