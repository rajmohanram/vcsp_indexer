import sqlite3
import os


def check_db_file(db_file):
    """Checks for the existence of the SQLite database file 'app.db'.
    Creates the file and updates the schema if it doesn't exist.
    """

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TIMESTAMP NOT NULL,
                bucket TEXT NOT NULL,
                event TEXT NOT NULL,
                status_message TEXT NOT NULL
            )
        """)
    except sqlite3.OperationalError as e:
        print(f"Error creating table: {e}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'app.db')
    check_db_file(dbfile)
