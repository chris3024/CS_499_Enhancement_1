import json
import pytest

@pytest.fixture
def sample_animals():
    """Return two dog + two monkey dicts"""
    return [
        {"name": "Fido", "animal_type": "Dog", "breed": "Labrador",
         "gender": "Male", "age": "3", "weight": "20", "acquisition_date": "2024-01-05",
         "acquisition_country": "USA", "training_status": "Not Trained",
         "reserved": "No", "in_service_country": "USA"},
        {"name": "Molly", "animal_type": "Dog", "breed": "Beagle",
         "gender": "Female", "age": "5", "weight": "18", "acquisition_date": "2023-09-11",
         "acquisition_country": "Canada", "training_status": "Fully Trained",
         "reserved": "Yes", "in_service_country": "Canada"},
        {"name": "Kiki", "animal_type": "Monkey", "species": "Capuchin",
         "gender": "Female", "age": "4", "weight": "7", "acquisition_date": "2022-03-08",
         "acquisition_country": "Brazil", "training_status": "In Training",
         "reserved": "No", "in_service_country": "Brazil"},
        {"name": "Bo", "animal_type": "Monkey", "species": "Marmoset",
         "gender": "Male", "age": "2", "weight": "5", "acquisition_date": "2024-05-01",
         "acquisition_country": "Peru", "training_status": "Not Trained",
         "reserved": "No", "in_service_country": "Peru"},
    ]

@pytest.fixture
def tmp_json(tmp_path, sample_animals):
    """Create a temporary JSON file with sample data."""
    file = tmp_path / "animals.json"
    file.write_text(json.dumps(sample_animals, indent=4))
    return file
