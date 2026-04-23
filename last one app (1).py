from flask import Flask, render_template, jsonify
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)

# -------------------------------
# 🔌 Theft Detection Function
# -------------------------------
def detect_theft():
    current = random.uniform(0, 50)   # simulate current
    voltage = 230
    power = current * voltage

    # simple theft condition
    theft = 1 if current > 40 else 0

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO electricity (timestamp, current, voltage, power, theft_detected)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        round(current, 2),
        voltage,
        round(power, 2),
        theft
    ))

    conn.commit()
    conn.close()

    return theft


# -------------------------------
# 🏠 Home Route
# -------------------------------
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM electricity ORDER BY id DESC LIMIT 10")
    data = cursor.fetchall()

    conn.close()
    return render_template('index.html', data=data)


# -------------------------------
# 🔁 Auto Detection Route
# -------------------------------
@app.route('/check')
def check():
    theft = detect_theft()
    return jsonify({"theft": theft})


# -------------------------------
# ▶️ Run App
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)