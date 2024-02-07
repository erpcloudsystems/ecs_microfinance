# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PhonebillDeduction(Document):
	@frappe.whitelist()
	def get_employee(doc, method=None):
		selected_employee = frappe.db.sql(f"""
			select `tabEmployee`.name as name, `tabEmployee`.employee_name as employee_name, `tabEmployee`.department as department, `tabEmployee`.cell_number
			from `tabEmployee`
			where `tabEmployee`.status = "Active"

			""", as_dict=1)

		if selected_employee != []:
			for i in selected_employee:
				doc.append("phone_bill_table", {
					"employee": i.name,
					"employee_name": i.employee_name,
					"department": i.department,
					"company_mobile": i.cell_number,
					'salary_component' : 'خصم خط تليفون'
				})

		# for i in selected_cow:
		# 	doc.append("cows", {
		# 		"value_of_food": i.quantity_of_food * doc.price_per_one
		# 	})

		if selected_employee == []:
			frappe.msgprint("لا يوجد بيانات")

	@frappe.whitelist()
	def on_submit(self):
		for row in self.phone_bill_table:
			additional_salary = frappe.new_doc('Additional Salary')
			additional_salary.ref_doctype = "Employee Penalty"
			additional_salary.employee = row.employee
			additional_salary.company = frappe.db.get_value("Employee", row.employee, "company")
			additional_salary.salary_component = 'خصم خط تليفون'
			additional_salary.payroll_date = self.payroll_date

			additional_salary.amount = row.employee_deduct
			additional_salary.insert()
			additional_salary.submit()