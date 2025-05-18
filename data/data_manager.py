"""
Name: Christopher Sharp
Course: CS499 Computer Science Capstone
Date Last Modified: 05-18-2025

Description:
    data.data_manager
    Handles the saving and loading of the JSON files
"""

import json
import logging
import os


def read_animal_data(file_path):
    """
    Reads animal records from a JSON file.
    Returns an empty list if the file doesn't exist or contains invalid data.
    """
    if not os.path.exists(file_path):
        logging.warning("File not found: %s", file_path)
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as err:
        logging.warning("Failed to parse JSON in %s: %s", file_path, err)
        return []


def append_animal_records(file_path, new_records):
    """
    Appends new records to the animal data JSON file.
    """
    if not isinstance(new_records, list) or not all(isinstance(entry, dict) for entry in new_records):
        logging.error("Invalid input: expected list of dictionaries")
        return

    current_data = read_animal_data(file_path)
    updated_data = current_data + new_records

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, indent=4)
        logging.info("Appended %d records to %s", len(new_records), file_path)
    except Exception as err:
        logging.error("Could not write to file %s: %s", file_path, err)


def overwrite_animal_data(file_path, full_data):
    """
    Replaces all content in the animal data file.
    """
    if not isinstance(full_data, list) or not all(isinstance(entry, dict) for entry in full_data):
        logging.error("Invalid input: expected list of dictionaries")
        return

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(full_data, f, indent=4)
        logging.info("Rewrote all data in %s", file_path)
    except Exception as err:
        logging.error("Failed to write to %s: %s", file_path, err)
