# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeePenalty(Document):
	def on_submit(self):
		record_name = str(self.name) + str(self.against_to)
		frappe.db.sql(""" INSERT INTO `tabPenalty Logs`
										(penalty_date, raised_by, against_to, penalty_deduction, notes, parent, parentfield, parenttype, name)
								VALUES ('{penalty_date}', '{raised_by}', '{against_to}', '{penalty_deduction}', '{notes}', '{parent}', '{parentfield}', '{parenttype}', '{record_name}')
								""".format(penalty_date=self.penalty_date, raised_by=self.raised_by,
										   against_to=self.against_to,
										   # penalty_type=self.penalty_type,
										   penalty_deduction=self.penalty_deduction,
										   notes=self.notes,
										   parent=self.against_to, parenttype="Employee",
										   parentfield="custom_penalty_logs", record_name=record_name))


		extra_salary = frappe.new_doc('Extra Salary')
		extra_salary.ref_doctype = "Employee Penalty"
		extra_salary.employee = self.against_to
		extra_salary.company = frappe.db.get_value("Employee", self.against_to, "company")
		extra_salary.salary_component = self.salary_component
		extra_salary.payroll_date = self.penalty_date
		v = float(self.penalty_deduction)
		extra_salary.amount = v
		extra_salary.insert()
		extra_salary.submit()

	def on_cancel(self):
		record_name = str(self.name) + str(self.against_to)
		frappe.db.sql(""" DELETE FROM `tabPenalty Logs` where parent = '{parent}' and parentfield = '{parentfield}' and parenttype = '{parenttype}' and name = '{record_name}'
			 """.format(parent=self.against_to, parenttype="Employee", parentfield="custom_penalty_logs",
						record_name=record_name))


