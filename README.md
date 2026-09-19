# Student Expense Tracker

A command-line personal finance application built in Python, designed to help students track income, expenses, budgets, and spending habits — all from the terminal.

## Description

Student Expense Tracker is a beginner-to-intermediate level Python project that demonstrates core programming concepts through a real-world, practical application. It allows users to record income and expenses, categorize spending, set monthly budgets, search and filter transactions, generate reports, and export data to CSV — with all data persisted between sessions using JSON.

## Features

- Add income and expenses
- View all transactions in a formatted table
- Delete a transaction
- Categorize expenses (Food, Transport, Education, Shopping, Entertainment, Health, Other)
- Calculate total income, total expenses, and current balance
- Set a monthly budget with overspending warnings
- Generate a monthly spending report (by category, highest expense, remaining budget)
- Search/filter transactions by category, date, or type
- Save data permanently using JSON
- Load saved data automatically on startup
- Export all transactions to a CSV file

## Technologies

- Python 3
- Standard library only: `json`, `csv`, `os`, `datetime`
- No external dependencies, no frameworks, no database

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/<your-username>/student_expense_tracker.git
   ```
2. Navigate into the project folder:
   ```
   cd student_expense_tracker
   ```
3. No additional packages are required — the project uses only Python's standard library.

## How to Run

```
python main.py
```

or, on some systems:

```
python3 main.py
```

The app automatically creates `data/` and `exports/` folders on first run to store your saved transactions and CSV exports.

## Example Usage

```
===== Student Expense Tracker =====
1. Add Income
2. Add Expense
3. View All Transactions
4. Delete Transaction
5. Search/Filter Transactions
6. Set Monthly Budget
7. Show Monthly Report
8. Export to CSV
9. Exit
Enter your choice: 2
Enter expense amount: 250
Categories:
1. Food
2. Transport
3. Education
4. Shopping
5. Entertainment
6. Health
7. Other
Choose category number: 1
Enter date (YYYY-MM-DD) or press Enter for today: 
Expense added successfully!
```

## Future Improvements

- Better CLI interface (colors, menus with arrow-key navigation)
- More robust date handling and filtering by date ranges
- Recurring expenses (e.g. subscriptions)
- Multiple budgets (per category, per week)
- Password protection for the data file
- Migrating from JSON to a SQLite database
- Graphical user interface (GUI)
- Web-based version

## Author

Built as a learning project to practice core Python concepts: variables, control flow, functions, file handling, JSON, CSV, and exception handling.