import tkinter as tk
from tkinter import messagebox,ttk
from tkcalendar import DateEntry
from datetime import datetime
from expense import add_expense, total_expenses, plot_expenses
from income import add_income,  total_income, plot_income
import matplotlib.pyplot as plt
import pandas as pd
import csv

incomefile = 'budgettracker/income.csv'
expensefile = 'budgettracker/expenses.csv'
# Root Window ===>
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("1000x1000")  
icon = tk.PhotoImage(file="budget.png")
root.iconphoto(False, icon)
root.resizable(True, True) 
# Main Layout Frame (Horizontal) ===>
main_layout = tk.Frame(root)
main_layout.pack(fill="both", expand=True)
#Left Panel: Income/Expense Forms ===>
main_frame = tk.Frame(main_layout)
main_frame.pack(side="left", fill="y", padx=10, pady=10)

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

def filter_records(file_path, year, month, record_type):
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            filtered = []
            for row in reader:
                if row and row[0]:
                    try:
                        date_obj = datetime.strptime(row[0], "%m/%d/%y")
                        if date_obj.year == int(year) and date_obj.month == int(month):
                            filtered.append(row)
                    except ValueError:
                        continue
            if not filtered:
                messagebox.showinfo("Info", f"No {record_type} found for the selected month and year.")
            else:
                messagebox.showinfo(f"Filtered {record_type.capitalize()}", f"Found {len(filtered)} records for {month}/{year} for {record_type}.")
            return filtered
    except FileNotFoundError:
        messagebox.showerror("Error", f"No {record_type} recorded yet.")
        return []

def filter_income(year, month):
    return filter_records(incomefile, year, month, "income")

def filter_expenses(year, month):
    return filter_records(expensefile, year, month, "expenses")
   
def update_table_with_filter(year, month):
    for row in tree.get_children():
        tree.delete(row)

    income_rows = filter_income(year, month)
    expense_rows = filter_expenses(year, month)

    income_df = pd.DataFrame(income_rows, columns=["Date", "Category", "Description", "Amount"])
    income_df['Type'] = 'income'

    expense_df = pd.DataFrame(expense_rows, columns=["Date", "Category", "Description", "Amount"])
    expense_df['Type'] = 'expense'

    df = pd.concat([income_df, expense_df], ignore_index=True)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    df.insert(0, 'S.No', range(1, len(df) + 1))
    df['Income'] = df.apply(lambda row: row['Amount'] if row['Type'] == 'income' else '', axis=1)
    df['Expense'] = df.apply(lambda row: row['Amount'] if row['Type'] == 'expense' else '', axis=1)
    df = df[["S.No", "Date", "Category", "Description", "Income", "Expense"]]

    for index, row in df.iterrows():
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=list(row), tags=(tag,))


def open_filter_window():
    filter_window = tk.Toplevel()
    filter_window.title("Filter Entries")
    tk.Label(filter_window, text="Select Month:").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(filter_window, text="Select Year:").grid(row=1, column=0, padx=10, pady=5)
    selected_month = ttk.Combobox(filter_window, values=[f"{i:02}" for i in range(1, 13)], width=5)
    selected_month.grid(row=0, column=1, padx=10, pady=5)
    selected_month.set(datetime.now().strftime('%m'))

    selected_year = ttk.Combobox(filter_window, values=[str(y) for y in range(2000, datetime.now().year + 1)], width=7)
    selected_year.grid(row=1, column=1, padx=10, pady=5)
    selected_year.set(datetime.now().strftime('%Y'))

    def apply_selected_filter():
        year = selected_year.get()
        month = selected_month.get()
        if year and month:
            update_table_with_filter(year, month)
            filter_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please select both month and year.")
    tk.Button(filter_window, text="Apply Filter", command=apply_selected_filter,bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=2, column=0, columnspan=2, pady=10)



def plot_income_vs_expense():
    income = total_income()
    expenses_by_category = total_expenses()
    labels = ['Income', 'Expense']
    values = [income, expenses_by_category]
    colors = ['green', 'red']
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title('Income vs Expense')
    plt.ylabel('Amount')
    plt.show()
    

def update_table():
    for row in tree.get_children():
        tree.delete(row)
    try:
        income_df = pd.read_csv(incomefile)
        income_df['Type'] = 'income'
    except:
        income_df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type"])
    try:
        expense_df = pd.read_csv(expensefile)
        expense_df['Type'] = 'expense'
    except:
        expense_df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type"])

    df = pd.concat([income_df, expense_df], ignore_index=True)
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    df.insert(0, 'S.No', range(1, len(df) + 1))
    df['Income'] = df.apply(lambda row: row['Amount'] if row['Type'] == 'income' else '', axis=1)
    df['Expense'] = df.apply(lambda row: row['Amount'] if row['Type'] == 'expense' else '', axis=1)

    df = df[["S.No", "Date", "Category", "Description", "Income", "Expense"]]

    for index, row in df.iterrows():
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=list(row), tags=(tag,))


def add_income_ui(date, cat, desc, amt):
    try:
        add_income(date, cat, desc, amt)
        update_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_expense_ui(date, cat, desc, amt):
    try:
        add_expense(date, cat, desc, amt)
        update_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def plot_income_and_expense():
    plot_income()
    plot_expenses()

# Right Panel: Centered Table ===>
table_frame = tk.Frame(main_layout, width=400)
table_frame.pack(side="right", fill="both", expand=True)

center_table_frame = tk.Frame(table_frame)
center_table_frame.place(relx=0.5, rely=0.5, anchor="center") 

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview.Heading", font=("Times New Roman", 13, "bold"), foreground="black", background="#e1e1e1")
style.configure("Treeview", 
    font=("Arial", 9),
    rowheight=25,
    bordercolor="black",
    borderwidth=1,
    relief="flat"
)
style.layout("Treeview", [
    ('Treeview.treearea', {'sticky': 'nswe'})
])

# === Treeview Table with Scrollbar ===
tree_scroll = tk.Scrollbar(center_table_frame)
tree_scroll.pack(side="right", fill="y")

columns = ["S.No", "Date", "Category", "Description", "Income", "Expense"]
tree = ttk.Treeview(center_table_frame, columns=columns, show='headings', height=20, yscrollcommand=tree_scroll.set)
tree_scroll.config(command=tree.yview)
tree.column("S.No", width=100, anchor='center')
tree.column("Date", width=150, anchor='center')
tree.column("Category", width=150, anchor='w')
tree.column("Description", width=180, anchor='w')
tree.column("Income", width=100, anchor='e')
tree.column("Expense", width=100, anchor='e')

for col in columns:
    tree.heading(col, text=col)

tree.pack()

tk.Label(main_frame, text="Income section", font=('Times New Roman', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=(10, 0))
i_date=DateEntry(main_frame,datepat="dd/mm/yyyy")
i_date.set_date(datetime.now())
i_category = tk.Entry(main_frame)
i_description = tk.Entry(main_frame)
i_amount = tk.Entry(main_frame)
tk.Label(main_frame, text="Date:").grid(row=1, column=0)
tk.Label(main_frame, text="Source:").grid(row=2, column=0)
tk.Label(main_frame, text="Description:").grid(row=3, column=0)
tk.Label(main_frame, text="Amount:").grid(row=4, column=0)
i_date.grid(row=1, column=1)
i_category.grid(row=2, column=1)
i_description.grid(row=3, column=1)
i_amount.grid(row=4, column=1)
tk.Button(main_frame, text="Add Income", command=lambda: add_income_ui(i_date.get(), i_category.get(), i_description.get(), i_amount.get()),bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=7, column=0, columnspan=2, pady=(10, 0))
tk.Button(main_frame, text="Total Income", command=lambda: messagebox.showinfo("Total Income", f"Total Income: {total_income()}"),bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=8, column=0, columnspan=2, pady=(10, 0))
tk.Button(main_frame, text="Clear Fields", command=clear_income_fields,bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=9, column=0,columnspan=2, pady=(10, 0))


#Expense Section
tk.Label(main_frame, text="Expense Section", font=('Times New Roman', 18, 'bold')).grid(row=17, column=0, columnspan=2, pady=(20, 0))
e_date = DateEntry(main_frame, datepat="dd/mm/yyyy")
e_date.set_date(datetime.now())
e_category = tk.Entry(main_frame)
e_description = tk.Entry(main_frame)
e_amount = tk.Entry(main_frame)
tk.Label(main_frame, text="Date:").grid(row=18, column=0)
tk.Label(main_frame, text="Category:").grid(row=19, column=0) 
tk.Label(main_frame, text="Description:").grid(row=20, column=0)
tk.Label(main_frame, text="Amount:").grid(row=21, column=0)
e_date.grid(row=18, column=1)
e_category.grid(row=19, column=1)
e_description.grid(row=20, column=1)
e_amount.grid(row=21, column=1)
tk.Button(main_frame, text="Add Expense", command=lambda: add_expense_ui(e_date.get(), e_category.get(), e_description.get(), e_amount.get()),bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=24, column=0, columnspan=2, pady=(10, 0))
tk.Button(main_frame, text="Total Expenses", command=lambda: messagebox.showinfo("Total Expenses", f"Total Expenses: {total_expenses()}"),bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=25, column=0, columnspan=2, pady=(10, 0))
tk.Button(main_frame, text="Clear Fields", command=clear_expense_fields,bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=26, column=0,columnspan=2, pady=(10, 0))
tk.Button(main_frame, text="Show All Entries", command=update_table,bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=28, column=0, columnspan=2, pady=(10, 0))
tk.Button(main_frame, text="Filter Entries", command=open_filter_window,bg="#4AA6C5",fg="black",activebackground="#28C5AB").grid(row=29, column=0, columnspan=2, pady=(10, 0))
top_button_frame = tk.Frame(table_frame)
top_button_frame.pack(anchor="e", padx=10, pady=(10, 0)) 
pie_icon_small = tk.PhotoImage(file="pie.png")
plot_button = tk.Button(
    top_button_frame,
    image=pie_icon_small,
    text="Income & Expense",
    compound="left",  
    command=plot_income_and_expense,
    relief="raised",
    cursor="hand2",
    font=("Arial", 9),
    bg="#4AA6C5",fg="black",activebackground="#28C5AB"
)
plot_button.pack(pady=5)

bar_icon = tk.PhotoImage(file="bar.png")
bar_button = tk.Button(
    top_button_frame,
    image=bar_icon,
    text="Income vs Expense",
    compound="left", 
    command=plot_income_vs_expense,
    padx=-10,
    relief="raised",
    cursor="hand2",
    font=("Arial", 9),
    bg="#4AA6C5",fg="black",activebackground="#28C5AB"
)
bar_button.pack(pady=(0, 10))
#tk.Button(root,text="Pie chart expense", command=plot_expenses, bg="#4AA6C5", fg="black", activebackground="#28C5AB").pack(side="bottom", pady=10         )
root.mainloop()
