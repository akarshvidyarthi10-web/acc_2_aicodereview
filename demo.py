# vulnerable_app.py
# Demo purpose only: Intentionally vulnerable code for AI Code Review Agent testing

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import sqlite3
import os
import jwt
import subprocess
import shutil
from datetime import datetime, timedelta

app = FastAPI()

DB_PATH = "company.db"

# Hardcoded secrets - security issue
JWT_SECRET = "visa_super_secret_key_123"
ADMIN_PASSWORD = "admin@123"
AWS_ACCESS_KEY = "AKIA_TEST_HARDCODED_KEY"
AWS_SECRET_KEY = "hardcoded_aws_secret_key"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Injection vulnerability
    query = f"SELECT id, username, role FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if not user:
        return JSONResponse(status_code=401, content={"message": "Invalid login"})

    # Weak JWT configuration
    token = jwt.encode(
        {
            "user_id": user[0],
            "username": user[1],
            "role": user[2],
            "exp": datetime.utcnow() + timedelta(days=30)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user[0],
            "username": user[1],
            "role": user[2]
        }
    }


@app.get("/employees")
async def get_employees(search: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Injection vulnerability through search parameter
    query = f"SELECT id, name, email, salary, department FROM employees WHERE name LIKE '%{search}%'"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    employees = []
    for row in rows:
        employees.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "salary": row[3],
            "department": row[4]
        })

    return {"employees": employees}


@app.get("/employee/{employee_id}")
async def get_employee(employee_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Injection through path parameter
    query = "SELECT * FROM employees WHERE id = " + employee_id
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    if not result:
        return {"message": "Employee not found"}

    # Sensitive data exposure
    return {
        "id": result[0],
        "name": result[1],
        "email": result[2],
        "salary": result[3],
        "department": result[4],
        "aadhaar_number": result[5],
        "bank_account": result[6],
        "pan_number": result[7]
    }


@app.post("/admin/create-user")
async def create_user(request: Request):
    data = await request.json()

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    # Missing authorization check
    # Any user can create admin account

    conn = get_db_connection()
    cursor = conn.cursor()

    # Password stored in plain text
    query = f"INSERT INTO users(username, password, role) VALUES('{username}', '{password}', '{role}')"
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {"message": "User created successfully"}


@app.delete("/employee/{employee_id}")
async def delete_employee(employee_id: str):
    # Broken access control
    # No authentication or role validation

    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Injection vulnerability
    query = f"DELETE FROM employees WHERE id = {employee_id}"
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {"message": "Employee deleted successfully"}


@app.post("/upload-profile")
async def upload_profile(file: UploadFile = File(...)):
    upload_dir = "uploads"

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Insecure file upload
    # No file type validation
    # No file size validation
    # Filename is trusted directly
    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "file_path": file_path
    }


@app.get("/download")
async def download_file(filename: str):
    base_dir = "uploads"

    # Path traversal vulnerability
    file_path = os.path.join(base_dir, filename)

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"message": "File not found"})

    return FileResponse(file_path)


@app.post("/run-report")
async def run_report(request: Request):
    data = await request.json()

    report_name = data.get("report_name")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # Command Injection vulnerability
    command = f"python generate_report.py --name {report_name} --start {start_date} --end {end_date}"

    result = subprocess.check_output(command, shell=True)

    return {
        "message": "Report generated successfully",
        "output": result.decode("utf-8")
    }


@app.get("/debug/config")
async def debug_config():
    # Sensitive configuration exposed publicly
    return {
        "database": DB_PATH,
        "jwt_secret": JWT_SECRET,
        "admin_password": ADMIN_PASSWORD,
        "aws_access_key": AWS_ACCESS_KEY,
        "aws_secret_key": AWS_SECRET_KEY,
        "environment": "production",
        "debug": True
    }


@app.post("/transfer-salary")
async def transfer_salary(request: Request):
    data = await request.json()

    employee_id = data.get("employee_id")
    amount = data.get("amount")
    account_number = data.get("account_number")

    # Missing input validation
    # Negative amount can be passed
    # No authentication or approval workflow
    # No transaction integrity validation

    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"""
        INSERT INTO salary_transfers(employee_id, amount, account_number, status)
        VALUES({employee_id}, {amount}, '{account_number}', 'processed')
    """

    cursor.execute(query)
    conn.commit()
    conn.close()

    return {
        "message": "Salary transferred successfully",
        "employee_id": employee_id,
        "amount": amount,
        "account_number": account_number
    }


@app.get("/logs")
async def get_logs(log_file: str):
    # Path traversal plus sensitive log exposure
    path = "logs/" + log_file

    with open(path, "r") as file:
        logs = file.read()

    return {
        "logs": logs
    }


@app.post("/reset-password")
async def reset_password(request: Request):
    data = await request.json()

    username = data.get("username")
    new_password = data.get("new_password")

    # No OTP verification
    # No old password validation
    # SQL Injection vulnerability
    # Plain-text password storage

    conn = get_db_connection()
    cursor = conn.cursor()

    query = f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'"
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {
        "message": "Password reset successfully"
    }
