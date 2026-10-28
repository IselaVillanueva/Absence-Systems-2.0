"""Read fictional Employee and Absence Request records. Start the application with: python run.py"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Employee Absence API")

# Locate the JSON files beside this Python file, even from another working directory.
DATA_DIR = Path(__file__).resolve().parent / "data"
EMPLOYEES_FILE = DATA_DIR / "employees.json"
ABSENCE_REQUESTS_FILE = DATA_DIR / "absence_requests.json"


def load_data(file_path: Path):
    # json.load converts the JSON array into a Python list of dictionaries.
    # 'with' closes the file when this indented block finishes.
    with file_path.open(encoding="utf-8") as file:
        return json.load(file)


# A decorator connects an HTTP method and URL path to the function below it.
@app.get("/")
def root():
    return {"message": "Welcome to the Employee Absence API!", "documentation": "/docs"}


@app.get("/employees")
def list_employees():
    # Load on every request, so a saved edit to the JSON is visible immediately.
    return load_data(EMPLOYEES_FILE)


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    # FastAPI reads the URL value and validates/converts it to an integer.
    employees = load_data(EMPLOYEES_FILE)
    for employee in employees:
        # [] reads a dictionary entry; == compares two values.
        if employee["Employee_ID"] == employee_id:
            return employee  # return ends the function; FastAPI sends JSON.

    # Outside the loop: report 'not found' only after checking every employee.
    raise HTTPException(status_code=404, detail="Employee not found")


@app.get("/absence-requests")
def list_absence_requests():
    return load_data(ABSENCE_REQUESTS_FILE)


@app.get("/absence-requests/{request_id}")
def get_absence_request(request_id: int):
    requests = load_data(ABSENCE_REQUESTS_FILE)
    for req in requests:
        if req["Request_ID"] == request_id:
            return req

    raise HTTPException(status_code=404, detail="Absence request not found")