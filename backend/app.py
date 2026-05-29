from flask import Flask, request, jsonify
import mysql.connector
import os
import time
import sys

# Flush logs immediately
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)

# Track DB initialization
_db_initialized = False

# Config WITHOUT database first
DB_CONFIG_NO_DB = {
    "host": os.environ.get("MYSQL_HOST", "mysql-service.critical-apps.svc.cluster.local"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "root123"),
    "connection_timeout": 5,
}

# Config WITH database
DB_CONFIG = {
    **DB_CONFIG_NO_DB,
    "database": os.environ.get("MYSQL_DATABASE", "feedbackdb"),
}

def get_connection():
    for attempt in range(10):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Exception as e:
            print(f"DB connection attempt {attempt+1}/10 failed: {e}", flush=True)
            time.sleep(5)

    raise Exception("Could not connect to MySQL")

def init_db():
    print("Initializing database...", flush=True)

    # Create DB if not exists
    for attempt in range(10):
        try:
            conn = mysql.connector.connect(**DB_CONFIG_NO_DB)

            cursor = conn.cursor()

            db_name = os.environ.get("MYSQL_DATABASE", "feedbackdb")

            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}`"
            )

            conn.commit()

            cursor.close()
            conn.close()

            print(f"Database '{db_name}' ready.", flush=True)

            break

        except Exception as e:
            print(f"DB init attempt {attempt+1}/10 failed: {e}", flush=True)
            time.sleep(5)

    else:
        raise Exception("Could not initialize database")

    # Create table
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            feedback_date DATE,
            feedback_text TEXT
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()

    print("Table ready.", flush=True)

@app.route('/health')
def health():
    return "Backend Healthy", 200

@app.route('/feedback', methods=['GET'])
def get_feedback():

    global _db_initialized

    if not _db_initialized:
        init_db()
        _db_initialized = True

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, feedback_date, feedback_text
        FROM feedback
    """)

    rows = cursor.fetchall()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "date": str(row[2]),
            "feedback": row[3]
        })

    cursor.close()
    conn.close()

    return jsonify(result)

@app.route('/feedback', methods=['POST'])
def add_feedback():

    global _db_initialized

    if not _db_initialized:
        init_db()
        _db_initialized = True

    data = request.json

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback(name, feedback_date, feedback_text)
        VALUES (%s, %s, %s)
    """, (
        data['name'],
        data['date'],
        data['feedback']
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Feedback Added"
    }), 201

@app.route('/feedback/<int:id>', methods=['DELETE'])
def delete_feedback(id):

    global _db_initialized

    if not _db_initialized:
        init_db()
        _db_initialized = True

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM feedback
        WHERE id=%s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Feedback Deleted"
    }), 200

if __name__ == '__main__':
    print("Starting Flask...", flush=True)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )