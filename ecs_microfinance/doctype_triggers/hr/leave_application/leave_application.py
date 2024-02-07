from __future__ import unicode_literals
import frappe
from frappe import _
from datetime import datetime


def calculate_days_between_dates(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    delta = end_date - start_date
    return delta.days


def validate_number_of_days_before_leave_application(doc):
    """
    throw an error if the user creates a leave application befor the allowed number of days before
    """
    leave_type_policy = frappe.db.get_all("Leave Type Policy",
                                          filters={
                                              "parent": doc.leave_type,
                                              "from": ['<=', doc.total_leave_days],
                                              "to": ['>=', doc.total_leave_days]
                                              }, 
                                          fields=["from", "to", "number_of_days_before"])
    if leave_type_policy:
        num_of_days_before = leave_type_policy[0]["number_of_days_before"]
        date_diff = abs(calculate_days_between_dates(doc.posting_date, doc.from_date))
        if num_of_days_before > date_diff:
            frappe.throw(f"لا يمكن تقديم طلب الاجازه قبل  {num_of_days_before} يوم", frappe.exceptions.ValidationError)

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
    if doc.type_of_leave == "اعتيادي":
        validate_number_of_days_before_leave_application(doc)


        
    


@frappe.whitelist()
def on_submit(doc, method=None):
    record_name = str(doc.name) + str(doc.employee)
    frappe.db.sql(""" INSERT INTO `tabVacation Logs`
									(posting_date, from_date, to_date, total_leave_days, type_of_leave, parent, parentfield, parenttype, name)
							VALUES ('{posting_date}', '{from_date}', '{to_date}', '{total_leave_days}','{type_of_leave}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
							""".format(posting_date=doc.posting_date,
                                       from_date=doc.from_date,
                                       to_date=doc.to_date,
                                       total_leave_days=doc.total_leave_days,
                                       type_of_leave=doc.type_of_leave,
                                       parent=doc.employee, parenttype="Employee",
                                       parentfield="vacation_logs", record_name=record_name))
@frappe.whitelist()
def on_cancel(doc, method=None):
    record_name = str(doc.name) + str(doc.employee)
    frappe.db.sql(""" DELETE FROM `tabVacation Logs` where parent = '{parent}' and parentfield = '{parentfield}' and parenttype = '{parenttype}' and name = '{record_name}'
		 """.format(parent=doc.employee, parenttype="Employee", parentfield="vacation_logs",
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
