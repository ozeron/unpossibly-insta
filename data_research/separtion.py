import json

import utils


def write_single_post(data, chosen_author, chosen_post):
    post_path = utils.to_data_dir('single_post.json')
    with open(post_path, 'w') as output:
        json.dump(data[chosen_author]['posts'][chosen_post], output)


def write_json(data, chosen, batch=None):
    if batch:
        data[chosen]['posts'] = data[chosen]['posts'][:batch]

    output_path = utils.to_data_dir(f'data{chosen}.json')
    with open(output_path, 'w') as output:
        json.dump(data[chosen], output)


def main():
    dataset_path = utils.to_data_dir('dataset.json')
    with open(dataset_path, 'r') as file:
        data = json.load(file)

    write_json(data, chosen=2)
    # write_single_post(data, chosen_author=2, chosen_post=0)

if __name__ == '__main__':
    main()
