import json

import utils


def normalized_words(text: str):
    for word in text.lower().split():
        yield word


def count_labels():
    """result:
        data2.json = 4331
    """

    profile_path = utils.to_data_dir('data2.json')
    with open(profile_path, 'r') as file:
        data = json.load(file)

    cache = set()

    i = 1
    length = len(data['posts'])
    for post in data['posts']:
        annotations = post['annotations']
        for annotation in annotations:
            if annotation == 'labelAnnotations':
                for item in annotations[annotation]:
                    cache |= set(normalized_words(item['description']))
            elif annotation == 'webDetection':
                for item in annotations[annotation]['webEntities']:
                    if 'description' in item:
                        cache |= set(normalized_words(item['description']))
        print(f'Post {i:4d} / {length}. Current cache length: {len(cache)}')
        i += 1


def main():
    count_labels()


if __name__ == '__main__':
    main()
