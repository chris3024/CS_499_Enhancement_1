"""
data.data_manager
Handles the saving and loading of the JSON files
"""

import json
import logging


def load_animals(file_name):
    """
    Loads the animal data from the JSON file
    """

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            animals = json.load(file)
        logging.info(f"Loaded animals: {animals}")
        return animals
    except FileNotFoundError:
        logging.error(f"{file_name} not found!")
        return []


def save_animals(file_name, animal_data):
    """
    Saves the animal data from the JSON file
    """

    try:

        if isinstance(animal_data, list) and all(isinstance(item, dict) for item in animal_data):
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(animal_data, file, indent=4)
            logging.info(f"Data saved to {file_name} successfully!")
        else:
            logging.error("Error: animal_data must be a list of dictionaries.")
    except Exception as e:
        logging.error(f"Error saving data to {file_name}: {e}")
