import sqlite3

def init_db():
    conn = sqlite3.connect('checkboxes.db')
    cursor = conn.cursor()

    # Create the 'checkboxes' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checkboxes (
            id INTEGER PRIMARY KEY,
            checked BOOLEAN DEFAULT 0
        )
    ''')

    # Insert 50,000 rows for the checkboxes if they don't exist
    cursor.execute('DELETE FROM checkboxes')  # Optional: Clear existing data if any
    for i in range(50000):
        cursor.execute('INSERT OR IGNORE INTO checkboxes (id, checked) VALUES (?, ?)', (i, False))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
