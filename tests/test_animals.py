from animals.dog import Dog
from animals.monkey import Monkey

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
    m = Monkey("Bo", "Marmoset", 20, 40, 30, "Male", 2, 5,
               "2024-05-01", "Peru", "Not Trained", "Yes", "Peru")
    m.species = "Capuchin"
    m.tail_length = 25
    assert (m.species, m.tail_length, m.animal_type) == ("Capuchin", 25, "Monkey")
