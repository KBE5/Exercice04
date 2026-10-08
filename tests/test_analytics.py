"""Tests des endpoints analytiques (/analytics/bilan)."""

import pytest
from tests.conftest import entete


@pytest.mark.parametrize(
    "fixture_token, expected_status",
    [
        (None, 401),
        ("token_reader", 403),
        ("token_analyst", 200),
    ],
)
def test_analytics_bilan_permissions(client, request, fixture_token, expected_status):
    headers = entete(request.getfixturevalue(fixture_token)) if fixture_token else {}

    response = client.get("/analytics/bilan", headers=headers)
    assert response.status_code == expected_status


def test_analytics_bilan_valeurs_exactes(client, token_analyst):
    """Vérification des agrégats calculés sur le jeu de recette."""
    response = client.get("/analytics/bilan", headers=entete(token_analyst))

    assert response.status_code == 200
    data = response.json()

    assert data["nb_observations"] == 24
    assert data["total_visiteurs"] == 75660
    assert data["moyenne_visiteurs"] == 3152.5