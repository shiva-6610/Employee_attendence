from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['attendance_db']
employee_collection = db['employees']
attendance_collection = db['attendance']

# Home - List employees
@app.route('/')
def index():
    employees = list(employee_collection.find())
    return render_template("index.html", employees=employees)

# Add new employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        employee_collection.insert_one({'name': name, 'emp_id': emp_id})
        return redirect(url_for('index'))
    return render_template("add_employee.html")

# Mark Attendance
@app.route('/attendance/<emp_id>', methods=['GET', 'POST'])
def mark_attendance(emp_id):
    employee = employee_collection.find_one({'emp_id': emp_id})
    if not employee:
        return "Employee not found"
    
    if request.method == 'POST':
        action = request.form['action']
        timestamp = datetime.now()
        attendance_collection.insert_one({
            'emp_id': emp_id,
            'name': employee['name'],
            'action': action,
            'timestamp': timestamp
        })
        return redirect(url_for('index'))
    
    records = attendance_collection.find({'emp_id': emp_id}).sort('timestamp', -1)
    return render_template("attendance.html", employee=employee, records=records)

# View all attendance records
@app.route('/records')
def view_records():
    all_records = list(attendance_collection.find().sort('timestamp', -1))
    return render_template("attendance.html", records=all_records, all_view=True)

if __name__ == '__main__':
    app.run(debug=True)





#---------- run ---------------
# python app.py