import pandas as pd
import configparser
import mysql.connector
import streamlit as st

# MySQL connection
def create_connection():
    config = configparser.ConfigParser()
    config.read_file(open('config.ini'))
    
    connection = mysql.connector.connect(
        host=config['dbconfig']['SQL_HOST'],
        port=int(config['dbconfig']['SQL_PORT']),
        user=config['dbconfig']['SQL_USER'],
        password=config['dbconfig']['SQL_PASS'],
        database=config['dbconfig']['SQL_DATABASE']
    )
    return connection

# Fetch all student records from the database
students = []
def get_students():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    connection.close()
    global students
    students = records

# Add a new student to the database
def add_student(name, age, grade):
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO records (name, age, grade) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, age, grade))
    connection.commit()
    connection.close()
    get_students()

# Update a student's details
def update_student(student_id, name, age, grade):
    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE records SET name=%s, age=%s, grade=%s WHERE id=%s"
    cursor.execute(query, (name, age, grade, student_id))
    connection.commit()
    connection.close()
    get_students()

# Delete a student from the database
def delete_student(student_id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM records WHERE id=%s"
    cursor.execute(query, (student_id,))
    connection.commit()
    connection.close()
    get_students()

# Main Streamlit app
def main():
    st.title("Student Record Management System")
    
    # Display all student records in a table
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Student Records")
        
    with col2:
        st.button("Refresh", on_click=get_students())
        
    # Fetch student records
    get_students()

    if students:
        df = pd.DataFrame(students, columns=["ID", "Name", "Age", "Grade"])
        st.dataframe(df, hide_index=True, use_container_width=True)  # Display records in a table format using st.dataframe
    else:
        st.write("No student records found.")
    
    # Add a new student
    st.subheader("Add New Student")
    with st.form("add_student_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        grade = st.number_input("Grade", min_value=1, max_value=100)
        submitted = st.form_submit_button("Add Student")
        if submitted:
            add_student(name, age, grade)
            st.success("Student added successfully!")
    
    # Modify an existing student
    st.subheader("Modify Student")
    student_id = st.number_input("Student ID", min_value=1, step=1)
    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=1, max_value=100)
    grade = st.number_input("New Grade", min_value=1, max_value=100)
    if st.button("Update Student"):
        update_student(student_id, name, age, grade)
        st.success("Student updated successfully!")

    # Delete a student
    st.subheader("Delete Student")
    student_id = st.number_input("Student ID to delete", min_value=1, step=1)
    if st.button("Delete Student"):
        delete_student(student_id)
        st.success("Student deleted successfully!")

if __name__ == "__main__":
    main()
