import os
import sys

path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '..',
    'data_utils'
)
sys.path.append(path)

import helpers  # noqa E402


def test_to_mapping_non_string():
    assert helpers.to_mapping_non_string(None) is None
    assert helpers.to_mapping_non_string({'key': 'value'}) == {'key': 'value'}
    assert helpers.to_mapping_non_string(['test value']) == ['test value']
    assert helpers.to_mapping_non_string(True) == [True]
    assert helpers.to_mapping_non_string(('a', 'b')) == ['a', 'b']


def test_from_json():
    assert helpers.from_json(None) is None
    assert helpers.from_json({'key': 'value'}) == {'key': 'value'}
    assert helpers.from_json(['test value']) == ['test value']
    assert helpers.from_json(True) == [True]
    assert helpers.from_json(('a', 'b')) == ['a', 'b']
    assert helpers.from_json('test value') == ['test value']

    raw = '{"key": "value", "nested": ["a", "b"]}'
    expected = {'key': 'value', 'nested': ['a', 'b']}
    assert helpers.from_json(raw) == expected


def test_from_yaml():
    assert helpers.from_yaml(None) is None
    assert helpers.from_yaml({'key': 'value'}) == {'key': 'value'}
    assert helpers.from_yaml(['test value']) == ['test value']
    assert helpers.from_yaml(True) == [True]
    assert helpers.from_yaml(('a', 'b')) == ['a', 'b']

    assert helpers.from_yaml('test value') == 'test value'
    raw = 'key: value\nnested:\n- a\n- b'
    expected = {'key': 'value', 'nested': ['a', 'b']}
    assert helpers.from_yaml(raw) == expected


def test_raw_to_map():
    assert helpers.raw_to_map(None, 'json') is None
    assert helpers.raw_to_map({'key': 'value'}, 'json') == {'key': 'value'}
    assert helpers.raw_to_map(['test value'], 'json') == ['test value']
    assert helpers.raw_to_map(True, 'json') == [True]
    assert helpers.raw_to_map(('a', 'b'), 'json') == ['a', 'b']
    assert helpers.raw_to_map('test value', 'json') == ['test value']
    assert helpers.raw_to_map('test value', 'nonsense') == ['test value']

    assert helpers.raw_to_map(None, 'yaml') is None
    assert helpers.raw_to_map({'key': 'value'}, 'yaml') == {'key': 'value'}
    assert helpers.raw_to_map(['test value'], 'yaml') == ['test value']
    assert helpers.raw_to_map(True, 'yaml') == [True]
    assert helpers.raw_to_map(('a', 'b'), 'yaml') == ['a', 'b']

    raw = '{"key": "value", "nested": ["a", "b"]}'
    expected = {'key': 'value', 'nested': ['a', 'b']}
    assert helpers.raw_to_map(raw, 'json') == expected

    assert helpers.raw_to_map('test value', 'yaml') == 'test value'
    raw = 'key: value\nnested:\n- a\n- b'
    expected = {'key': 'value', 'nested': ['a', 'b']}
    assert helpers.raw_to_map(raw, 'yaml') == expected


def test_to_json():
    assert helpers.to_json(None) is None
    assert helpers.to_json(True) is True
    assert helpers.to_json('test') == 'test'

    data = ['abc', 'def']
    expected = '[\n  "abc",\n  "def"\n]'
    assert helpers.to_json(data) == expected

    data = {'abc': 1, 'def': ['uvw', 'xyz']}
    expected = '{\n  "abc": 1,\n  "def": [\n    "uvw",\n    "xyz"\n  ]\n}'
    assert helpers.to_json(data) == expected


def test_to_yaml():
    assert helpers.to_yaml(None) is None
    assert helpers.to_yaml(True) is True
    assert helpers.to_yaml('test') == 'test'

    data = ['abc', 'def']
    expected = '- abc\n- def\n'
    assert helpers.to_yaml(data) == expected

    data = {'abc': 1, 'def': ['uvw', 'xyz']}
    expected = 'abc: 1\ndef:\n  - uvw\n  - xyz\n'
