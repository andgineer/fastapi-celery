import pytest
from fastapi import status
from requests import Response
from tests.api.wait_for_http_status import wait_for_http_status


@pytest.mark.parametrize("data_path", [("../map_reduce_data")], indirect=["data_path"])
def test_words_count(data_path, client, celery_session_worker, celery_session_app):
    words_file_path = data_path / "words.txt"
    with words_file_path.open() as words_file:
        response: Response = client.post(
            "/api/words",
            files={
                "text": ("text.txt", words_file.read()),
            },
            follow_redirects=False,
        )
    assert response.status_code == status.HTTP_303_SEE_OTHER
    uri = response.headers["Location"]
    assert len(uri) > 20
    assert uri.startswith("/api/words/")
    response = wait_for_http_status(
        lambda: client.get(uri),
        max_wait_seconds=300,
    )
    assert response.json()["count"] == 69
