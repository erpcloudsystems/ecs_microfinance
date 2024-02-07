# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TrainingNeed(Document):
	@frappe.whitelist()
	def get_employee(doc, method=None):
		selected_employee = {}
		doc.set("training_need_table", [])
		if doc.department:
			selected_employee = frappe.db.sql("""
			select `tabEmployee`.name as name, `tabEmployee`.employee_name as employee_name, `tabEmployee`.department as department,
			 `tabEmployee`.designation as designation, `tabEmployee`.territory as territory
			from `tabEmployee`
			where `tabEmployee`.status = "Active"
			and `tabEmployee`.department = '{department}'
			""".format(department=doc.department), as_dict=1)

		else:
			selected_employee = frappe.db.sql("""
				select `tabEmployee`.name as name, `tabEmployee`.employee_name as employee_name, `tabEmployee`.department as department,
				`tabEmployee`.designation as designation, `tabEmployee`.territory as territory
				from `tabEmployee`
				where `tabEmployee`.status = "Active"
				""", as_dict=1)

		if selected_employee != []:
			for i in selected_employee:
				doc.append("training_need_table", {
					"employee": i.name,
					"employee_name": i.employee_name,
					"department": i.department,
					"designation": i.designation,
					"territory": i.territory,
				})
