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
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            animals = json.load(file)
            if not isinstance(animals, list):
                logging.warning("%s content is not a list. Returning empty list.", file_name)
                return []
        logging.info("Loaded %d animals from %s", len(animals), file_name)
        return animals
    except FileNotFoundError:
        logging.warning("File %s not found. Starting with empty list.", file_name)
        return []
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON in %s: %s", file_name, e)
        return []


def save_animals(file_name, animal_data):
    """
    Appends new animals to the JSON file without overwriting existing ones.
    """
    try:
        if not (isinstance(animal_data, list) and all(isinstance(item, dict) for item in animal_data)):
            logging.error("animal_data must be a list of dictionaries.")
            return

        existing = []
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                try:
                    existing = json.load(file)
                    if not isinstance(existing, list):
                        logging.warning("Existing file content is not a list. Starting fresh.")
                        existing = []
                except json.JSONDecodeError:
                    logging.warning("File %s contains invalid JSON. Overwriting.", file_name)

        # Combine and write
        combined = existing + animal_data
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(combined, file, indent=4)
        logging.info("Appended %d animals to %s successfully.", len(animal_data), file_name)

    except Exception as e:
        logging.error("Error saving to %s: %s", file_name, e)


def replace_all_animals(file_name, animals):
    """
    Replaces the entire animal list in the file.
    """
    try:
        if isinstance(animals, list) and all(isinstance(item, dict) for item in animals):
            with open(file_name, "w", encoding="utf-8") as file:
                json.dump(animals, file, indent=4)
            logging.info("Replaced all data in %s successfully!", file_name)
        else:
            logging.error("Data must be a list of dictionaries.")
    except Exception as e:
        logging.error("Error saving data to %s: %s", file_name, e)
