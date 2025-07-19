from os import walk
from csv import reader
from pygame.image import load


def load_layout(file_path):
    with open(file_path) as file:
        return [row for row in reader(file, delimiter=",")]


def load_image(file_path, is_alpha=True):
    image = load(file_path)
    return image.convert_alpha() if is_alpha else image.convert()


def load_image_list(folder_path):
    for parent_path, _, file_names in walk(folder_path):
        file_names = sorted(file_names, key=lambda e: int(e.split(".")[0]))
        return [load_image(f"{parent_path}/{file_name}") for file_name in file_names]


def load_image_dict(folder_path):
    for parent_path, folder_names, _ in walk(folder_path):
        return {
            folder_name: load_image_list(f"{parent_path}/{folder_name}")
            for folder_name in folder_names
        }
