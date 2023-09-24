import tkinter as tk
from tkinter import ttk
import pandas as pd
from datetime import date, timedelta, datetime
import random


# Need to insert genuine errors (mutation of field values) rather than string


def random_date(seed):        
    start_date = date(1993, 8, 1)
    end_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d").date()
    random_date = start_date + timedelta(days=random.randint(1, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

class DummyDataCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Dummy Data Creator")
        # Need to add more
        self.data_types = ["int", "float", "str", "bool", "date"]
        # Get this out of field and into "main"
        self.row_count = [10,100,1000,10000,100000]
        self.fields = []

        self.create_widgets()

    def create_widgets(self):
        # Field interface
        ttk.Label(self.root, text="Data Type:").grid(row=0, column=0)
        self.data_type_var = tk.StringVar(self.root)
        self.data_type_var.set(self.data_types[0])
        data_type_option = ttk.OptionMenu(self.root, self.data_type_var, *self.data_types)
        data_type_option.grid(row=0, column=1)

        ttk.Label(self.root, text="Insert Errors:").grid(row=1, column=0)
        self.insert_error_var = tk.BooleanVar(self.root)
        insert_error_checkbox = ttk.Checkbutton(self.root, variable=self.insert_error_var)
        insert_error_checkbox.grid(row=1, column=1)

        ttk.Label(self.root, text="Insert N/A:").grid(row=2, column=0)
        self.insert_na_var = tk.BooleanVar(self.root)
        insert_na_checkbox = ttk.Checkbutton(self.root, variable=self.insert_na_var)
        insert_na_checkbox.grid(row=2, column=1)
        
        # Add field
        ttk.Button(self.root, text="Add Field", command=self.add_field).grid(row=4, column=0, columnspan=2)
        
        # Dataframe parameters
        # Output data row count
        ttk.Label(self.root, text="Row count:").grid(row=5, column=0)
        self.row_count_var = tk.StringVar(self.root)
        self.row_count_var.set(self.row_count[0])
        row_count_option = ttk.OptionMenu(self.root, self.row_count_var, *self.row_count)
        row_count_option.grid(row=5, column=1)
        
        ttk.Button(self.root, text="Generate Data", command=self.generate_data).grid(row=6, column=0, columnspan=2)

    def add_field(self):
        data_type = self.data_type_var.get()
        insert_error = self.insert_error_var.get()
        insert_na = self.insert_na_var.get()
        row_count = self.row_count_var.get()

        field = {"data_type": data_type, "insert_error": insert_error, "insert_na": insert_na, "row_count": row_count}
        self.fields.append(field)
        self.rows = row_count


        field_label = ttk.Label(self.root, text=f"Field {len(self.fields)}: {field}")
        #Expands based on field count
        field_label.grid(row=6 + len(self.fields), column=0, columnspan=2)

    def generate_data(self):
        if not self.fields:
            return
        
        # Create empty dictionary
        # This is the basis for the dataset, fields are added as lists iteratively
        data = {}
        for idx, field in enumerate(self.fields, start=1):
            data_type = field["data_type"]
            insert_error = field["insert_error"]
            insert_na = field["insert_na"]
            row_count = int(self.rows) #int(field["row_count"])

            if data_type == "int":
                if insert_error:
                    data[f"Field_{idx}"] = [random.choice([1, 2, "Error"]) for _ in range(row_count)]
                else:
                    data[f"Field_{idx}"] = [random.randint(1, 100) for _ in range(row_count)]
            elif data_type == "float":
                if insert_error:
                    data[f"Field_{idx}"] = [random.choice([1.0, 2.0, "Error"]) for _ in range(row_count)]
                else:
                    data[f"Field_{idx}"] = [random.uniform(1.0, 100.0) for _ in range(row_count)]
            elif data_type == "str":
                if insert_error:
                    data[f"Field_{idx}"] = [random.choice(["A", "B", "Error"]) for _ in range(row_count)]
                else:
                    data[f"Field_{idx}"] = ["".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(5)) for _ in range(row_count)]
            elif data_type == "bool":
                if insert_error:
                    data[f"Field_{idx}"] = [random.choice([True, False, "Error"]) for _ in range(row_count)]
                else:
                    data[f"Field_{idx}"] = [random.choice([True, False]) for _ in range(row_count)]
            elif data_type == "date":
                seed = 12345
                if insert_error:
                    data[f"Field_{idx}"] = [random.choice([True, False, "Error"]) for _ in range(row_count)]
                else:
                    data[f"Field_{idx}"] = [random_date(seed) for _ in range(row_count)]

            if insert_na:
                for i in range(random.randint(1, 5)):
                    data[f"Field_{idx}"][random.randint(0, 9)] = "N/A"

        df = pd.DataFrame(data)
        df.to_csv("dummy_data.csv", index=False)
        tk.messagebox.showinfo("Info", "Dummy data generated and saved as 'dummy_data.csv'.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DummyDataCreator(root)
    root.mainloop()
