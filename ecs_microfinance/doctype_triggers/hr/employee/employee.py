from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
from frappe.utils import date_diff
from frappe.utils import add_to_date
import datetime
import math
def round_to_quarter(number):
    return math.ceil(number / 0.25) * 0.25


@frappe.whitelist()
def before_insert(doc, method=None):
    doc.contract_end_date = add_to_date(doc.date_of_joining, days=-1, years=1)


@frappe.whitelist()
def after_insert(doc, method=None):
    date_of_joining = doc.get("date_of_joining")
    if date_of_joining:
        date_of_joining = datetime.datetime.strptime(str(date_of_joining).split(" ")[0], '%Y-%m-%d').date()
        day = date_of_joining.day
        month = date_of_joining.month
        year = date_of_joining.year

        x = (30 - day) + 1
        y = (12 - month) * 30
        z = (x + y) * 0.05833
        z = round_to_quarter(z)
        # m = (x+y)*0.0167

        leave_allocation = frappe.new_doc('Leave Allocation')
        leave_allocation.ref_doctype = "Employee"
        leave_allocation.ref_docname = doc.name
        leave_allocation.employee = doc.employee
        leave_allocation.company = frappe.db.get_value("Employee", doc.employee, "company")
        leave_allocation.leave_type = "أجازة اعتيادي(21)"
        leave_allocation.from_date = doc.date_of_joining
        leave_allocation.to_date = datetime.datetime.now().date().replace(month=12, day=31)
        leave_allocation.new_leaves_allocated = z
        leave_allocation.insert()
        leave_allocation.submit()
        name = leave_allocation.name
        url = "/app/leave-allocation/"+ name
        frappe.msgprint("New Leave Allocation has been Created Please Check and Submit "+"<a href = "+url+">from here  </a>")
    else:
        frappe.msgprint("Date of Joining is missing or in an incorrect format in the imported data.")

    # value = frappe.db.get_value('Designation', {'name': doc.designation}, ['auto_create_ssa'])
    # if value == 1:
    #
    #     salary_structure_assignment = frappe.new_doc('Salary Structure Assignment')
    #     salary_structure_assignment.ref_doctype = "Employee"
    #     salary_structure_assignment.ref_docname = doc.name
    #     salary_structure_assignment.employee = doc.employee
    #     salary_structure_assignment.company = frappe.db.get_value("Employee", doc.employee, "company")
    #     salary_structure_assignment.base =frappe.db.get_value('Designation', {'name': doc.designation, "auto_create_ssa" : 1}, ['basic_salary'])
    #     salary_structure_assignment.transport_allowance =frappe.db.get_value('Designation', {'name': doc.designation, "auto_create_ssa" : 1}, ['transportation_allowance'])
    #     salary_structure_assignment.housing_allowance =frappe.db.get_value('Designation', {'name': doc.designation, "auto_create_ssa" : 1}, ['housing_allowance'])
    #     salary_structure_assignment.salary_structure =frappe.db.get_value('Designation', {'name': doc.designation, "auto_create_ssa" : 1}, ['salary_structure'])
    #     salary_structure_assignment.from_date = doc.date_of_joining
    #     salary_structure_assignment.insert()
    #     # salary_structure_assignment.save()
    #     name = salary_structure_assignment.name
    #     url = "/app/salary-structure-assignment/"+ name
    #     frappe.msgprint("New Salary Stracture has been Created Please Check and Submit "+"<a href = "+url+">from here  </a>")
    #
    #
    # if doc.employment_type == "Training":
    #
    #     salary_structure_assignment = frappe.new_doc('Salary Structure Assignment')
    #     salary_structure_assignment.ref_doctype = "Employee"
    #     salary_structure_assignment.ref_docname = doc.name
    #     salary_structure_assignment.employee = doc.employee
    #     salary_structure_assignment.salary_structure = doc.salary_structure
    #     salary_structure_assignment.base = doc.training_salary_for_day
    #     salary_structure_assignment.company = frappe.db.get_value("Employee", doc.employee, "company")
    #     salary_structure_assignment.from_date = doc.date_of_joining
    #     salary_structure_assignment.insert()
    #     salary_structure_assignment.submit()
    #     # salary_structure_assignment.save()
    #     name = salary_structure_assignment.name
    #     url = "/app/salary-structure-assignment/"+ name
    #     frappe.msgprint("New Salary Stracture has been Created Please Check "+"<a href = "+url+">from here  </a>")

@frappe.whitelist()
def onload(doc, method=None):
    pass

@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):

    # date_of_joining = doc.get("date_of_joining")
    # if date_of_joining:
    #     date_of_joining = datetime.datetime.strptime(str(date_of_joining).split(" ")[0], '%Y-%m-%d').date()
    #     day = date_of_joining.day
    #     month = date_of_joining.month
    #     year = date_of_joining.year
    #     year1 = year+1
    #     day1 = day-1
    #
    #     doc.contract_end_date = datetime.datetime.now().date().replace(year=year1, day=day1)


    if doc.status == "Left" and doc.user_id:
        user = frappe.get_doc("User", doc.user_id)
        user.enabled = 0
        user.save()

@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
