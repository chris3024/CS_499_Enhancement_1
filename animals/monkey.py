"""
Name: Christopher Sharp
Course: CS499 Computer Science Capstone
Date Last Modified: 05-18-2025

Description:
    animals.monkey
    Handles the Monkey animal class and its attributes
"""

from animals.rescue_animal import RescueAnimal

class Monkey(RescueAnimal):
    def __init__(self, name, species, gender, age, weight, acquisition_date,
                 acquisition_country, training_status, reserved, in_service_country):
        super().__init__(name, gender, age, weight, acquisition_date, acquisition_country, training_status,
                         reserved, in_service_country)

        self._species = species
        self._animal_type = 'Monkey'

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value
