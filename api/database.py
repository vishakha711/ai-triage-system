import sqlite3

# DB connect (file auto create hogi)
conn = sqlite3.connect("patients.db", check_same_thread=False)
cursor = conn.cursor()

# Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    symptom_text TEXT,
    confidence REAL,
    wait_time INTEGER,
    priority TEXT,
    heart_rate INTEGER,
    spo2 INTEGER,
    temperature REAL
)
""")
conn.commit()

# Patient add karne ka function
def add_patient(name, age, symptom, priority, confidence, wait_time, hr, spo2, temp):
    cursor.execute("""
    INSERT INTO patients 
    (name, age, symptom_text, priority, confidence, wait_time, heart_rate, spo2, temperature)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, symptom, priority, confidence, wait_time, hr, spo2, temp))
    conn.commit()

# Queue size nikalne ka function
def get_queue_size():
    cursor.execute("SELECT COUNT(*) FROM patients")
    return cursor.fetchone()[0]

def get_all_patients():
    cursor.execute("""
    SELECT id, name, age, symptom_text, priority, confidence, wait_time, heart_rate, spo2, temperature 
    FROM patients
    ORDER BY 
    CASE 
        WHEN priority='HIGH' THEN 1
        WHEN priority='MEDIUM' THEN 2
        WHEN priority='LOW' THEN 3
    END
    """)
    
    return cursor.fetchall()

def remove_patient(patient_id):
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
