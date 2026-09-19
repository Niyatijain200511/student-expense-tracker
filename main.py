import json
import csv
import os
from datetime import datetime
 
DATA_FILE = "data/transactions.json"
EXPORT_FILE = "exports/transactions.csv"
 
CATEGORIES = ["Food", "Transport", "Education", "Shopping", "Entertainment", "Health", "Other"]
 
transactions = []   # each transaction: {"type": "income"/"expense", "amount": float, "category": str, "date": str}
monthly_budget = 0.0
 
 
# ---------------------- FILE HANDLING ----------------------
 
def ensure_folders():
    os.makedirs("data", exist_ok=True)
    os.makedirs("exports", exist_ok=True)
 
 
def load_data():
    global transactions, monthly_budget
    ensure_folders()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                transactions = data.get("transactions", [])
                monthly_budget = data.get("monthly_budget", 0.0)
            print("Previous data loaded successfully.")
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not read saved data. Starting fresh.")
            transactions = []
            monthly_budget = 0.0
    else:
        print("No saved data found. Starting fresh.")
 
 
def save_data():
    ensure_folders()
    data = {"transactions": transactions, "monthly_budget": monthly_budget}
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except IOError:
        print("Error: Could not save data.")
 
 
# ---------------------- HELPERS ----------------------
 
def get_float_input(prompt):
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
            if number <= 0:
                print("Amount must be greater than zero. Try again.")
                continue
            return number
        except ValueError:
            print("Invalid number. Please enter a numeric value.")
 
 
def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if min_value is not None and number < min_value:
                print(f"Please enter a number >= {min_value}.")
                continue
            if max_value is not None and number > max_value:
                print(f"Please enter a number <= {max_value}.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a whole number.")
 
 
def choose_category():
    print("Categories:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"{i}. {cat}")
    choice = get_int_input("Choose category number: ", 1, len(CATEGORIES))
    return CATEGORIES[choice - 1]
 
 
def get_date_input():
    value = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if value == "":
        return datetime.now().strftime("%Y-%m-%d")
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        print("Invalid date format, using today's date instead.")
        return datetime.now().strftime("%Y-%m-%d")
 
 
# ---------------------- CORE FEATURES ----------------------
 
def add_transaction(t_type):
    amount = get_float_input(f"Enter {t_type} amount: ")
    category = "Income" if t_type == "income" else choose_category()
    date = get_date_input()
 
    transaction = {"type": t_type, "amount": amount, "category": category, "date": date}
    transactions.append(transaction)
    save_data()
    print(f"{t_type.capitalize()} added successfully!")
 
    if t_type == "expense":
        check_budget_warning()
 
 
def view_transactions(filtered_list=None):
    data = filtered_list if filtered_list is not None else transactions
    if not data:
        print("No transactions found.")
        return
    print(f"\n{'No.':<5}{'Type':<10}{'Category':<15}{'Amount':<10}{'Date':<12}")
    print("-" * 52)
    for i, t in enumerate(data, start=1):
        print(f"{i:<5}{t['type']:<10}{t['category']:<15}{t['amount']:<10.2f}{t['date']:<12}")
 
 
def delete_transaction():
    view_transactions()
    if not transactions:
        return
    index = get_int_input("Enter transaction number to delete: ", 1, len(transactions))
    removed = transactions.pop(index - 1)
    save_data()
    print(f"Deleted: {removed['type']} of {removed['amount']} ({removed['category']})")
 
 
def search_transactions():
    print("Search by: 1. Category  2. Date  3. Type")
    option = get_int_input("Choose search option: ", 1, 3)
 
    if option == 1:
        keyword = input("Enter category to search: ").strip().lower()
        results = [t for t in transactions if t["category"].lower() == keyword]
    elif option == 2:
        keyword = input("Enter date (YYYY-MM-DD): ").strip()
        results = [t for t in transactions if t["date"] == keyword]
    else:
        keyword = input("Enter type (income/expense): ").strip().lower()
        results = [t for t in transactions if t["type"] == keyword]
 
    view_transactions(results)
 
 
# ---------------------- CALCULATIONS ----------------------
 
def calculate_total(t_type):
    return sum(t["amount"] for t in transactions if t["type"] == t_type)
 
 
def calculate_balance():
    return calculate_total("income") - calculate_total("expense")
 
 
def calculate_category_totals():
    totals = {}
    for t in transactions:
        if t["type"] == "expense":
            totals[t["category"]] = totals.get(t["category"], 0) + t["amount"]
    return totals
 
 
# ---------------------- BUDGET ----------------------
 
def set_budget():
    global monthly_budget
    monthly_budget = get_float_input("Enter monthly budget amount: ")
    save_data()
    print("Monthly budget set successfully!")
 
 
def check_budget_warning():
    if monthly_budget <= 0:
        return
    total_expense = calculate_total("expense")
    if total_expense > monthly_budget:
        print(f"⚠ WARNING: You have exceeded your monthly budget of {monthly_budget:.2f}!")
    elif total_expense > monthly_budget * 0.8:
        print(f"⚠ Note: You have used over 80% of your monthly budget.")
 
 
# ---------------------- REPORTS ----------------------
 
def show_monthly_report():
    total_income = calculate_total("income")
    total_expense = calculate_total("expense")
    balance = calculate_balance()
    category_totals = calculate_category_totals()
 
    print("\n===== MONTHLY REPORT =====")
    print(f"Total Income   : {total_income:.2f}")
    print(f"Total Expenses : {total_expense:.2f}")
    print(f"Balance        : {balance:.2f}")
    print(f"Monthly Budget : {monthly_budget:.2f}")
    print(f"Remaining Budget: {monthly_budget - total_expense:.2f}")
 
    print("\nSpending by Category:")
    if not category_totals:
        print("No expenses recorded yet.")
    else:
        for category, amount in category_totals.items():
            print(f"- {category}: {amount:.2f}")
 
        highest_category = max(category_totals, key=category_totals.get)
        print(f"\nHighest spending category: {highest_category} ({category_totals[highest_category]:.2f})")
    print("===========================\n")
 
 
# ---------------------- CSV EXPORT ----------------------
 
def export_to_csv():
    ensure_folders()
    if not transactions:
        print("No transactions to export.")
        return
    try:
        with open(EXPORT_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Category", "Amount", "Date"])
            for t in transactions:
                writer.writerow([t["type"], t["category"], t["amount"], t["date"]])
        print(f"Transactions exported successfully to {EXPORT_FILE}")
    except IOError:
        print("Error: Could not export data to CSV.")
 
 
# ---------------------- MENU ----------------------
 
def show_menu():
    print("\n===== Student Expense Tracker =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. Delete Transaction")
    print("5. Search/Filter Transactions")
    print("6. Set Monthly Budget")
    print("7. Show Monthly Report")
    print("8. Export to CSV")
    print("9. Exit")
 
 
def main():
    load_data()
    while True:
        show_menu()
        choice = get_int_input("Enter your choice: ", 1, 9)
 
        if choice == 1:
            add_transaction("income")
        elif choice == 2:
            add_transaction("expense")
        elif choice == 3:
            view_transactions()
        elif choice == 4:
            delete_transaction()
        elif choice == 5:
            search_transactions()
        elif choice == 6:
            set_budget()
        elif choice == 7:
            show_monthly_report()
        elif choice == 8:
            export_to_csv()
        elif choice == 9:
            print("Goodbye! Your data has been saved.")
            break
 
 
if __name__ == "__main__":
    main()