import pytest

from animals.rescue_animal import RescueAnimal
from animals.dog import Dog
from animals.monkey import Monkey

# touch every public property once
@pytest.mark.parametrize(
    "field,value",
    [
        ("name",                "Buddy"),
        ("gender",              "Female"),
        ("age",                 7),
        ("weight",              18),
        ("acquisition_date",    "2025-05-01"),
        ("acquisition_country", "Canada"),
        ("training_status",     "Fully Trained"),
        ("reserved",            "Yes"),
        ("in_service_country",  "Canada"),
    ],
)
def test_rescue_animal_setters_roundtrip(field, value):
    # 9 positional args, in the order defined in rescue_animal.py
    ra = RescueAnimal(
        "Test",          # name
        "Male",          # gender
        4,               # age
        10,              # weight
        "2025-01-01",    # acquisition_date
        "USA",           # acquisition_country
        "Not Trained",   # training_status
        "No",            # reserved
        "USA",           # in_service_country
    )

    setattr(ra, field, value)
    assert getattr(ra, field) == value

def test_dog_properties_roundtrip():
    d = Dog("Fido", "Labrador", "Male", 3, 20, "2024-01-05",
            "USA", "Not Trained", "No", "USA")
    d.breed = "Beagle"
    assert d.breed == "Beagle"
    # inherited
    d.weight = 22
    assert d.weight == 22
    assert d.animal_type == "Dog"

def test_monkey_properties_roundtrip():
    m = Monkey("Bo", "Marmoset", "Male", 2, 5,
               "2024-05-01", "Peru", "Not Trained", "Yes", "Peru")
    m.species = "Capuchin"
    assert (m.species, m.animal_type) == ("Capuchin", "Monkey")
