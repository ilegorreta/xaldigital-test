#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
db = SQLAlchemy(app)


def validate_state(state):
    if isinstance(state, str) and len(state) == 2:
        return True
    else:
        return False


def validate_phone_number(phone1, phone2):
    PHONE_REGEX = "\w{3}-\w{3}-\w{4}"
    # Phone formatting should be something like this: '555-111-6789'
    if re.search(PHONE_REGEX, phone1) and re.search(PHONE_REGEX, phone2):
        return True
    else:
        return False


class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    company_name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(64), nullable=False)
    zip = db.Column(db.String(64), nullable=False)
    phone1 = db.Column(db.String(10), nullable=False)
    phone2 = db.Column(db.String(10))
    email = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64), nullable=False)

    def __init__(
        self,
        first_name,
        last_name,
        company_name,
        address,
        city,
        state,
        zip,
        phone1,
        phone2,
        email,
        department,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.phone1 = phone1
        self.phone2 = phone2
        self.email = email
        self.department = department


db.create_all()

# Retrieve single employee
@app.route("/employee/<employee_id>", methods=["GET"])
def get_item(employee_id):
    try:
        item = Employee.query.get(employee_id)
        del item.__dict__["_sa_instance_state"]
        return jsonify(item.__dict__)
    except Exception as e:
        return f"No employee with employee_id = {employee_id} was found. Please validate and try again."


# Retrieve all employees
@app.route("/employees", methods=["GET"])
def get_items():
    items = []
    for item in db.session.query(Employee).all():
        del item.__dict__["_sa_instance_state"]
        items.append(item.__dict__)
    return jsonify(items)


# Post a new Employee
@app.route("/new_employee", methods=["POST"])
def create_item():
    body = request.get_json()
    db.session.add(
        Employee(
            body["first_name"],
            body["last_name"],
            body["company_name"],
            body["address"],
            body["city"],
            body["state"],
            body["zip"],
            body["phone1"],
            body["phone2"],
            body["email"],
            body["department"],
        )
    )
    if not validate_state(body["state"]):
        return "State field formatted incorrectly. Please double check input data and try again."
    elif not validate_phone_number(body["phone1"], body["phone2"]):
        return "Phone number field(s) formatted incorrectly. Please double check input data and try again."
    else:
        db.session.commit()
        return "Employee posted successfully!"


# Update employee information
@app.route("/employee/<employee_id>", methods=["PUT"])
def update_item(employee_id):
    body = request.get_json()
    db.session.query(Employee).filter_by(employee_id=employee_id).update(
        dict(
            first_name=body["first_name"],
            last_name=body["last_name"],
            company_name=body["company_name"],
            address=body["address"],
            city=body["city"],
            state=body["state"],
            zip=body["zip"],
            phone1=body["phone1"],
            phone2=body["phone2"],
            email=body["email"],
            department=body["department"],
        )
    )
    if not validate_state(body["state"]):
        return "State field formatted incorrectly. Please double check input data and try again."
    elif not validate_phone_number(body["phone1"], body["phone2"]):
        return "Phone number field(s) formatted incorrectly. Please double check input data and try again."
    else:
        db.session.commit()
        return "Employee updated successfully!"


# Remove employee from database
@app.route("/employee/<employee_id>", methods=["DELETE"])
def delete_item(employee_id):
    try:
        db.session.query(Employee).filter_by(employee_id=employee_id).delete()
        db.session.commit()
        return "Employee deleted successfully"
    except Exception as e:
        return f"No employee with employee_id = {employee_id} was found. Please validate and try again."


if __name__ == "__main__":
    app.run(debug=True)
