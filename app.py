from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="usersdb"
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    if not data:
        return {"message":"Missing Data"}, 400

    name = data.get("name")
    email = data.get("email")

    print("DEBUG:", name, email)

    if not name or not email:
        return {"message":"Missing Data"}, 400


    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )

    conn.commit()
    conn.close()

    return {"message": "User Registered Successfully"}

@app.route('/users')
def get_users():
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, email FROM users")
    rows = cursor.fetchall()

    users = [{"name": r[0], "email": r[1]} for r in rows]

    return jsonify(users)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)
