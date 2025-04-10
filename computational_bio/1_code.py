import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

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

class SpecimenCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Specimen Size Calculator")
        self.geometry("400x500")
        
        # Create main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Username entry
        ttk.Label(main_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username = ttk.Entry(main_frame)
        self.username.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Microscope size entry
        ttk.Label(main_frame, text="Microscope Size (mm):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.microscope_size = ttk.Entry(main_frame)
        self.microscope_size.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Magnification entry
        ttk.Label(main_frame, text="Magnification:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.magnification = ttk.Entry(main_frame)
        self.magnification.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Calculate button
        ttk.Button(main_frame, text="Calculate", command=self.calculate).grid(row=3, column=0, columnspan=2, pady=20)

        # Result display
        self.result_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.result_var).grid(row=4, column=0, columnspan=2, pady=5)

        # Recent measurements
        ttk.Label(main_frame, text="Recent Measurements:").grid(row=5, column=0, columnspan=2, pady=5)
        self.tree = ttk.Treeview(main_frame, columns=('Username', 'Microscope Size', 'Actual Size', 'Date'), show='headings')
        
        # Configure columns
        self.tree.heading('Username', text='Username')
        self.tree.heading('Microscope Size', text='Microscope Size')
        self.tree.heading('Actual Size', text='Actual Size')
        self.tree.heading('Date', text='Date')
        
        self.tree.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Initialize database
        setup_database()
        self.load_recent_measurements()

    def calculate(self):
        try:
            username = self.username.get()
            microscope_size = float(self.microscope_size.get())
            magn = int(self.magnification.get())

            if not username:
                messagebox.showerror("Error", "Please enter a username")
                return

            actual_size = original_size(microscope_size, magn)
            self.result_var.set(f"Original size of specimen: {actual_size:.2f} µm")
            
            save_measurement(username, microscope_size, actual_size)
            self.load_recent_measurements()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")

    def load_recent_measurements(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load recent measurements
        conn = sqlite3.connect('specimen_records.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, microscope_size, actual_size, date_added 
            FROM specimens 
            ORDER BY date_added DESC 
            LIMIT 5
        ''')
        
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        
        conn.close()

if __name__ == "__main__":
    app = SpecimenCalculator()
    app.mainloop()
