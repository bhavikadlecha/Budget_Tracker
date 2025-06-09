import tkinter as tk
from tkinter import messagebox,ttk
from tkcalendar import DateEntry
from datetime import datetime
from expense import add_expense, total_expenses, plot_expenses
from income import add_income,  total_income, plot_income
import matplotlib.pyplot as plt
import csv
# main.py

income = 'budgettracker/income.csv'
expense = 'budgettracker/expenses.csv'

def handle_add_expense():
    try:
        add_expense(e_date.get(), e_category.get(), e_description.get(), e_amount.get())
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_expense_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_expense_fields():
    e_date.set_date(datetime.now())
    e_category.delete(0, tk.END)
    e_description.delete(0, tk.END)
    e_amount.delete(0, tk.END)

def clear_income_fields():
    i_date.set_date(datetime.now())
    i_category.delete(0, tk.END)
    i_description.delete(0, tk.END)
    i_amount.delete(0, tk.END)



def handle_add_income():
    try:
        add_income(i_date.get(), i_category.get(), i_description.get(), i_amount.get())
        messagebox.showinfo("Success", "Income added successfully!")
        clear_income_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))



    
def filter_income(year, month):
    try:
        with open(income, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            filtered_income = []
            for row in reader:
                if row and row[0]:
                    try:
                        date_obj = datetime.strptime(row[0], "%m/%d/%y")  # If it's mm/dd/yy
                        if date_obj.year == int(year) and date_obj.month == int(month):
                            filtered_income.append(row)
                    except ValueError:
                        continue 
            if not filtered_income:
                messagebox.showinfo("Info", "No income found for the selected month and year.")
            else:
                messagebox.showinfo("Filtered Income", f"Found {len(filtered_income)} records for {month}/{year}.")
            return filtered_income
    except FileNotFoundError:
        messagebox.showerror("Error", "No income recorded yet.")
        return []
    
def filter_expenses(year, month):
    try:
        with open(expense, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            filtered_expenses = []
            for row in reader:
                if row and row[0]:
                    try:
                        # Try to parse the actual format used in the CSV
                        date_obj = datetime.strptime(row[0], "%m/%d/%y")  # If it's mm/dd/yy
                        if date_obj.year == int(year) and date_obj.month == int(month):
                            filtered_expenses.append(row)
                    except ValueError:
                        continue
            if not filtered_expenses:
                messagebox.showinfo("Info", "No expenses found for the selected month and year.")
            else:
                messagebox.showinfo("Filtered Expenses", f"Found {len(filtered_expenses)} records for {month}/{year}.")
            return filtered_expenses
    except FileNotFoundError:
        messagebox.showerror("Error", "No expenses recorded yet.")
        return []
    
def plot_income_vs_expense():

    income = total_income()
    expense = total_expenses()

    labels = ['Income', 'Expense']
    values = [income, expense]
    colors = ['green', 'red']

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title('Income vs Expense')
    plt.ylabel('Amount')
    plt.show()
root = tk.Tk()
icon = tk.PhotoImage(file="budget.png")
root.iconphoto(False, icon)
root.title("Budget Tracker")
root.geometry("900x900")

tk.Label(root, text="Add Income", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=(10, 0))

i_date=DateEntry(root,datepat="yyyy-mm-dd")
i_date.set_date(datetime.now())
i_category = tk.Entry(root)
i_description = tk.Entry(root)
i_amount = tk.Entry(root)
# Month Dropdown,Year Dropdown
income_filter_month = ttk.Combobox(root, values=[f"{i:02}" for i in range(1, 13)], width=5)
income_filter_month.set(datetime.now().strftime('%m'))


income_filter_year = ttk.Combobox(root, values=[str(y) for y in range(2000, datetime.now().year + 1)], width=7)
income_filter_year.set(datetime.now().strftime('%Y'))



tk.Label(root, text="Date:").grid(row=1, column=0)
tk.Label(root, text="Source:").grid(row=2, column=0)
tk.Label(root, text="Description:").grid(row=3, column=0)
tk.Label(root, text="Amount:").grid(row=4, column=0)
tk.Label(root, text="Month:").grid(row=5, column=0)
tk.Label(root, text="Year:").grid(row=6, column=0)  
i_date.grid(row=1, column=1)
i_category.grid(row=2, column=1)
i_description.grid(row=3, column=1)
i_amount.grid(row=4, column=1)
income_filter_month.grid(row=5, column=1, sticky="w")
income_filter_year.grid(row=6, column=1, sticky="w")

tk.Button(root, text="Add Income", command=lambda: add_income(i_date.get(), i_category.get(), i_description.get(), i_amount.get())).grid(row=7, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Total Income", command=lambda: messagebox.showinfo("Total Income", f"Total Income: {total_income()}")).grid(row=8, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Clear Fields", command=clear_income_fields).grid(row=9, column=0,columnspan=2, pady=(10, 0))
tk.Button(root, text="Plot Income", command=plot_income).grid(row=10, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Filter Income", command=lambda: filter_income(income_filter_year.get(), income_filter_month.get())).grid(row=11, column=0, columnspan=2, pady=(10, 0))

#Expense Section
tk.Label(root, text="Add Expense", font=('Arial', 12, 'bold')).grid(row=14, column=0, columnspan=2, pady=(20, 0))
e_date = DateEntry(root, datepat="yyyy-mm-dd")
e_date.set_date(datetime.now())
e_category = tk.Entry(root)
e_description = tk.Entry(root)
e_amount = tk.Entry(root)

# Month Dropdown,Year Dropdown
expense_filter_month = ttk.Combobox(root, values=[f"{i:02}" for i in range(1, 13)], width=5)
expense_filter_month.set(datetime.now().strftime('%m'))
expense_filter_year = ttk.Combobox(root, values=[str(y) for y in range(2000, datetime.now().year + 1)], width=7)
expense_filter_year.set(datetime.now().strftime('%Y'))
tk.Label(root, text="Date:").grid(row=15, column=0)
tk.Label(root, text="Category:").grid(row=16, column=0) 
tk.Label(root, text="Description:").grid(row=17, column=0)
tk.Label(root, text="Amount:").grid(row=18, column=0)
tk.Label(root, text="Month:").grid(row=19, column=0)
tk.Label(root, text="Year:").grid(row=20, column=0)

e_date.grid(row=15, column=1)
e_category.grid(row=16, column=1)
e_description.grid(row=17, column=1)
e_amount.grid(row=18, column=1)
expense_filter_month.grid(row=19, column=1, sticky="w")
expense_filter_year.grid(row=20, column=1, sticky="w")

tk.Button(root, text="Add Expense", command=lambda: add_expense(e_date.get(), e_category.get(), e_description.get(), e_amount.get())).grid(row=22, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Total Expenses", command=lambda: messagebox.showinfo("Total Expenses", f"Total Expenses: {total_expenses()}")).grid(row=23, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Clear Fields", command=clear_expense_fields).grid(row=24, column=0,columnspan=2, pady=(10, 0))
tk.Button(root, text="Plot Expenses", command=plot_expenses).grid(row=25, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Filter Expenses", command=lambda: filter_expenses(expense_filter_year.get(), expense_filter_month.get())).grid(row=26, column=0, columnspan=2, pady=(10, 0))
tk.Button(root, text="Plot Income vs Expense", command=plot_income_vs_expense).grid(row=27, column=0, columnspan=2, pady=(10, 0))
root.mainloop()