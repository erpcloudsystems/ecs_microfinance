from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import  date_diff
import datetime
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
@frappe.whitelist()
def validate(doc, method=None):
    pass
#     _from = doc.from_date
#     if isinstance(_from, str):
#         _from = datetime.datetime.strptime(doc.from_date, "%Y-%m-%d").date()
#     _from = _from.replace(day=1)
#
#     number_of_working_from_home = frappe.db.sql(
#         f"""
#     SELECT count(*)
#     FROM `tabAttendance`
#     WHERE docstatus = 1
#          AND employee = '{doc.employee}'
#          and status = "Work From Home"
#          and attendance_date between '{_from}' and '{doc.from_date}'
#     """)[0][0]
#
#     y = date_diff(doc.to_date, doc.from_date) + 1
#     z = frappe.db.get_value("Employee Grade", doc.grade, "allowed_woh_days")
#
#     if number_of_working_from_home + y > z:
#         frappe.throw(_("Sorry You Exceeded Allowed Work From Home Days In Month"))
#
#
# @frappe.whitelist()
# def on_submit(self, method=None):
#     extra_salary = frappe.new_doc('Extra Salary')
#     extra_salary.ref_doctype = "Attendance Request"
#     extra_salary.employee = self.employee
#     extra_salary.company = frappe.db.get_value("Employee", self.employee, "company")
#     extra_salary.payroll_date = self.to_date
#     x= frappe.db.get_value("Employee Grade", self.grade, "per_deem")
#     extra_salary.salary_component = "بدل سفر"
#     v = float(self.transpiration_allowance)
#     extra_salary.amount = v*x
#     extra_salary.insert()
#     extra_salary.submit()



@frappe.whitelist()
def on_cancel(doc, method=None):
    pass

@frappe.whitelist()
def on_submit(doc, method=None):
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
