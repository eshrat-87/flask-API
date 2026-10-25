import streamlit as st
import requests
import json

st.set_page_config(page_title="Student Management System", layout="wide")

st.title("📚 Student Management System")

API_URL = "http://localhost:5000"

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["View Students", "Add Student", "Update Student", "Delete Student"])

def refresh_data():
    """Refresh the page."""
    st.rerun()

# View Students
if page == "View Students":
    st.subheader("All Students")
    
    if st.button("🔄 Refresh", key="refresh_view"):
        refresh_data()
    
    try:
        response = requests.get(f"{API_URL}/students")
        if response.status_code == 200:
            students = response.json()
            
            if students:
                # Display as table
                st.dataframe(
                    students,
                    use_container_width=True,
                    hide_index=True
                )
                st.success(f"Total Students: {len(students)}")
            else:
                st.info("No students found. Add a student to get started!")
        else:
            st.error("Failed to fetch students")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Flask API. Make sure it's running on http://localhost:5000")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Add Student
elif page == "Add Student":
    st.subheader("Add New Student")
    
    with st.form("add_student_form"):
        name = st.text_input("Name", placeholder="Enter student name")
        department = st.text_input("Department", placeholder="e.g., Computer Science")
        email = st.text_input("Email", placeholder="student@example.com")
        
        submitted = st.form_submit_button("➕ Add Student")
        
        if submitted:
            if name and department and email:
                try:
                    data = {
                        "name": name,
                        "department": department,
                        "email": email
                    }
                    response = requests.post(f"{API_URL}/students", json=data)
                    
                    if response.status_code == 201:
                        st.success(f"✅ Student '{name}' added successfully!")
                        st.balloons()
                        # Clear form
                        st.rerun()
                    elif response.status_code == 400:
                        st.error(f"❌ {response.json().get('error', 'Bad request')}")
                    else:
                        st.error("Failed to add student")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to Flask API. Make sure it's running on http://localhost:5000")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("Please fill in all fields")

# Update Student
elif page == "Update Student":
    st.subheader("Update Student")
    
    try:
        # Get all students for selection
        response = requests.get(f"{API_URL}/students")
        if response.status_code == 200:
            students = response.json()
            
            if students:
                student_options = {f"{s['name']} (ID: {s['id']})": s['id'] for s in students}
                selected_student = st.selectbox("Select Student to Update", list(student_options.keys()))
                
                if selected_student:
                    student_id = student_options[selected_student]
                    
                    # Get current student data
                    student_response = requests.get(f"{API_URL}/students/{student_id}")
                    if student_response.status_code == 200:
                        current_student = student_response.json()
                        
                        with st.form("update_student_form"):
                            name = st.text_input("Name", value=current_student['name'])
                            department = st.text_input("Department", value=current_student['department'])
                            email = st.text_input("Email", value=current_student['email'])
                            
                            submitted = st.form_submit_button("✏️ Update Student")
                            
                            if submitted:
                                try:
                                    data = {
                                        "name": name,
                                        "department": department,
                                        "email": email
                                    }
                                    update_response = requests.put(f"{API_URL}/students/{student_id}", json=data)
                                    
                                    if update_response.status_code == 200:
                                        st.success("✅ Student updated successfully!")
                                        st.rerun()
                                    elif update_response.status_code == 400:
                                        st.error(f"❌ {update_response.json().get('error', 'Bad request')}")
                                    else:
                                        st.error("Failed to update student")
                                except requests.exceptions.ConnectionError:
                                    st.error("❌ Cannot connect to Flask API")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
            else:
                st.info("No students found")
        else:
            st.error("Failed to fetch students")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Flask API. Make sure it's running on http://localhost:5000")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Delete Student
elif page == "Delete Student":
    st.subheader("Delete Student")
    st.warning("⚠️ This action cannot be undone!")
    
    try:
        response = requests.get(f"{API_URL}/students")
        if response.status_code == 200:
            students = response.json()
            
            if students:
                student_options = {f"{s['name']} (ID: {s['id']})": s['id'] for s in students}
                selected_student = st.selectbox("Select Student to Delete", list(student_options.keys()))
                
                if selected_student:
                    student_id = student_options[selected_student]
                    
                    if st.button("🗑️ Delete Student", type="secondary"):
                        try:
                            delete_response = requests.delete(f"{API_URL}/students/{student_id}")
                            
                            if delete_response.status_code == 200:
                                st.success("✅ Student deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete student")
                        except requests.exceptions.ConnectionError:
                            st.error("❌ Cannot connect to Flask API")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            else:
                st.info("No students found")
        else:
            st.error("Failed to fetch students")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to Flask API. Make sure it's running on http://localhost:5000")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Student Management System | Built with Flask + Streamlit + SQLite")
