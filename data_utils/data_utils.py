from . import helpers


def load_file(path, data_type=None, raw=False):
    func_map = {
        'json': helpers.from_json,
        'yaml': helpers.from_yaml,
        'yml': helpers.from_yaml
    }

    if not data_type:
        data_type = path.split('.')[-1]

    if data_type not in func_map and not raw:
        raise Exception('Cannot load file of type: {}.'.format(data_type))

    try:
        with open(path) as f:
            out = f.read()

    except Exception as e:
        raise(e)

    if raw:
        return out
    else:
        return func_map[data_type](out)


def write_file(path, data, data_type=None, raw=False):
    func_map = {
        'json': helpers.to_json,
        'yaml': helpers.to_yaml,
        'yml': helpers.to_yaml
    }

    if not data_type:
        data_type = path.split('.')[-1]

    if data_type not in func_map and not raw:
        raise Exception('Cannot write file of type: {}.'.format(data_type))

    if not raw:
        data = func_map[data_type](data)

    try:
        with open(path, 'w') as f:
            f.write(data)

        return True
    except Exception as e:
        raise(e)


def convert_data(data, in_type, out_type):
    if in_type == out_type:
        raise Exception('In and out types are the same: {}'.format(in_type))

    if in_type not in ('data', 'json', 'yaml'):
        raise Exception('Invalid input type: {}'.format(in_type))

    if out_type not in ('data', 'json', 'yaml'):
        raise Exception('Invalid output type: {}'.format(out_type))

    if in_type == 'data':
        return helpers.map_to_raw(data, out_type)
    elif out_type == 'data':
        return helpers.raw_to_map(data, in_type)
    else:
        return helpers.map_to_raw(helpers.raw_to_map(data, in_type), out_type)
