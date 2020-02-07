from collections import Mapping
import json

from six import string_types
import yaml


def to_mapping_non_string(raw):
    if raw is None or isinstance(raw, (Mapping, list)):
        return raw
    elif isinstance(raw, tuple):
        return [t for t in raw]
    else:
        return [raw]


def from_json(raw):
    if not isinstance(raw, string_types):
        return to_mapping_non_string(raw)

    try:
        out = json.loads(raw)
    except Exception as e:
        print('Exception loading data: {}'.format(e))
        out = [raw]

    return out


def to_json(data):
    if not isinstance(data, (Mapping, list)):
        return data

    return json.dumps(data, indent=2, sort_keys=True)


def from_yaml(raw):
    if not isinstance(raw, string_types):
        return to_mapping_non_string(raw)

    try:
        out = yaml.safe_load(raw)
    except Exception as e:
        print('Exception loading data: {}'.format(e))
        out = [raw]

    return out


def to_yaml(data):
    if not isinstance(data, (Mapping, list)):
        return data

    return yaml.safe_dump(data)


def raw_to_map(raw, data_type):
    default = 'json'
    type_map = {
        'json': from_json,
        'yaml': from_yaml
    }
    if data_type not in type_map:
        data_type = default

    return type_map[data_type](raw)


def map_to_raw(data, data_type):
    default = 'json'
    type_map = {
        'json': to_json,
        'yaml': to_yaml
    }
    if data_type not in type_map:
        data_type = default

    return type_map[data_type](data)
