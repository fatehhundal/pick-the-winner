import sqlite3
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)
DB_NAME = "database.db"

def get_connection():
    """Create and return a SQLite connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # access columns by name
    return conn

def init_db():
    """Create the customers table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            phoneNumber INTEGER,
            numberOfItems INTEGER,
            totalAmount INTEGER,
            currentDate TEXT
        );
    """)

    conn.commit()
    conn.close()

# Initialise database when the app starts
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/details", methods=["POST"])
def details():
    username = request.form["user_name"]
    phoneNumber = request.form["contact_number"]
    numberOfItems = request.form["number_of_items"]
    totalAmount = request.form["amount"]
    currentDate = request.form["current_date"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO customers (username, phoneNumber, numberOfItems, totalAmount, currentDate)
        VALUES (?, ?, ?, ?, ?)
    """, (username, phoneNumber, numberOfItems, totalAmount, currentDate))

    conn.commit()
    conn.close()

    return render_template("page.html")

@app.route("/winner")
def winner():
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, phoneNumber
        FROM customers
        WHERE currentDate = ?
        ORDER BY totalAmount DESC
        LIMIT 1;
    """, (today,))

    row = cur.fetchone()
    conn.close()

    if row:
        return render_template("page.html", user_name=row["username"], phone_number = row["phoneNumber"])
    
    return render_template("page.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)