# Budget Tracker

## Description
A simple budget tracker application built with Python and Tkinter.  
The app lets you add income and expenses, view total amounts, filter data by month and year, and plot graphs to visualize your finances.

## Features
- Add income and expenses with date, category, description, and amount.
- View total income and total expenses.
- Filter income and expenses by month and year.
- Plot pie charts for income and expenses by category.
- Compare income vs expense with bar chart.
- Data is saved in CSV files inside `budgettracker/` folder.

## Requirements
- Python 3.x
- `tkinter` 
- `matplotlib`
- `tkcalendar`

## How to Run
1. Make sure all files and the `budgettracker/` folder are in the same directory.
2. Install dependencies if needed:


## File Structure
- `main.py` - Main GUI and app logic.
- `expense.py` - Functions related to expenses.
- `income.py` - Functions related to income.
- `budgettracker/` - Folder with `income.csv` and `expenses.csv` for data storage.
- `budget.png` - Icon for the app window.

## Notes
- Ensure `budgettracker/` folder exists and is writable to save CSV files.
- The app will create CSV files if they don't exist when adding data.

---

Enjoy tracking your budget!
