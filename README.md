# Flask API Assignment

This repository contains a complete Flask API assignment with three tasks:
- Task 1: Student Management System (Flask + SQLite + Streamlit)
- Task 2: API Key Authentication
- Task 3: Authentication & Authorization with Role-based Access Control

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Assignment1
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
Assignment1/
│
├── Task1/              # Student Management System
│   ├── app.py          # Flask API
│   ├── streamlit_app.py # Streamlit Frontend
│   └── database.db     # SQLite database
│
├── Task2/              # API Key Authentication
│   └── app.py          # Flask API with API key auth
│
├── Task3/              # Authentication & Authorization
│   ├── app.py          # Flask API with RBAC
│   └── employees.db    # SQLite database
│
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎯 Task 1: Student Management System

### Setup and Run
```bash
cd Task1
python app.py
```

Open another terminal:
```bash
cd Task1
streamlit run streamlit_app.py
```

### API Endpoints (Running on port 5000)
- `GET /students` - Get all students
- `GET /students/<id>` - Get a specific student
- `POST /students` - Add a new student
- `PUT /students/<id>` - Update a student
- `DELETE /students/<id>` - Delete a student

### Features
- Complete CRUD operations
- SQLite database
- Streamlit web interface
- Real-time data synchronization

## 🔑 Task 2: API Key Authentication

### Setup and Run
```bash
cd Task2
python app.py
```

### Demo API Keys (generated on startup):
Check the console output when starting the server for 3 random API keys.

### API Endpoint (Running on port 5001)
- `POST /process` - Process text (convert to uppercase)

### Authentication
Send API key in header:
```
X-API-Key: your-api-key-here
```

### Request Format
```json
{
    "text": "hello world"
}
```

### Response Format
```json
{
    "input": "hello world",
    "output": "HELLO WORLD",
    "status": "success"
}
```

## 👥 Task 3: Authentication & Authorization

### Setup and Run
```bash
cd Task3
python app.py
```

### Demo Users
- **Employee**: username=`employee`, password=`password123`
- **Administrator**: username=`admin`, password=`admin123`

### API Endpoints (Running on port 5002)
- `POST /login` - Login endpoint
- `GET /employees` - Get all employees (authorized users)
- `POST /employees` - Add employee (admin only)
- `PUT /employees/<id>` - Update employee (admin only)
- `DELETE /employees/<id>` - Delete employee (admin only)

### Role-based Access Control
| Action        | Employee | Administrator |
|---------------|----------|---------------|
| View employees | ✅        | ✅             |
| Add employee   | ❌        | ✅             |
| Update employee | ❌        | ✅             |
| Delete employee | ❌        | ✅             |

### Authentication Methods
- Basic Auth (username/password in Authorization header)
- Login endpoint for easier testing

## 🧪 Testing

### Task 1 Testing
```bash
# Using curl
curl http://localhost:5000/students
curl -X POST http://localhost:5000/students -H "Content-Type: application/json" -d '{"name":"John","department":"CS","email":"john@example.com"}'
```

### Task 2 Testing
```bash
# Replace YOUR_API_KEY with actual key from console
curl -X POST http://localhost:5001/process \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"text":"hello"}'
```

### Task 3 Testing
```bash
# Login (Alternative to Basic Auth)
curl -X POST http://localhost:5002/login \
  -H "Content-Type: application/json" \
  -d '{"username":"employee","password":"password123"}'

# View employees (Employee role)
curl -u employee:password123 http://localhost:5002/employees

# Try to delete (Employee role - should fail)
curl -X DELETE -u employee:password123 http://localhost:5002/employees/1

# Delete employee (Admin role - should succeed)
curl -X DELETE -u admin:admin123 http://localhost:5002/employees/1
```

## 🛠️ Technologies Used
- **Flask** - Web framework for building APIs
- **SQLite** - Lightweight database
- **Streamlit** - Frontend framework for Task 1
- **requests** - HTTP client for API testing

## 📊 Features Implemented
- ✅ Complete CRUD operations (Task 1)
- ✅ Database persistence (Tasks 1 & 3)
- ✅ API Key authentication (Task 2)
- ✅ Role-based access control (Task 3)
- ✅ User authentication (Task 3)
- ✅ Web interface (Task 1)
- ✅ Error handling and validation
- ✅ JSON-based API responses

## 📝 Notes
1. Each task runs on a different port:
   - Task 1: Port 5000
   - Task 2: Port 5001
   - Task 3: Port 5002

2. Databases are automatically created and initialized on first run.

3. Demo data is populated in Task 3 (employees).

4. All endpoints return proper HTTP status codes and error messages.

## 🎥 Video Demonstration
Each task folder contains instructions for recording a demo video showing:
- Add, Update, Delete operations (Task 1)
- API key validation (Task 2)
- Role-based access control (Task 3)

---

**Ready for submission!** 🚀