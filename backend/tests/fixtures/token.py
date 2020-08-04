from app.config import get_config as app_config
import pytest


@pytest.fixture(scope='function')
def admin_token(client):
    response = client.post(
        "/api/auth",
        json={
            'login': app_config().admin_login,
            'password': app_config().admin_password,
        }
    )
    return response.json()['token']
