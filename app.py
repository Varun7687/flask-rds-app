import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()  # Loads a local .env file if you have one

app = Flask(__name__)

def check_database():
    required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
    if any(not os.getenv(key) for key in required):
        return False, "Database settings are not configured."

    connection = None
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", "3306")),
            connect_timeout=5,
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return True, "The database connection is working."

    except (pymysql.MySQLError, ValueError):
        app.logger.exception("Database connection check failed")
        return False, "Connection failed. Check the app logs and database settings."

    finally:
        if connection:
            connection.close()

@app.route("/")
def home():
    db_connected, db_message = check_database()
    return render_template(
        "index.html",
        db_connected=db_connected,
        db_message=db_message,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)

