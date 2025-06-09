import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
from tkcalendar import DateEntry
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
        if not file_exists:
            writer.writerow(['Date', 'Category', 'Description', 'Amount'])
        writer.writerow([date, category, description, amount])
    messagebox.showinfo("Success", "Income record added successfully.")
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
            for row in reader:
                if row:
                     incomes[row[1]] += float(row[3])

        categories = list(incomes.keys())
        amounts = list(incomes.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140,colors=plt.cm.tab20.colors)
        plt.title('Incomes by Category')
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showerror("Error", "No Income recorded yet.")  