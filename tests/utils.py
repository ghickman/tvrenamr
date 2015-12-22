import os
import random


PATH = os.path.abspath(os.path.dirname(__file__))


def build_path(path):
    if not os.path.exists(path):
        os.mkdir(path)

    return path


def join_path(path):
    return os.path.join(PATH, path)


def random_files(path):
    for i in range(3):
        yield os.path.join(path, random.choice(os.listdir(path)))
