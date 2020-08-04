from string import ascii_letters, digits
from hypothesis import given, strategies as st
from app.api.v1.auth.get_user_group import extract_token


@given(
    st.text(min_size=1, max_size=32, alphabet=ascii_letters+digits),
    st.text(min_size=1, max_size=32, alphabet=ascii_letters+digits)
)
def test_extract_token(bearer_str, token_str):
    assert extract_token(bearer_str + ' ' + token_str) == (bearer_str, token_str)

