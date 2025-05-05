"""
data.data_manager
Handles the saving and loading of the JSON files
"""

import json
import logging
import os


def load_animals(file_name):
    """
    Loads the animal data from the JSON file
    Returns an empty list if file does not exist or is invalid
    """
    if not os.path.isfile(file_name):
        logging.warning("File not found: %s", file_name)
        return []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        logging.warning("JSON decode error in %s: %s", file_name, e)
        return []

def save_animals(file_name, animal_data):
    """
    Appends new animals to the JSON file without overwriting existing ones.
    """
    if not isinstance(animal_data, list) or not all(isinstance(a, dict) for a in animal_data):
        logging.error("Invalid data format: Expected list of dictionaries")
        return

    existing_data = load_animals(file_name)
    combined_data = existing_data + animal_data

    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(combined_data, file, indent=4)
        logging.info("Saved %d new records to %s", len(animal_data), file_name)
    except Exception as e:
        logging.error("Failed to write to %s: %s", file_name, e)


def replace_all_animals(file_name, animals):
    """
    Replaces the entire animal list in the file.
    """
    if not isinstance(animals, list) or not all(isinstance(a, dict) for a in animals):
        logging.error("Invalid data format: Expected list of dictionaries")
        return

    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(animals, file, indent=4)
        logging.info("Replaced data in %s successfully", file_name)
    except Exception as e:
        logging.error("Failed to write to %s: %s", file_name, e)
