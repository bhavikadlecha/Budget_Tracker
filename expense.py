import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
from tkcalendar import DateEntry
import os

expense = os.path.join("budgettracker", "expenses.csv")


def add_expense(date, category, description, amount):
    if not date or not category or not description:
        raise ValueError("All fields must be filled out.")
    
    if float(amount) <= 0:
        raise ValueError("Amount must be a positive number.")

    file_exists = os.path.isfile(expense)
    with open(expense, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.stat(expense).st_size == 0:
            writer.writerow(['Date', 'Category', 'Description', 'Amount'])
        writer.writerow([date, category, description, amount])
    messagebox.showinfo("Success", "Expense added successfully.")



def total_expenses():
    try:
        with open(expense, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            return sum(float(row[3]) for row in reader if row)
    except FileNotFoundError:
       raise FileNotFoundError("No expenses recorded yet.")

        




def plot_expenses():
    try:
        with open(expense, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header 
            expenses = defaultdict(float)
            for row in reader:
                if row:
                     expenses[row[1]] += float(row[3])

        categories = list(expenses.keys())
        amounts = list(expenses.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140,colors=plt.cm.tab20.colors)
        plt.title('Expenses by Category')
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        messagebox.showerror("Error", "No expenses recorded yet.")

