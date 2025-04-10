from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

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

def original_size(microscope_size, magn):
    '''
    Calculates the real ife size of the organism given the microscope size
    '''
    specimen_size = microscope_size / magn * 1000
    return specimen_size

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        username = data['username']
        microscope_size = float(data['microscope_size'])
        magn = int(data['magnification'])
        
        actual_size = original_size(microscope_size, magn)
        
        conn = sqlite3.connect('specimen_records.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO specimens (username, microscope_size, actual_size, date_added)
            VALUES (?, ?, ?, ?)
        ''', (username, microscope_size, actual_size, datetime.now()))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'result': f"{actual_size:.2f}"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/recent-measurements')
def get_recent_measurements():
    conn = sqlite3.connect('specimen_records.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT username, microscope_size, actual_size, date_added 
        FROM specimens 
        ORDER BY date_added DESC 
        LIMIT 5
    ''')
    measurements = cursor.fetchall()
    conn.close()
    
    return jsonify(measurements)

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)