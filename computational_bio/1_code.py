import sqlite3
from datetime import datetime

def setup_database():
    conn = sqlite3.connect('specimen_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            microscope_size REAL NOT NULL,
            actual_size REAL NOT NULL,
            date_added TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_measurement(username, microscope_size, actual_size):
    conn = sqlite3.connect('specimen_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO specimens (username, microscope_size, actual_size, date_added)
        VALUES (?, ?, ?, ?)
    ''', (username, microscope_size, actual_size, datetime.now()))
    conn.commit()
    conn.close()

def original_size(microscope_size, magn):
    '''
   Calculates the real ife size of the organism given the microscope size
    '''
    specimen_size = microscope_size / magn * 1000
    return specimen_size

if __name__ == "__main__":
    setup_database()
    
    username = input("Enter your username: ")
    microscope_size = float(input("Enter the microscope size of specimen (mm): "))
    magn = int(input("Enter the microscope mag coefficient: "))
    
    actual_size = original_size(microscope_size, magn)
    print(f"Original size of specimen in (µm) {actual_size:.2f}")
    
    save_measurement(username, microscope_size, actual_size)
    print("Measurement saved to database!")
