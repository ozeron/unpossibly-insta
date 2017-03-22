import extract_data
import linear_reg


def main():
    print('extracting data...')
    extract_data.main(chosen_author=2)
    print('building model...')
    linear_reg.main()


if __name__ == '__main__':
    main()
