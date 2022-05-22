import pytest

from vcfio.utils.easy_dict import EasyDict


class TestEasyDict:
    @pytest.mark.parametrize("input_dict, key, default, empty_value, infer_type, expected_value", [
        ({'a': '1'}, 'a', None, None, True, 1),
        ({'a': '1.1'}, 'a', None, None, True, 1.1),
        ({'a': ''}, 'a', None, None, True, ''),
        ({'a': '.'}, 'a', None, '.', True, None),
        ({'a': [1, 2, 3]}, 'a', None, '.', True, [1, 2, 3]),
        ({'a': [1, 2, 3]}, 'a', None, '.', True, [1, 2, 3]),
        ({'a': ['1.1', 1.1]}, 'a', None, '.', True, [1.1, 1.1]),
        ({'a': '1,2,3'}, 'a', None, '.', True, [1, 2, 3]),
        ({'a': '1,2,3'}, 'a', None, '.', False, '1,2,3'),
        ({'a': None}, 'a', 'default', '.', True, 'default'),
        ({'a': None}, 'b', 'default', '.', True, 'default'),
    ])
    def test_get(self, input_dict, key, default, empty_value, infer_type, expected_value):
        ed = EasyDict(input_dict)
        assert expected_value == ed.get(key, default, empty_value, infer_type)
