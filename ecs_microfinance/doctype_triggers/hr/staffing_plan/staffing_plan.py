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
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
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


@frappe.whitelist()
def get_job_request(doc,from_date,to_date, method=None):

    emps = frappe.db.sql(""" select a.designation, a.no_of_positions, a.expected_salary, b.name,b.posting_date
                                                               from `tabJob Request Detail` a join `tabJob Request` b
                                                               on a.parent = b.name
                                                               where b.posting_date >='{from1}'
                                                               and b.posting_date <='{to}'

                                                           """.format(from1=from_date,
                                                                      to=to_date), as_dict=1)
    if emps:
        # event = frappe.get_doc('Staffing Plan', doc)
        # event.staffing_details = []
        #
        # for y in emps:
        #     items = event.append("staffing_details", {})
        #     items.employee = y.employee
        #     items.employee_name = y.employee_name
        #     items.designation = y.designation
        #     items.no_of_positions = y.vacancies
        #     items.expected_salary = y.estimated_cost_per_position
        return emps

    else:
        frappe.throw("لا يوجد موظفين في هذه الفترة")



