from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'lab_systems.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS systems
                 (id TEXT PRIMARY KEY, lab TEXT, seat TEXT, makeModel TEXT, specs TEXT, 
                  os TEXT, status TEXT, issueCategory TEXT, complaint TEXT, reportedDate TEXT,
                  reportedBy TEXT, assignedTo TEXT, resolution TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/api/systems', methods=['GET'])
def get_systems():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM systems')
    rows = c.fetchall()
    conn.close()
    
    systems = []
    for row in rows:
        systems.append({
            'id': row[0], 'lab': row[1], 'seat': row[2], 'makeModel': row[3],
            'specs': row[4], 'os': row[5], 'status': row[6], 'issueCategory': row[7],
            'complaint': row[8], 'reportedDate': row[9], 'reportedBy': row[10],
            'assignedTo': row[11], 'resolution': row[12], 'timestamp': row[13]
        })
    return jsonify(systems)

@app.route('/api/systems', methods=['POST'])
def add_system():
    data = request.json
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO systems 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['id'], data['lab'], data['seat'], data['makeModel'],
               data['specs'], data['os'], data['status'], data['issueCategory'],
               data['complaint'], data['reportedDate'], data['reportedBy'],
               data['assignedTo'], data['resolution'], datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/api/systems/<system_id>', methods=['DELETE'])
def delete_system(system_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM systems WHERE id = ?', (system_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/')
def index():
    with open('LabTracker.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
