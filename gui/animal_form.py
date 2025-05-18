"""
gui.animal_form
Handles the form to add animals
"""
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from data.data_manager import append_animal_records


class AnimalFormWindow(tk.Toplevel):

    def __init__(self, parent, animal_type):
        super().__init__(parent)
        self.animal_type = animal_type
        self.title("Animal Form")
        self.geometry("400x600")
        self.resizable(False, False)

        self.inputs = {}
        self.create_widgets()

    def create_widgets(self):
        field_width = 30
        frame = ttk.LabelFrame(self, text="Add Animal")
        frame.grid(column=0, row=0, padx=10, pady=10, sticky="nsew")

        def add_input(labels, rows, widget_function):
            ttk.Label(frame, text=labels).grid(column=0, row=rows, padx=10, pady=5, sticky="e")
            widget = widget_function()
            widget.grid(column=1, row=rows, padx=10, pady=5, sticky="w")
            self.inputs[labels.lower().replace(" ", "_")] = widget

        add_input("Name", 0, lambda: ttk.Entry(frame, width=field_width))

        if self.animal_type == "Dog":
            add_input("Breed", 1, lambda: ttk.Entry(frame, width=field_width))
        else:
            add_input("Species", 1, lambda: ttk.Combobox(
                frame, values=["Capuchin", "Guenon", "Macaque", "Marmoset", "Squirrel Monkey", "Tamarin"],
                state="readonly", width=25))

        add_input("Gender", 2, lambda: ttk.Combobox(
            frame, values=["Male", "Female"], state="readonly", width=25))

        for label, row in [("Age", 3), ("Weight", 4)]:
            add_input(label, row, lambda: ttk.Entry(
                frame, width=field_width,
                validate="key",
                validatecommand=(self.register(self.validate_integer), "%P")
            ))

        add_input("Acquisition Date", 5, lambda: ttk.Entry(frame, width=field_width))
        self.inputs["acquisition_date"].insert(0, datetime.today().strftime('%Y-%m-%d'))

        add_input("Acquisition Country", 6, lambda: ttk.Entry(frame, width=field_width))
        add_input("Training Status", 7, lambda: ttk.Combobox(
            frame, values=["Not Trained", "In Training", "Fully Trained"], state="readonly", width=25))
        add_input("Reserved", 8, lambda: ttk.Combobox(
            frame, values=["Yes", "No"], state="readonly", width=25))
        add_input("In Service Country", 9, lambda: ttk.Entry(frame, width=field_width))

        submit_btn = ttk.Button(frame, text="Submit", command=self.on_submit)
        submit_btn.grid(row=10, column=1, padx=10, pady=10, sticky="e")

    @staticmethod
    def validate_integer(value):
        return value.isdigit() or value == ""

    def on_submit(self):
        required = ["name", "age", "weight", "gender", "acquisition_country", "in_service_country"]
        data = {k: widget.get() for k, widget in self.inputs.items()}

        if any(not data[k].strip() for k in required):
            messagebox.showerror("Error", "Please fill all required fields.", parent=self)
            return

        data["animal_type"] = self.animal_type
        file_map = {
            "Dog": ("breed", "data/animal_data_dog.json"),
            "Monkey": ("species", "data/animal_data_monkey.json")
        }

        specific_field, file_name = file_map[self.animal_type]
        if not data.get(specific_field):
            messagebox.showerror("Error", f"{specific_field.capitalize()} is required.", parent=self)
            return

        append_animal_records(file_name, [data])
        messagebox.showinfo("Success", f"{self.animal_type} saved!", parent=self)
        self.destroy()
