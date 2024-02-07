from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass

def calculate_and_set_values(doc, method):
    import math
    doc.gross = (doc.base or 0.0) + (doc.transport_allowance or 0.0) + (doc.housing_allowance or 0.0) + (doc.incentives or 0.0) + (doc.exempt_bonuses or 0.0) + (doc.mobile_allowancee or 0.0) + (doc.training_allowancee or 0.0) + (doc.living_allowancee or 0.0) + (doc.other_allowancee or 0.0)

    t = doc.gross / 1.3
    doc.variable = int(math.ceil(t / 100.0)) * 100

    # Check if doc.insurance_salary is None before performing operations on it
    if not doc.insurance_salary:
        doc.insurance_salary = doc.variable  # Or set it to some default value

    if doc.variable > float(doc.maximum_insurance_salaryy):
        doc.variable = doc.maximum_insurance_salaryy
    elif doc.variable < float(doc.minimum_insurance_salaryy):
        doc.variable = doc.minimum_insurance_salaryy

    x = doc.basic_salaryy

    if doc.basic_salaryy is None:
        x = 0.0  # Or set it to some default value
    elif doc.basic_salaryy > float(doc.maximum_emergency_subsidyy):
        x = doc.maximum_emergency_subsidyy
    elif doc.basic_salaryy < float(doc.minimum_emergency_subsidyy):
        x = float(doc.minimum_emergency_subsidyy)

    doc.emergency_subsidy = (x * 1.0) / 100




@frappe.whitelist()
def validate(doc, method=None):
    calculate_and_set_values(doc, method)



@frappe.whitelist()
def on_submit(doc, method=None):
        record_name = str(doc.name) + str(doc.employee)
        frappe.db.sql(""" INSERT INTO `tabSalary Logs`
    									(from_date, base, insurance_salary, gross, notes, parent, parentfield, parenttype, name)
    							VALUES ('{from_date}', '{base}', '{insurance_salary}','{gross}','{notes}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
    							""".format(from_date=doc.from_date,
                                           base=doc.base,
                                           insurance_salary=doc.insurance_salary,
                                           gross=doc.gross,
                                           notes=doc.notes,
                                           parent=doc.employee, parenttype="Employee",
                                           parentfield="salary_logs", record_name=record_name))

@frappe.whitelist()
def on_cancel(doc, method=None):
        record_name = str(doc.name) + str(doc.employee)
        frappe.db.sql(""" DELETE FROM `tabSalary Logs` where parent = '{parent}' and parentfield = '{parentfield}' and parenttype = '{parenttype}' and name = '{record_name}'
    		 """.format(parent=doc.employee, parenttype="Employee", parentfield="salary_logs",
                        record_name=record_name))

@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
