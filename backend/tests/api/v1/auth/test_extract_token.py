from string import ascii_letters
from string import digits

from app.api.v1.auth.get_user_group import extract_token
from hypothesis import given
from hypothesis import strategies as st


@given(
    st.text(min_size=1, max_size=32, alphabet=ascii_letters + digits),
    st.text(min_size=1, max_size=32, alphabet=ascii_letters + digits),
)
def test_extract_token(bearer_str, token_str):
    assert extract_token(f"{bearer_str} {token_str}") == (bearer_str, token_str)
