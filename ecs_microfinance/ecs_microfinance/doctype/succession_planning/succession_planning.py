# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SuccessionPlanning(Document):
	@frappe.whitelist()
	def get_employee(doc, method=None):
		selected_employee = {}
		if doc.potential_successors_designation:
			condition = ""
			potential_successors_designation = doc.potential_successors_designation
			potential_successors_branch = doc.potential_successors_branch
			potential_successors_department = doc.potential_successors_department
			potential_successors_governorate = doc.potential_successors_governorate

			if potential_successors_designation:
				condition += f"AND `tabEmployee`.designation = '{potential_successors_designation}'"
			
			if potential_successors_branch:
				condition +=f"AND `tabEmployee`.branch = '{potential_successors_branch}'"
			if potential_successors_department:
				condition += f"AND `tabEmployee`.department = '{potential_successors_department}'"
			
			if potential_successors_governorate:
				condition +=f"AND `tabEmployee`.governorate = '{potential_successors_governorate}'"
			
			selected_employee = frappe.db.sql("""
			select `tabEmployee`.name as name, `tabEmployee`.employee_name as employee_name, `tabEmployee`.department as potential_successors_department,
			 `tabEmployee`.designation as potential_successors_designation, `tabEmployee`.governorate as potential_successors_governorate, `tabEmployee`.branch as potential_successors_branch
			from `tabEmployee`
			where `tabEmployee`.status = "Active"
		
			{condition}
			""".format(condition=condition), as_dict=1)


		if selected_employee != []:
			for i in selected_employee:
				doc.append("succession_planning_table", {
					"employee": i.name,
					"employee_name": i.employee_name,
					"department": i.potential_successors_department,
					"designation": i.potential_successors_designation,
				})



	@frappe.whitelist()
	def get_employees(doc, method=None):
		selected_employee = {}
		if doc.designation:
			condition = ""
			governorate = doc.governorate
			branch = doc.branch
			department = doc.department
			designation = doc.designation

			if designation:
				condition += f"AND `tabEmployee`.designation = '{designation}'"
			
			if branch:
				condition +=f"AND `tabEmployee`.branch = '{branch}'"
			if department:
				condition += f"AND `tabEmployee`.department = '{department}'"
			
			if governorate:
				condition +=f"AND `tabEmployee`.governorate = '{governorate}'"
			
			selected_employee = frappe.db.sql("""
			select `tabEmployee`.name as name, `tabEmployee`.employee_name as employee_name, `tabEmployee`.department as department,
			 `tabEmployee`.designation as designation, `tabEmployee`.governorate as governorate, `tabEmployee`.branch as branch, `tabEmployee`.contract_end_date as contract_end_date
			from `tabEmployee`
			where `tabEmployee`.status = "Active"
		
			{condition}
			""".format(condition=condition), as_dict=1)
		if selected_employee != []:
			for i in selected_employee:
				doc.employee = i.name
				doc.employee_name = i.employee_name
				doc.contract_end_date = i.contract_end_date




