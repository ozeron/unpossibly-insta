import os

from settings import DATA_DIR


def to_data_dir(file_name: str) -> str:
    return os.path.join(DATA_DIR, file_name)
