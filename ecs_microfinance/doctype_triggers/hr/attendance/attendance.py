from __future__ import unicode_literals
import frappe
from frappe import _


from .hr.attendance_policy_applier import AttendancePoliciesApplier


@frappe.whitelist()
def before_insert(doc, method=None):
    pass


@frappe.whitelist()
def after_insert(doc, method=None):
    pass


@frappe.whitelist()
def onload(doc, method=None):
    # frappe.msgprint(str(doc.in_time))
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


@frappe.whitelist()
def validate(doc, method=None):
    pass


@frappe.whitelist()
def on_submit(doc, method=None):
    if doc.attendance_request or doc.leave_application:
        return
    applier = AttendancePoliciesApplier()
    applier.apply_policy_on(doc)
    ## Auto Create Submit Extra Salary On Submit
    # Component = frappe.get_value('Salary Component', {'branch': doc.branch, 'extra_salary' : 1}, ['name'])
    # if doc.status == "Present":
    #     new_doc = frappe.get_doc({
    #             "doctype": "Extra Salary",
    #             "salary_component": Component,
    #             "type": "Earning",
    #             "currency": "EGP",
    #             "amount": "1",
    #             "employee": doc.employee,
    #             "branch": doc.branch,
    #             "employee_name": doc.employee_name,
    #             "payroll_date": doc.attendance_date,
    #             "branch": doc.branch,
    #             "shift": doc.shift,
    #             })
    #     new_doc.insert(ignore_permissions=True)
    #     new_doc.submit()
    #
    # if doc.late_entry:
    #     new_doc = frappe.get_doc({
    #             "doctype": "Extra Salary",
    #             "salary_component": doc.salary_component,
    #             "type": "Deduction",
    #             "currency": "EGP",
    #             "amount": "1",
    #             "employee": doc.employee,
    #             "branch": doc.branch,
    #             "employee_name": doc.employee_name,
    #             "payroll_date": doc.attendance_date,
    #             "branch": doc.branch,
    #             "shift": doc.shift,
    #             })
    #     new_doc.insert(ignore_permissions=True)
    #     new_doc.submit()
    pass


@frappe.whitelist()
def on_cancel(doc, method=None):
    pass


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

