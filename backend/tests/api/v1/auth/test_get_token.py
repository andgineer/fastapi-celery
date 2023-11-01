from string import ascii_letters
from string import digits

import pytest
from app.config import get_config as app_config
from fastapi import status
from hypothesis import given
from hypothesis import settings
from hypothesis import strategies as st


@pytest.mark.does_not_change_db
@pytest.mark.unittest  # we do not know server's admin password so this is for unittests only
def test_get_token_success(client):
    response = client.post(
        "/api/auth",
        json={
            "login": app_config().admin_login,
            "password": app_config().admin_password,
        },
    )
    assert response.status_code == 200
    assert response.json()["type"] == "bearer"
    assert len(response.json()["token"]) > 30


@pytest.mark.does_not_change_db
@given(
    st.text(min_size=1, max_size=32, alphabet=ascii_letters + digits),
)
@settings(max_examples=10, deadline=None)
def test_get_token_wrong_login(client, wrong_login):
    response = client.post(
        "/api/auth",
        json={
            "login": wrong_login,
            "password": app_config().admin_password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "password" in response.json()["detail"]
    )  # check that it does not provide info what is wrong


@pytest.mark.does_not_change_db
@given(
    st.text(min_size=1, max_size=32, alphabet=ascii_letters + digits),
)
@settings(max_examples=10, deadline=None)
def test_get_token_wrong_password(client, wrong_password):
    response = client.post(
        "/api/auth",
        json={
            "login": app_config().admin_login,
            "password": wrong_password,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "password" in response.json()["detail"]
    )  # check that it does not provide info what is wrong


# todo inject jwt with wrong group and check the groups really working
