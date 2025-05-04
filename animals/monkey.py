# animals/monkey.py

from animals.rescue_animal import RescueAnimal

# Monkey class for Monkey data
class Monkey(RescueAnimal):
    def __init__(self, name, species, gender, age, weight, acquisition_date,
                 acquisition_country, training_status, reserved, in_service_country):
        super().__init__(name, gender, age, weight, acquisition_date, acquisition_country, training_status,
                         reserved, in_service_country)

        self._species = species
        self._animal_type = 'Monkey'

    # Getters/Setters for Monkey class
    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value
