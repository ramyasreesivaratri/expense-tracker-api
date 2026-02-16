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

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount) VALUES (?, ?)",
        (title, amount),
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


# ---------- RUN APP (IMPORTANT FOR RENDER) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
