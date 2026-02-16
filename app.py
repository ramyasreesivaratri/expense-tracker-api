from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DATABASE = "expenses.db"

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- CREATE TABLE ----------
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_table()

# ---------- HOME ROUTE ----------
@app.route("/")
def home():
    return "Expense Tracker API is Running Successfully 🚀"

# ---------- ADD EXPENSE ----------
@app.route("/add", methods=["POST"])
def add_expense():
    data = request.get_json()

    title = data.get("title")
    amount = data.get("amount")
    category = data.get("category")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
        (title, amount, category),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully"})

# ---------- GET ALL EXPENSES ----------
@app.route("/expenses", methods=["GET"])
def get_expenses():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    return jsonify([dict(expense) for expense in expenses])

# ---------- DELETE EXPENSE ----------
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_expense(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Expense deleted successfully"})

# ---------- TOTAL EXPENSE ----------
@app.route("/total", methods=["GET"])
def total_expense():
    conn = get_db_connection()
    total = conn.execute("SELECT SUM(amount) as total FROM expenses").fetchone()
    conn.close()

    return jsonify({"total": total["total"] if total["total"] else 0})

# ---------- FILTER BY CATEGORY ----------
@app.route("/category/<string:category>", methods=["GET"])
def filter_category(category):
    conn = get_db_connection()
    expenses = conn.execute(
        "SELECT * FROM expenses WHERE category = ?", (category,)
    ).fetchall()
    conn.close()

    return jsonify([dict(expense) for expense in expenses])

# ---------- RUN APP ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
