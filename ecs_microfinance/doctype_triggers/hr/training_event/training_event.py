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
        # emps = frappe.db.sql(""" select a.employee, a.designation,a.training_fielded,b.name,b.posting_date
        #                                                         from `tabTraining Budget Table` a join `tabTraining Budget` b
        #                                                         on a.parent = b.name
        #                                                         where a.training_fielded = '{field}'
        #                                                         and b.posting_date >='{from1}'
        #                                                         and b.posting_date <='{to}'
        #                                                         and b.docstatus = 1
        #
        #                                                     """.format(field=doc.training_field,from1=doc.from_date,to=doc.to_date), as_dict=1)
        # if emps:
        #     doc.employees =[]
        #     for y in emps:
        #         items = doc.append("employees", {})
        #         items.employee = y.employee
        #         items.designation = y.designation
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
def get_employee(doc,training_field,from_date,to_date, method=None):

    emps = frappe.db.sql(""" select a.employee, a.employee_name, a.designation,a.training_fielded,b.name,b.posting_date
                                                               from `tabTraining Budget Table` a join `tabTraining Budget` b
                                                               on a.parent = b.name
                                                               where a.training_fielded = '{field}'
                                                               and b.posting_date >='{from1}'
                                                               and b.posting_date <='{to}'
                                                               and b.docstatus = 1

                                                           """.format(field=training_field, from1=from_date,
                                                                      to=to_date), as_dict=1)
    if emps:
        # event = frappe.get_doc('Training Event', doc)
        # event.employees = []
        #
        # for y in emps:
        #     items = event.append("employees", {})
        #     items.employee = y.employee
        #     items.employee_name = y.employee_name
        #     items.designation = y.designation
        return emps

    else:
        frappe.throw("لا يوجد موظفين في هذه الفترة")
