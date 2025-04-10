import os
from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
from config import DATABASE_URL

app = Flask(__name__)

def get_db_connection():
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    return psycopg2.connect(DATABASE_URL)

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS specimens (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            microscope_size REAL NOT NULL,
            actual_size REAL NOT NULL,
            date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        username = data['username']
        microscope_size = float(data['microscope_size'])
        magn = int(data['magnification'])
        
        actual_size = original_size(microscope_size, magn)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO specimens (username, microscope_size, actual_size)
            VALUES (%s, %s, %s)
        ''', (username, microscope_size, actual_size))
        conn.commit()
        cursor.close()
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
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute('''
        SELECT username, microscope_size, actual_size, date_added 
        FROM specimens 
        ORDER BY date_added DESC 
        LIMIT 5
    ''')
    measurements = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return jsonify(measurements)

def original_size(microscope_size, magn):
    '''
    Calculates the real ife size of the organism given the microscope size
    '''
    specimen_size = microscope_size / magn * 1000
    return specimen_size

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    setup_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)