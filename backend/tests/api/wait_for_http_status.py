import time
from collections.abc import Callable

import pytest
from requests import Response
from starlette import status


def wait_for_http_status(
    http_request: Callable[[], Response],
    wait_for_status: tuple | frozenset | set | list = frozenset(
        {status.HTTP_200_OK},
    ),
    response_func: Callable[[Response], bool] | None = None,
    max_wait_seconds: float = 30,  # with xdist we really need as much on my macbook pro
    sleep_seconds: float = 0.3,
) -> Response:
    """
    Waits for `http_request(uri)` to return result.status_code from
    `wait_for_status` (by default `(200,)`).
    Optionally exit before that if the `response_func(response).json()` returns True

    pytest.fail if it won't happen before `max_wait_seconds`.
    After each check sleeps fo `sleep_seconds`.

    Returns the request's result.
    """
    waiting_time: float = 0
    response = None
    while waiting_time < max_wait_seconds:
        response = http_request()
        if response.status_code in wait_for_status:
            break
        if response.status_code != status.HTTP_202_ACCEPTED:
            pytest.fail(f"Unexpected HTTP status `{response.status_code}`")
        if response_func is not None and response_func(response.json()):
            break
        time.sleep(sleep_seconds)
        waiting_time += sleep_seconds
    else:
        if response is not None:
            pytest.fail(
                f"Enumeration result is being in status `{response.status_code}` "
                f"more than {waiting_time} secs",
            )
        else:
            pytest.fail("The request returns None")
    assert response is not None  # Type narrowing: response is guaranteed to be set here
    return response
