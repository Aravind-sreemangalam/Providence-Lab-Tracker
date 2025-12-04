from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DB_FILE = 'lab_systems.db'

def init_db():
    """Initialize database"""
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
    """Get all systems"""
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
    """Add or update system"""
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
    """Delete system"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM systems WHERE id = ?', (system_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/')
def index():
    """Serve frontend"""
    try:
        html_path = os.path.join(os.path.dirname(__file__), 'LabTracker.html')
        with open(html_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return '''
        <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>Error: LabTracker.html not found</h1>
            <p>Make sure LabTracker.html is in the same folder as app.py</p>
            <p>Files required:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>app.py</li>
                <li>LabTracker.html</li>
                <li>requirements.txt</li>
            </ul>
        </body>
        </html>
        ''', 404

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
