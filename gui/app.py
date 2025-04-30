import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
from data.data_manager import load_animals
from gui.animal_form import AnimalFormWindow

class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.animal_type = None
        self.toggle_reserved_button = None
        self.selected_animal_name = None
        self.available_button = None
        self.sorting_frame = None
        self.load_button_dogs = None
        self.load_button_monkey = None
        self.add_button_dog = None
        self.add_button_monkey = None
        self.action_frame = None
        self.tree = None

        # Table column headers
        self.columns = ["Name", "Type", "Breed/Species", "Gender", "Age", "Weight", "Acquisition Date",
                        "Acquisition Country", "Training Status", "Reserved", "In Service Country"]

        self.title("Grazioso Salvare Animal Rescue Operations")
        self.geometry("1090x600")
        self.resizable(width=False, height=False)
        sv_ttk.set_theme('light')

        # Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, sticky="nw", padx=0, pady=10)


        self.main_frame.columnconfigure(0, weight=1, uniform="equal")
        self.main_frame.columnconfigure(1, weight=0, uniform="equal")
        self.main_frame.rowconfigure(0, weight=1, uniform="equal")
        self.main_frame.rowconfigure(1, weight=0)

        self.create_table()
        self.action_buttons()


    def create_table(self):
        column_widths = {
            "Name": 100,
            "Type": 80,
            "Breed/Species": 150,
            "Gender": 80,
            "Age": 50,
            "Weight": 60,
            "Acquisition Date": 110,
            "Acquisition Country": 120,
            "Training Status": 120,
            "Reserved": 70,
            "In Service Country": 120
        }

        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show="headings")

        for column in self.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=column_widths.get(column, 100), anchor="center", stretch=False)

        self.tree.grid(column=0, row=0, sticky="nsew", padx=10, pady=10)



    def action_buttons(self):
        self.action_frame = ttk.LabelFrame(self.main_frame, text="Action")
        self.action_frame.grid(row=1, column=0, sticky="nw", padx=10, pady=0)

        self.load_button_dogs = ttk.Button(self.action_frame, text="Load Dogs", command=self.load_dogs)
        self.load_button_dogs.grid(row=0, column=0, padx=5, pady=5)

        self.load_button_monkey = ttk.Button(self.action_frame, text="Load Monkey", command=self.load_monkey)
        self.load_button_monkey.grid(row=1, column=0, padx=5, pady=5)

        self.add_button_dog = ttk.Button(self.action_frame, text="Add Dog", command=self.add_dog)
        self.add_button_dog.grid(row=2, column=0, padx=5, pady=5)

        self.add_button_monkey = ttk.Button(self.action_frame, text="Add Monkey", command=self.add_monkey)
        self.add_button_monkey.grid(row=3, column=0, padx=5, pady=5)

        self.available_button = ttk.Button(self.action_frame, text="Available", command=self.show_reserved)
        self.available_button.grid(row=0, column=1, padx=25, pady=5)

        self.toggle_reserved_button = ttk.Button(self.action_frame, text="Toggle Reserved")
        self.toggle_reserved_button.grid(row=0, column=3, padx=25, pady=5)

    def load_dogs(self):
        dogs = load_animals("data/animal_data_dog.json")
        self.display_animals(dogs)

    def load_monkey(self):
        monkey = load_animals("data/animal_data_monkey.json")
        self.display_animals(monkey)

    def add_dog(self):
        AnimalFormWindow(self, animal_type="Dog")

    def add_monkey(self):
        AnimalFormWindow(self, animal_type="Monkey")

    def display_animals(self, animals):
        """Display animals in the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for animal in animals:
            self.tree.insert("", "end", values=(
                animal.get("name"),
                animal.get("animal_type"),
                animal.get("breed") if "breed" in animal else animal.get("species"),
                animal.get("gender"),
                animal.get("age"),
                animal.get("weight"),
                animal.get("acquisition_date"),
                animal.get("acquisition_country"),
                animal.get("training_status"),
                animal.get("reserved"),
                animal.get("in_service_country"),
            ))

    def show_reserved(self):
        dogs = load_animals("data/animal_data_dog.json")
        monkey = load_animals("data/animal_data_monkey.json")

        all_animals = dogs + monkey
        reserved_animals = [animal for animal in all_animals if animal.get("reserved") == "No"]

        self.display_animals(reserved_animals)





