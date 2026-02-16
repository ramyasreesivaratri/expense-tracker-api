import sqlite3

# Connect to database
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT
)
""")

conn.commit()


# ---------------- FUNCTIONS ---------------- #

def add_expense():
    title = input("Enter expense title: ")
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")

    cursor.execute(
        "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
        (title, amount, category)
    )
    conn.commit()
    print("Expense Added Successfully!\n")


def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("No expenses found.\n")
    else:
        print("\n------ All Expenses ------")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Amount: {row[2]}, Category: {row[3]}")
        print("--------------------------\n")


def delete_expense():
    expense_id = int(input("Enter expense ID to delete: "))

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

    print("Expense Deleted Successfully!\n")


def show_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"\nTotal Expense: {total}\n")


def filter_by_category():
    category = input("Enter category to filter: ")

    cursor.execute("SELECT * FROM expenses WHERE category = ?", (category,))
    rows = cursor.fetchall()

    if not rows:
        print("No expenses found in this category.\n")
    else:
        print(f"\n------ Expenses in {category} ------")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Amount: {row[2]}, Category: {row[3]}")
        print("------------------------------------\n")


# ---------------- MAIN MENU ---------------- #

while True:
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Show Total Expense")
    print("5. Filter by Category")
    print("6. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        delete_expense()
    elif choice == "4":
        show_total()
    elif choice == "5":
        filter_by_category()
    elif choice == "6":
        print("Exiting Program...")
        break
    else:
        print("Invalid choice\n")
