# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import datetime

class EndofService(Document):
	@frappe.whitelist()
	def get_employee_data(self):
		employee_salary_structure = frappe.db.sql(f"""
													SELECT * FROM `tabSalary Structure Assignment`
													WHERE employee = '{self.employee}' 
													AND docstatus = 1
													ORDER BY from_date DESC
													LIMIT 1
												""", as_dict=1)[0]

		self.allowances = employee_salary_structure['housing_allowance'] + employee_salary_structure.living_allowancee + employee_salary_structure.transport_allowance + employee_salary_structure.training_allowancee + employee_salary_structure.mobile_allowancee + employee_salary_structure.other_allowancee
		self.basic_salary = employee_salary_structure['base']


	@frappe.whitelist()
	def calculte_days(self):
		# Get the current date as a datetime object
		current_date = datetime.now().date()

		# Convert self.date_of_joining string to a datetime object
		date_of_joining = datetime.strptime(self.date_of_joining, "%Y-%m-%d").date()

		
		# Convert self.date_of_joining string to a datetime object
		last_working_date = datetime.strptime(self.last_working_date, "%Y-%m-%d").date()

		# Get the first date of the current year
		first_date_of_year = datetime(current_date.year, 1, 1).date()

		if date_of_joining < first_date_of_year:
			days = (last_working_date - first_date_of_year).days
			self.total_leave_balance = days * (21 / 12 / 30)

		elif date_of_joining > first_date_of_year:
			days = (last_working_date - date_of_joining).days
			self.total_leave_balance = days * (21 / 12 / 30)
		
		leave_days_result = frappe.db.sql(f"""
			SELECT SUM(total_leave_days) 
			FROM `tabLeave Application` 
			WHERE from_date > '{first_date_of_year}'
			AND to_date < '{last_working_date}'
			AND leave_type = 'أجازة اعتيادي(21)'
			AND employee = '{self.employee}'
		""")
		if leave_days_result:
			self.used_leave = leave_days_result[0][0]  
			self.remaining_leaves = self.total_leave_balance - self.used_leave 
			self.leaves_allowance_amount = ((self.basic_salary + self.allowances ) / 30) * self.remaining_leaves



		



