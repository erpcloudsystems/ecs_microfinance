# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = get_columns(), get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Employee"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",  # Change this from "Date" to "Data"
            "width": 200
        },
    ]

def get_data(filters):
    employees_without_checkin = get_employees_without_checkin(filters)
    return employees_without_checkin

def get_employees_without_checkin(filters):
    conditions = ""
    if filters.get("time"):  # Assuming you have a filter for the date
        conditions += " and DATE(`tabEmployee Checkin`.time) = DATE(%(time)s)"

    query = f"""
        SELECT `tabEmployee`.name as name, `tabEmployee`.employee_name
        FROM `tabEmployee`
        where `tabEmployee`.status = "Active"
        AND
        `tabEmployee`.name  not in (
        SELECT `tabEmployee`.name as name
        FROM `tabEmployee`
        JOIN `tabEmployee Checkin` ON `tabEmployee`.name = `tabEmployee Checkin`.employee
         {conditions})
    """

    employees = frappe.db.sql(query, filters, as_dict=1)

    return employees
