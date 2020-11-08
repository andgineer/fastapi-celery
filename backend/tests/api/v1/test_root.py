import pytest


@pytest.mark.does_not_change_db
def test_read_root(client):
    response = client.get("/api/")
    assert response.status_code == 200
    assert "version" in response.json()
