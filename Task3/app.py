from flask import Flask, request, jsonify
import sqlite3
import os
from functools import wraps
import hashlib

app = Flask(__name__)

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'employees.db')

# Demo users with hashed passwords
DEMO_USERS = {
    'employee': 'password123',
    'admin': 'admin123'
}

# User roles
USER_ROLES = {
    'employee': 'Employee',
    'admin': 'Administrator'
}

def init_db():
    """Initialize the database with employees table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL
        )
    ''')
    
    # Add some sample data
    cursor.execute('SELECT COUNT(*) FROM employees')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO employees (name, position) VALUES (?, ?)', ('John Doe', 'Software Engineer'))
        cursor.execute('INSERT INTO employees (name, position) VALUES (?, ?)', ('Jane Smith', 'Product Manager'))
        cursor.execute('INSERT INTO employees (name, position) VALUES (?, ?)', ('Mike Johnson', 'Designer'))
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
init_db()

# Authentication & Authorization middleware

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        
        if not auth:
            return jsonify({'error': 'Missing credentials'}), 401
        
        username = auth.username
        password = auth.password
        
        # Verify credentials
        if username not in DEMO_USERS or DEMO_USERS[username] != password:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Store user info in request for use in the view
        request.user = {
            'username': username,
            'role': USER_ROLES[username]
        }
        
        return f(*args, **kwargs)
    
    return decorated

def require_admin(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        
        if not auth:
            return jsonify({'error': 'Missing credentials'}), 401
        
        username = auth.username
        password = auth.password
        
        # Verify credentials
        if username not in DEMO_USERS or DEMO_USERS[username] != password:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Check if user is admin
        if USER_ROLES[username] != 'Administrator':
            return jsonify({'error': 'Access denied. Admin role required'}), 403
        
        request.user = {
            'username': username,
            'role': USER_ROLES[username]
        }
        
        return f(*args, **kwargs)
    
    return decorated

# API Endpoints

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint."""
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400
        
        username = data['username']
        password = data['password']
        
        # Verify credentials
        if username not in DEMO_USERS or DEMO_USERS[username] != password:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        role = USER_ROLES[username]
        
        return jsonify({
            'message': 'Login successful',
            'username': username,
            'role': role,
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employees', methods=['GET'])
@require_auth
def get_all_employees():
    """Get all employees (authorized users only)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees')
        employees = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'employees': employees,
            'user': request.user,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employees', methods=['POST'])
@require_admin
def add_employee():
    """Add employee (admin only)."""
    try:
        data = request.get_json()
        
        if not data or not all(key in data for key in ['name', 'position']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO employees (name, position) VALUES (?, ?)',
            (data['name'], data['position'])
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'id': new_id,
            'message': 'Employee added successfully',
            'user': request.user,
            'status': 'success'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employees/<int:employee_id>', methods=['PUT'])
@require_admin
def update_employee(employee_id):
    """Update employee (admin only)."""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        employee = cursor.fetchone()
        
        if employee is None:
            conn.close()
            return jsonify({'error': 'Employee not found'}), 404
        
        name = data.get('name', employee['name'])
        position = data.get('position', employee['position'])
        
        cursor.execute(
            'UPDATE employees SET name = ?, position = ? WHERE id = ?',
            (name, position, employee_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Employee updated successfully',
            'user': request.user,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
@require_admin
def delete_employee(employee_id):
    """Delete employee (admin only)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))
        employee = cursor.fetchone()
        
        if employee is None:
            conn.close()
            return jsonify({'error': 'Employee not found'}), 404
        
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Employee deleted successfully',
            'user': request.user,
            'status': 'success'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Task 3: Authentication & Authorization")
    print("=" * 60)
    print("Demo Users:")
    print("  Employee: username='employee', password='password123'")
    print("  Admin:    username='admin', password='admin123'")
    print("=" * 60)
    app.run(debug=True, port=5002)
