# Import of the json module to work with JSON files
import json

# Global list to store transactions
transactions = []


# Function to load transactions from JSON file (if it exists)
def load_transactions():
    try:
        with open("transactions.json", "r") as file:
            transactions.extend(json.load(file))
    except FileNotFoundError:
        pass  # Ignore if file doesn't exist


# Function to save transactions list to a JSON file
def save_transactions():
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)


# Function to display all transactions with numbering
def view_transactions():
    if not transactions:
        print("No transactions found!")
        return
    print("-" * 65)
    print("{:<5} {:<10} {:<20} {:<10} {:<15}".format("No.", "Amount", "Category", "Type", "Date"))
    print("-" * 65)
    for index, transaction in enumerate(transactions, start=1):
        amount, category, transaction_type, date = transaction
        print("{:<5} {:<10.2f} {:<20} {:<10} {:<15}".format(index, amount, category, transaction_type, date))
    print("-" * 65)


def validate_date(date):
    if not date:  # Skip validation if no date entered (existing date kept)
        return True
    try:
        year, month, day = map(int, date.split("-"))  # Split by "-" and convert to integers
        if not (1 <= year <= 9999 and 1 <= month <= 12 and 1 <= day <= 31):
            raise ValueError("Invalid date components. Please enter a valid date in YYYY-MM-DD format.")

        # Further validation based on month length
        if month in (4, 6, 9, 11) and day > 30:  # Months with 30 days
            raise ValueError(
                "Invalid date for the chosen month. Please enter a valid date in YYYY-MM-DD format.")
        elif month == 2:  # February validation (leap year check not included for simplicity)
            if day > 28:
                raise ValueError(
                    "Invalid date for February. Please enter a valid date in YYYY-MM-DD format.")
        return True
    except ValueError as err:
        raise err  # Re-raise the validation error


# Function to get user input for transaction details and add it to the list
def add_transaction():
    while True:
        try:
            amount = float(input("Enter amount (e.g., 100.50): "))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            category = input("Enter category (e.g., Food, Bills): ")
            transaction_type = input("Enter transaction type (Income/Expense): ").upper()
            if transaction_type not in ("INCOME", "EXPENSE"):
                raise ValueError("Invalid transaction type. Please enter 'Income' or 'Expense'.")
            while True:
                date = input("Enter date (YYYY-MM-DD): ")

                # Validate date components individually
                try:
                    if not validate_date(date):
                        raise ValueError("Invalid date for February. Please enter a valid date in YYYY-MM-DD format.")
                    break  # Exit inner loop if validation succeeds
                except ValueError:
                    print("Error: Invalid date format. Please try again.")

            transactions.append([amount, category, transaction_type, date])
            print("Transaction added successfully!")
            break
        except ValueError as err:
            print("Error:", err)


# Function to find a transaction by its displayed number (index + 1)
def find_transaction_by_number(number):
    if number < 1 or number > len(transactions):
        return None
    return transactions[number - 1]


# Function to update a transaction
def update_transaction():
    if not transactions:
        print("No transactions found to update!")
        return
    view_transactions()
    while True:
        try:
            number = int(input("Enter the number of the transaction to update: "))
            transaction = find_transaction_by_number(number)
            if not transaction:
                print("Invalid transaction number!")
                continue
            amount, category, transaction_type, date = transaction
            new_amount = float(input("Update amount (press Enter to keep existing): ") or amount)
            new_category = input("Update category (press Enter to keep existing): ") or category
            new_transaction_type = input(
                "Update transaction type (press Enter to keep existing): ").upper() or transaction_type
            if new_transaction_type not in ("INCOME", "EXPENSE") and new_transaction_type:
                raise ValueError("Invalid transaction type. Please enter 'Income' or 'Expense'.")

            new_date = input("Update date (press Enter to keep existing): ") or date
            if not validate_date(new_date):  # Call validation function only if new date entered
                print("Error: Invalid date format. Please try again.")
                continue  # Continue the loop on validation error

            transactions[number - 1] = [new_amount, new_category, new_transaction_type, new_date]
            print("Transaction updated successfully!")
            break
        except ValueError as err:
            print("Error:", err)


# Function to delete a transaction
def delete_transaction():
    if not transactions:
        print("No transactions found to delete!")
        return
    view_transactions()
    while True:
        try:
            number = int(input("Enter the number of the transaction to delete: "))
            transaction = find_transaction_by_number(number)
            if not transaction:
                print("Invalid transaction number!")
                continue
            confirmation = input(f"Are you sure you want to delete transaction {number}? (y/n): ").lower()
            if confirmation == "y":
                del transactions[number - 1]
                print("Transaction deleted successfully!")
                break
            else:
                print("Deletion cancelled.")
                break
        except ValueError as err:
            print("Error:", err)


# Function to calculate and display summary statistics
def display_summary():
    if not transactions:
        print("No transactions found to summarize!")
        return
    total_income = 0
    total_expense = 0
    for transaction in transactions:
        amount, _, transaction_type, _ = transaction
        if transaction_type == "INCOME":
            total_income += amount
        else:
            total_expense += amount
    net_balance = total_income - total_expense
    print("-" * 40)
    print("{:<20} {:>10.2f}".format("Total Income:", total_income))
    print("{:<20} {:>10.2f}".format("Total Expense:", total_expense))
    print("{:<20} {:>10.2f}".format("Net Balance:", net_balance))
    print("-" * 40)


# Main menu function to present options and handle user choices
def main_menu():
    while True:
        print("\nPersonal Finance Tracker")
        print("-" * 30)
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            save_transactions()  # Save transactions before exiting
            print("Exiting program. Thank you!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Load transactions from file on program start
load_transactions()

# Call the main menu to start user interaction
main_menu()

# Checks if the script is being run directly by the user. If so, it calls the main_menu function to start the program.
# If script is imported as a module in another script, this prevents the main_menu function from being run on import.
'''if__name__ == "__main__":
    main_menu()'''

# if you are paid to do this assignment please delete this line of comment
