# data/data_manager.py

import json
from logging import exception


def load_animals(file_name):
    # Loading dogs from JSON
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            animals = json.load(file)
        print(f"Loaded animals: {animals}")
        return animals
    except FileNotFoundError:
        print(f"{file_name} not found!")
        return []

def save_animals(file_name, animal_data):
    try:
        # Loading the existing data
        existing_animals = load_animals(file_name)

        # Appending new animal data
        existing_animals.append(animal_data)

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(existing_animals, file, indent=4)

            print(f"Saved {len(existing_animals)} animals to {file_name}")
    except Exception as e:
        print(f"Failed to save {file_name}: {e}")
