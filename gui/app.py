"""
Name: Christopher Sharp
Course: CS499 Computer Science Capstone
Date Last Modified: 05-18-2025

Description:
    gui.app
    This houses the main GUI for the application
    It sets the treeview and button layout,
    while implementing methods that carryout the actions of the buttons.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
from data.data_manager import read_animal_data, overwrite_animal_data
from gui.animal_form import AnimalFormWindow

class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.columns = [
            "Name", "Type", "Breed/Species", "Gender", "Age", "Weight", "Acquisition Date",
            "Acquisition Country", "Training Status", "Reserved", "In Service Country"
        ]

        self.title("Grazioso Salvare Animal Rescue Operations")
        self.geometry("1090x600")
        self.resizable(False, False)
        sv_ttk.set_theme('light')

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=0, row=0, sticky="nw", padx=0, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.create_table()
        self.create_action_panel()

    def create_table(self):
        column_widths = {
            "Name": 100, "Type": 80, "Breed/Species": 150, "Gender": 80,
            "Age": 50, "Weight": 60, "Acquisition Date": 110, "Acquisition Country": 120,
            "Training Status": 120, "Reserved": 70, "In Service Country": 120
        }

        self.tree = ttk.Treeview(self.main_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor="center", stretch=False)
        self.tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def create_action_panel(self):
        frame = ttk.LabelFrame(self.main_frame, text="Actions")
        frame.grid(row=1, column=0, sticky="nw", padx=10)

        load_buttons = [
            ("Load Dogs", lambda: self.load_animals_by_type("dog")),
            ("Load Monkey", lambda: self.load_animals_by_type("monkey")),
            ("Load All", self.load_all_animals)
        ]

        for i, (text, cmd) in enumerate(load_buttons):
            ttk.Button(frame, text=text, command=cmd).grid(row=0, column=i, padx=5, pady=5)

        add_buttons = [
            ("Add Dog", lambda: self.open_animal_form("Dog")),
            ("Add Monkey", lambda: self.open_animal_form("Monkey"))
        ]

        for i, (text, cmd) in enumerate(add_buttons):
            ttk.Button(frame, text=text, command=cmd).grid(row=1, column=i, padx=5, pady=5)

        action_buttons = [
            ("Available", self.show_unreserved_animals),
            ("Toggle Reserved", self.toggle_reserved_status)
        ]

        for i, (text, cmd) in enumerate(action_buttons):
            ttk.Button(frame, text=text, command=cmd).grid(row=2, column=i, padx=5, pady=5)

    def load_animals_by_type(self, animal_type):
        file_map = {
            "dog": "data/animal_data_dog.json",
            "monkey": "data/animal_data_monkey.json"
        }
        animals = read_animal_data(file_map[animal_type])
        self.display_animals(animals)

    def load_all_animals(self):
        dogs = read_animal_data("data/animal_data_dog.json")
        monkeys = read_animal_data("data/animal_data_monkey.json")
        self.display_animals(dogs + monkeys)

    def display_animals(self, animals):
        """
        Takes the loaded animal data and formats it
        for display into the treeview
        """
        self.tree.delete(*self.tree.get_children())
        for animal in animals:
            self.tree.insert("", "end", values=(
                animal.get("name"),
                animal.get("animal_type"),
                animal.get("breed", animal.get("species", "")),
                animal.get("gender"),
                animal.get("age"),
                animal.get("weight"),
                animal.get("acquisition_date"),
                animal.get("acquisition_country"),
                animal.get("training_status"),
                animal.get("reserved"),
                animal.get("in_service_country")
            ))

    def show_unreserved_animals(self):
        dogs = read_animal_data("data/animal_data_dog.json")
        monkeys = read_animal_data("data/animal_data_monkey.json")
        unreserved = [a for a in dogs + monkeys if a.get("reserved") == "No"]
        self.display_animals(unreserved)

    def toggle_reserved_status(self):
        """
        Takes the selected animal and toggles its reserved status
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No animal selected")
            return

        item = self.tree.item(selected[0])["values"]
        name, a_type, reserved = item[0], item[1], item[9]
        new_status = "Yes" if reserved == "No" else "No"
        item[9] = new_status
        self.tree.item(selected[0], values=item)

        file_path = f"data/animal_data_{a_type.lower()}.json"
        animals = read_animal_data(file_path)
        for animal in animals:
            if animal["name"] == name and animal["animal_type"] == a_type:
                animal["reserved"] = new_status
                overwrite_animal_data(file_path, animals)
                messagebox.showinfo("Success", "Animal data updated")
                return

        messagebox.showerror("Error", "Animal not found")

    def open_animal_form(self, animal_type):
        form = AnimalFormWindow(self, animal_type=animal_type)
        form.grab_set()
        form.wait_window()
