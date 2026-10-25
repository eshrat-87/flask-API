from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def init_db():
    """Initialize the database with students table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
init_db()

# API Endpoints

@app.route('/students', methods=['GET'])
def get_all_students():
    """Get all students."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a single student by ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        
        if student is None:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify(dict(student)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students', methods=['POST'])
def add_student():
    """Add a new student."""
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['name', 'department', 'email']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO students (name, department, email) VALUES (?, ?, ?)',
            (data['name'], data['department'], data['email'])
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': new_id, 'message': 'Student added successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        
        if student is None:
            conn.close()
            return jsonify({'error': 'Student not found'}), 404
        
        name = data.get('name', student['name'])
        department = data.get('department', student['department'])
        email = data.get('email', student['email'])
        
        cursor.execute(
            'UPDATE students SET name = ?, department = ?, email = ? WHERE id = ?',
            (name, department, email, student_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Student updated successfully'}), 200
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        
        if student is None:
            conn.close()
            return jsonify({'error': 'Student not found'}), 404
        
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
