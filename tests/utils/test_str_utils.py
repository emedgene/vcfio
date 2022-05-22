from cmath import nan

from vcfio.utils.str_utils import to_number
import pytest


@pytest.mark.parametrize('input_value, default, expected_output', [
    (1, '', 1),
    ('1', '', 1),
    (1.0, '', 1.0),
    (1.2, '', 1.2),
    ('1.0', '', 1.0),
    ('aaaa', '', ''),
    ({'a': 1}, '', ''),
    ('.', None, None),
    ('0', '.', 0),
])
def test_to_number(input_value, default, expected_output):
    assert expected_output == to_number(input_value, default)
