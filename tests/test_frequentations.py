"""Tests de la consultation publique des fréquentations (/frequentations)."""

import pytest


def test_get_frequentations_sans_authentification(client):
    """Vérifie que la consultation publique est accessible sans token."""
    response = client.get("/frequentations", params={"page": 1, "page_size": 5})
    assert response.status_code == 200


@pytest.mark.parametrize(
    "page, page_size, expected_items_count, expected_status",
    [
        (1, 5, 5, 200),
        (1, 10, 10, 200),
        (10, 5, 0, 200),
        (0, 5, 422, 402),
    ],
)
def test_get_frequentations_pagination(client, page, page_size, expected_items_count, expected_status):
    response = client.get(
        "/frequentations",
        params={"page": page, "page_size": page_size},
    )
    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()
        assert len(data["items"]) == expected_items_count
        assert data["total"] == 24
        assert data["page"] == page
        assert data["page_size"] == page_size