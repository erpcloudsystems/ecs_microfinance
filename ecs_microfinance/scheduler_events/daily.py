from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import today , getdate

@frappe.whitelist()
def daily():
    check_period = 30
    employees = frappe.get_all("Employee", filters={"status": "Active"})
    for emp in employees:
        emp_doc= frappe.get_doc("Employee", emp.name)
        contract_end_date = emp_doc.contract_end_date
        if contract_end_date:
            days_until_contract_end = (contract_end_date - getdate(today())).days            
            if days_until_contract_end == check_period:
                make_employee_contract(emp.name)

    check_period1 = 1
    employees = frappe.get_all("Employee", filters={"status": "Active"})
    for emp in employees:
        emp_doc= frappe.get_doc("Employee", emp.name)
        probation_end_date = emp_doc.probation_end_date
        if probation_end_date:
            days_until_probation_end = (probation_end_date - getdate(today())).days
            if days_until_probation_end == check_period1:
                make_employee_probation_period(emp.name)


def make_employee_probation_period(docname):
    doc = frappe.get_doc("Employee", docname)
    emp_probation = frappe.new_doc("Employee Probation Period")
    emp_probation.employee = doc.employee
    emp_probation.save()
    


def make_employee_contract(docname):
    doc = frappe.get_doc("Employee", docname)
    emp_contract = frappe.new_doc("Employee Contracts")
    emp_contract.employee = doc.employee
    emp_contract.save()