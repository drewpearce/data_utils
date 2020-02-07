import os
import sys

import pytest

DIR = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(DIR, '..')
sys.path.append(path)

import data_utils  # noqa E402


DATA_DIR = os.path.join(DIR, 'data')


def test_load_file():
    data = data_utils.load_file(os.path.join(DATA_DIR, 'test.json'))
    assert data
    assert 'a' in data

    data = data_utils.load_file(os.path.join(DATA_DIR, 'test.yaml'))
    assert data
    assert 'a' in data

    data = data_utils.load_file(os.path.join(DATA_DIR, 'test.yaml'), raw=True)
    assert data
    assert data.startswith('a: 1')

    with pytest.raises(Exception) as e:
        data = data_utils.load_file(os.path.join(DATA_DIR, 'test.yml'))

    assert 'No such file' in str(e)

    with pytest.raises(Exception) as e:
        data = data_utils.load_file(os.path.join(DATA_DIR, 'test.txt'))

    assert 'Cannot load file' in str(e)


def test_write_file():
    f = os.path.join(DATA_DIR, 'temp.txt')
    data_utils.write_file(f, 'test', raw=True)
    assert os.path.isfile(f)
    assert data_utils.load_file(f, raw=True).startswith('test')
    os.remove(f)

    data = {'test': 'result'}
    f = os.path.join(DATA_DIR, 'temp.json')
    data_utils.write_file(f, data, 'json')
    assert os.path.isfile(f)
    assert data_utils.load_file(f, raw=True).startswith('{\n  "test"')
    os.remove(f)

    f = os.path.join(DATA_DIR, 'temp.yaml')
    data_utils.write_file(f, data, 'yaml')
    assert os.path.isfile(f)
    assert data_utils.load_file(f, raw=True) == 'test: result\n'
    os.remove(f)

    f = os.path.join(DATA_DIR, 'temp.js')
    with pytest.raises(Exception) as e:
        data_utils.write_file(f, data)

    assert 'Cannot write file' in str(e)

    f = os.path.join(DATA_DIR, 'bad/temp.txt')
    with pytest.raises(Exception) as e:
        data_utils.write_file(f, data, raw=True)

    assert 'No such file' in str(e)


def test_convert_data():
    json_data = data_utils.load_file(
        os.path.join(DATA_DIR, 'test.json'), raw=True)
    yaml_data = data_utils.load_file(
        os.path.join(DATA_DIR, 'test.yaml'), raw=True)
    result = data_utils.convert_data(json_data, 'json', 'yaml')
    assert result == yaml_data
    result = data_utils.convert_data(yaml_data, 'yaml', 'json')
    assert result == json_data

    with pytest.raises(Exception) as e:
        result = data_utils.convert_data(json_data, 'yaml', 'yaml')

    assert 'In and out types are the same' in str(e)

    with pytest.raises(Exception) as e:
        result = data_utils.convert_data(json_data, 'js', 'yaml')

    assert 'Invalid input type' in str(e)

    with pytest.raises(Exception) as e:
        result = data_utils.convert_data(json_data, 'json', 'yml')

    assert 'Invalid output type' in str(e)
