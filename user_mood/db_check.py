import sqlite3

# Path to your SQLite database file
db_file = 'moods.db'

def inspect_database():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Execute a query to retrieve all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Print the names of all tables in the database
        print("Tables in the database:")
        for table in tables:
            print(table[0])

        # Execute a query to retrieve the schema of the mood table
        cursor.execute("PRAGMA table_info('mood')")
        columns = cursor.fetchall()

        # Print the schema of the mood table
        print("\nSchema of the mood table:")
        for column in columns:
            print(column)

        # Execute a query to retrieve some sample data from the mood table
        cursor.execute("SELECT * FROM mood LIMIT 5")
        rows = cursor.fetchall()

        # Print some sample data from the mood table
        print("\nSample data from the mood table:")
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print("Error:", e)

    finally:
        # Close the database connection
        conn.close()

# Call the function to inspect the database
inspect_database()
