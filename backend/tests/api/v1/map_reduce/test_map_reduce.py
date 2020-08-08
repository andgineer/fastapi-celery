import pytest


@pytest.mark.parametrize('data_path', [('../map_reduce_data')], indirect=['data_path'])
def test_map_reduce(data_path):
    words_file_path = data_path / 'words.txt'
    with words_file_path.open() as words_file:
        pass
