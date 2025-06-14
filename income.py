import csv
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import defaultdict
import os

income = os.path.join("budgettracker", "income.csv")

def add_income(date, category, description, amount):
    if not date or not category or not description:
        raise ValueError("All fields must be filled out.")
    if float(amount) <= 0:
        raise ValueError("Amount must be a positive number.")
    file_exists = os.path.isfile(income)
    with open(income, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(income).st_size == 0:
            writer.writerow(['Date', 'Category', 'Description', 'Amount'])
        writer.writerow([date, category, description, amount])
    messagebox.showinfo("Success", "Income added successfully.")


def total_income():
    try:
        with open(income, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            return sum(float(row[3]) for row in reader if row)
    except FileNotFoundError:
       raise FileNotFoundError("No Income recorded yet.")

def plot_income():
    try:
        with open(income, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header 
            incomes = defaultdict(float)
            row_found = False
            for row in reader:
                if row:
                    row_found = True
                    incomes[row[1]] += float(row[3])

            if not row_found:
                messagebox.showinfo("Info", "No income data available. Please add records first.")
                return

        categories = list(incomes.keys())
        amounts = list(incomes.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140,colors=plt.cm.tab20.colors)
        plt.title('Incomes by Category')
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showerror("Error", "No Income recorded yet.")  
    
