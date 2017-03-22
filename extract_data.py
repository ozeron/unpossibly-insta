import json
import re
import time
from typing import List, Dict

import utils


def add_instagram_features(instagram: dict) -> List[float]:
    features = []

    # add dimensions
    add_dimensions(features, dim=instagram['dimensions'])

    # add date
    add_date(features, datetime=instagram['date'])

    # add comment
    # features.append(instagram['comments']['count'])

    # todo: caption

    return features


def add_dimensions(features, dim):
    features.append(dim['width'])
    features.append(dim['height'])


def add_date(features, datetime):
    date = time.gmtime(datetime)
    features.append(date.tm_mon)
    features.append(date.tm_wday)
    features.append(date.tm_hour)
    features.append(date.tm_min)


def hashed_text(text: str, score: float, limit: int) -> Dict[int, float]:
    text = re.sub(r'[^\w]', '', text)
    res = {}
    for word in text.split():
        res[hash(word) % limit] = score
    return res


def add_label_annotation(features, items: List[dict], limit: int):
    words = {}
    for item in items:
        if 'description' in item:
            d = hashed_text(item['description'], item['score'], limit)
            words.update(d)

    for word, score in words.items():
        features[word] = score


def add_annotations(annotations: dict) -> List[float]:
    limit = 5000  # check out test.count_labels
    features = [0] * limit
    if 'labelAnnotations' in annotations:
        add_label_annotation(features, annotations['labelAnnotations'], limit)
    if 'webDetection' in annotations:
        add_label_annotation(features, annotations['webDetection']['webEntities'], limit)

    return features


def get_features(post: dict) -> List[float]:
    likes = post['instagram']['likes']['count']
    features = [likes]

    # add instagram_feature
    features.extend(add_instagram_features(post['instagram']))

    # add annotations data
    # features.extend(add_annotations(post['annotations']))

    return features


def main(chosen_author=2):
    profile_path = utils.to_data_dir(f'data{chosen_author}.json')
    with open(profile_path, 'r') as file:
        data = json.load(file)

    output_path = utils.to_data_dir('data.csv')
    with open(output_path, 'w') as output:
        for post in data['posts']:
            features = get_features(post)
            output.write(', '.join(map(str, features)))
            output.write('\n')

if __name__ == '__main__':
    main()
