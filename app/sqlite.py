import sqlite3
import os

# Check if sqlite db file named app.db exists in the current directory
if not os.path.exists('app.db'):
    # If the file does not exist, create one and apply a schema for the 'logging' table
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE logging (date TEXT, log TEXT)''')
    conn.commit()
    conn.close()
    print("Created a new database 'app.db' with a 'logging' table.")
else:
    # If the file exists, check if it contains a schema for the 'logging' table
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(logging)")
    table_info = c.fetchall()
    column_names = [row[1] for row in table_info]
    if 'date' in column_names and 'log' in column_names:
        print("Database 'app.db' exists with the 'logging' table schema.")
    else:
        print("Database 'app.db' exists, but does not contain the expected 'logging' table schema.")
    conn.close()
