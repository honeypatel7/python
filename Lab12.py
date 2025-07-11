import csv 
import os 
import pandas as pd 
import matplotlib.pyplot as plt 
from datetime import datetime 

 
EXPENSES_FILE = 'expenses.csv' 
BACKUP_FILE = 'expenses_backup.csv' 
 
# 1. Expense Logging 
def log_expense(): 
    with open(EXPENSES_FILE, mode='a', newline='') as file: 
        writer = csv.writer(file) 
         
        # Gather user input 
        name = input("Enter your name: ") 
        date = input("Enter the date (YYYY-MM-DD): ") 
        description = input("Enter a description of the expense: ") 
        amount = float(input("Enter the amount spent: ")) 
        category = input("Enter the category (e.g., groceries, utilities, entertainment): ") 

 
         
        # Write to CSV 
        writer.writerow([name, date, description, amount, category]) 
        print("Expense logged successfully.") 
 
# Initialize CSV with headers if not exists 
if not os.path.exists(EXPENSES_FILE): 
    with open(EXPENSES_FILE, mode='w', newline='') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Name', 'Date', 'Description', 'Amount', 'Category']) 
 
# 2. Expense Analysis 
def analyze_expenses(): 
    try: 
        # Load the CSV file 
        df = pd.read_csv(EXPENSES_FILE) 
         
        # Convert 'Date' column to datetime, handling any invalid dates 
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce') 
        # Remove rows with invalid dates 
        df = df.dropna(subset=['Date']) 
         
        # Debugging: Check the data content after loading 
        print("\nData loaded for analysis:") 
        print(df.head()) 
 
        # Calculate total expenses per family member 
        member_totals = df.groupby('Name')['Amount'].sum() 
        print("\nTotal expenses per family member:") 
        print(member_totals) 
 
        # Group by date and calculate daily expenses 
        daily_totals = df.groupby(df['Date'].dt.date)['Amount'].sum() 
        print("\nDaily total expenses:") 
        print(daily_totals) 
 
        # Calculate average daily expense for the household 
        average_daily_expense = daily_totals.mean() 
        print(f"\nAverage daily expense for the household: {average_daily_expense:.2f}") 
 
    except Exception as e: 
        print(f"Error analyzing expenses: {e}") 
 
# 3. Expense Trends 
 
def plot_expense_trends(): 
    # Load data 
    df = pd.read_csv(EXPENSES_FILE) 
     
    # Ensure 'Date' column is in datetime format 
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce') 
     
    # Drop rows with NaN values in 'Date' or 'Amount' 
    df = df.dropna(subset=['Date', 'Amount']) 
     
    # Check if there's data in the filtered DataFrame 
    if df.empty: 
        print("No data available.") 

 
        return 
     
    # Sort by date for cumulative calculation 
    df = df.sort_values(by='Date') 
     
    # Group by day and calculate daily expenses 
    daily_expenses = df.groupby(df['Date'].dt.date)['Amount'].sum() 
     
    # Calculate the cumulative sum of daily expenses 
    daily_expenses_cumsum = daily_expenses.cumsum() 
     
    # Plot the cumulative expenses 
    plt.figure(figsize=(10, 6)) 
    plt.plot(pd.to_datetime(daily_expenses.index), daily_expenses_cumsum.values, marker='o') 
    plt.xlabel('Date') 
    plt.ylabel('Cumulative Expenses') 
    plt.title('Expense Trends') 
    plt.xticks(rotation=45) 
    plt.tight_layout() 
    plt.show() 
 
 
# 4. Expense Reporting 
def generate_expense_report(): 
    df = pd.read_csv(EXPENSES_FILE) 
    current_month = datetime.now().month 
    df['Date'] = pd.to_datetime(df['Date']) 
    monthly_df = df[df['Date'].dt.month == current_month] 
 
    # Total expenses for each family member for the current month 
    member_totals = monthly_df.groupby('Name')['Amount'].sum() 
    print("\nMonthly expenses per family member:") 
    print(member_totals) 
 
    # Breakdown of expenses by category 
    category_totals = monthly_df.groupby('Category')['Amount'].sum() 
    print("\nExpense breakdown by category:") 
    print(category_totals) 
 
    # Comparison of monthly expenses 
    monthly_totals = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum() 
    monthly_totals.plot(kind='bar', title="Monthly Expenses Comparison") 
    plt.xlabel('Month') 
    plt.ylabel('Total Expenses') 
    plt.tight_layout() 
    plt.show() 
 
# 6. Expense Budgeting 
def set_budget(): 
    budgets = {} 
    print("Set monthly budget for each category (enter 0 if no budget for a category):") 
    while True: 
        category = input("Enter category name (or type 'done' to finish): ") 
        if category.lower() == 'done': 
            break 
        amount = float(input(f"Enter budget for {category}: ")) 
        budgets[category] = amount 
    return budgets 

 
# The function calculates how much has been spent in each category for the current month. 
def check_budget(budgets): 
    df = pd.read_csv(EXPENSES_FILE) 
    current_month = datetime.now().month 
    df['Date'] = pd.to_datetime(df['Date']) 
    monthly_df = df[df['Date'].dt.month == current_month] 
 
    category_expenses = monthly_df.groupby('Category')['Amount'].sum() 
    for category, budget in budgets.items(): 
        if budget > 0: 
            spent = category_expenses.get(category, 0) 
            remaining = budget - spent 
            if remaining < 0: 
                print(f"Warning: Budget exceeded for {category} by {abs(remaining):.2f}") 
            else: 
                print(f"Remaining budget for {category}: {remaining:.2f}") 
 
# 7. Data Backup and Restore 
def backup_data(): 
    try: 
        pd.read_csv(EXPENSES_FILE).to_csv(BACKUP_FILE, index=False) 
        print("Data backup completed successfully.") 
    except FileNotFoundError: 
        print("Expenses file not found. No backup created.") 
 
def restore_data(): 
    try: 
        pd.read_csv(BACKUP_FILE).to_csv(EXPENSES_FILE, index=False) 
        print("Data restored from backup successfully.") 
    except FileNotFoundError: 
        print("Backup file not found. Unable to restore data.") 
 
# Main menu 
def main(): 
    budgets = {} 
    while True: 
        print("\nHousehold Expenses Tracker Menu:") 
        print("1. Log Expense") 
        print("2. Analyze Expenses") 
        print("3. Plot Expense Trends") 
        print("4. Generate Expense Report") 
        print("5. Set Budget") 
        print("6. Check Budget") 
        print("7. Backup Data") 
        print("8. Restore Data") 
        print("9. Exit") 
 
        choice = input("Enter your choice: ") 
         
        if choice == '1': 
            log_expense() 
        elif choice == '2': 
            analyze_expenses() 
        elif choice == '3': 
            plot_expense_trends() 
        elif choice == '4': 
            generate_expense_report() 
        elif choice == '5': 
            budgets = set_budget() 
        elif choice == '6': 
            check_budget(budgets) 
        elif choice == '7': 
            backup_data() 
        elif choice == '8': 
            restore_data() 
        elif choice == '9': 
            print("Exiting program.") 
            break 
        else: 
            print("Invalid choice. Please try again.") 
if __name__ == '__main__': 
    main()