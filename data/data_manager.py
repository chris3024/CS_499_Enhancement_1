# data/data_manager.py

import json

def load_animals(file_name):
    # Loading dogs from JSON
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            animals = json.load(file)
        return animals
    except FileNotFoundError:
        print(f"{file_name} not found!")
        return []


