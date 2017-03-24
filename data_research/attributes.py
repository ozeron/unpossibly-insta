import json

import utils


UNWANTED_POSTFIXES = ('url', 'id', 'Id', '_src', 'text', 'code', 'textAnnotations.description')


def have_unwanted(word: str) -> bool:
    return not all([not word.endswith(postfix) for postfix in UNWANTED_POSTFIXES])


def digger(data, cache: dict, header=''):
    if type(data) is dict:
        handle_dict(data, cache, header)
    elif type(data) is list:
        handle_list(data, cache, header)
    # primitives:
    elif type(data) is str:
        handle_str(data, cache, header)
    elif type(data) is bool:
        cache[header] = 'BOOLEAN'
    else:
        # int, float:
        handle_num(data, cache, header)


def handle_dict(data: dict, cache: dict, header: str):
    for key in data:
        next_hearer = f'{header}.{key}' if header else key
        digger(data[key], cache, next_hearer)


def handle_list(data: list, cache: dict, header: str):
    for i in range(len(data)):
        digger(data[i], cache, header)


def handle_str(data: str, cache: dict, header: str):
    if not have_unwanted(header):
        s = cache.get(header, set())
        s.add(data)
        cache[header] = s
    else:
        cache[header] = 'one of UNWANTED tags: ' + ', '.join(UNWANTED_POSTFIXES)


def handle_num(data: int or float, cache: dict, header: str):
    mi, ma = cache.get(header, (None, None))
    if mi is None:
        cache[header] = data, data
    else:
        cache[header] = min(mi, data), max(ma, data)


def main():
    data_path = utils.to_data_dir('data2.json')
    with open(data_path, 'r') as file:
        data = json.load(file)

    cache = dict()
    for post in data['posts']:
        digger(post, cache)

    out_path = utils.to_data_dir('text.json')
    with open(out_path, 'w') as file:
        json.dump(cache, file,
                  default=lambda obj: list(obj) if (type(obj) is set) else obj,
                  indent=4, sort_keys=True)
    print(f'Attributes number: {len(cache)}')
    print(f'Results are written to {out_path}')


if __name__ == '__main__':
    main()
