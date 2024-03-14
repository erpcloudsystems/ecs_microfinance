# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint, flt
from frappe.utils.nestedset import get_descendants_of

class HiringRequest(Document):
	def validate(self):
		# self.validate_period()
		# self.validate_details()
		self.set_total_estimated_budget()
	@frappe.whitelist()
	def set_hiring_request_details(self):
		staffing_plan = frappe.get_list(
			"Staffing Plan",
			filters={"from_date": ["<=", self.request_date], "to_date": [">=", self.request_date],"docstatus":1},
			fields=["*"],
			order_by="creation DESC",
			limit_page_length=1
		)
		company_set = get_descendants_of("Company", self.company)
		company_set.append(self.company)
		employee_count = frappe.db.count(
			"Employee", {"designation": self.designation,"branch":self.branch, "status": "Active", "company": ("in", company_set)}
		)

		if staffing_plan:
			staffing_details = frappe.db.get_all("Staffing Plan Detail", {"parent": staffing_plan[0]['name']}, ["*"])
			if staffing_details:
				self.hiring_request_details = []
				for req in staffing_details:
					if req.designation == self.designation and req.custom_branch == self.branch:
						total_no_of_employees = 0.0
						self.staffing_plan = staffing_plan[0]['name']
						#check if there is hiring request exist for same staffing 
						prevoious_request = frappe.db.get_all("Hiring Request",{"designation":self.designation,"branch":self.branch,"staffing_plan":staffing_plan[0]['name'],"docstatus":1},["no_of_employees"]) 
						if prevoious_request :
							for row in prevoious_request:
								total_no_of_employees += row["no_of_employees"]

						if req.custom_total_planned_manpower == employee_count:
							frappe.throw("لا يمكنك الطلب لأن عدد الموظفين الذين تم تعيينهم هو نفس العدد المطلوب في خطة التوظيف")
						self.append(
							"hiring_request_details",
							{
								"designation": req.designation,
								"vacancies": req.custom_total_planned_manpower - employee_count,
								"planned_manpower": req.custom_total_planned_manpower,
								"branch": req.custom_branch,
								"current_count": employee_count,
								"current_openings":total_no_of_employees
							},
						)
			else:
				frappe.msgprint("لا يوجد بيانات")


	def set_total_estimated_budget(self):
			# self.total_estimated_budget = 0
			# self.custom_total_annually_estimated_budget = 0
			for detail in self.get("hiring_request_details"):
				# Set readonly fields
				# self.set_number_of_positions(detail)
				designation_counts = get_designation_counts(detail.designation,self.company, detail.branch)
				
				detail.current_count = designation_counts["employee_count"]
				detail.current_openings = designation_counts["job_openings"]

				# detail.total_estimated_cost = 0
				# if detail.number_of_positions > 0:
				# 	if detail.vacancies and detail.estimated_cost_per_position:
				# 		detail.custom_total_planned_manpower = cint(detail.vacancies) + cint(detail.custom_previous_planned_manpower)
				# 		detail.total_estimated_cost = cint(detail.vacancies)  * flt(detail.estimated_cost_per_position)
				# 		detail.custom_total_annually_estimated_cost = cint(detail.total_estimated_cost) * 12
				# self.total_estimated_budget += detail.total_estimated_cost
				# self.custom_total_annually_estimated_budget += detail.custom_total_annually_estimated_cost

@frappe.whitelist()
def get_designation_counts(designation,  company, branch=None ,job_opening=None):
	if not designation:
		return False

	company_set = get_descendants_of("Company", company)
	company_set.append(company)
	if branch:
		employee_count = frappe.db.count(
			"Employee", {"designation": designation,"branch":branch, "status": "Active", "company": ("in", company_set)}
		)
	else:
		employee_count = frappe.db.count(
			"Employee", {"designation": designation, "status": "Active", "company": ("in", company_set)}
		)
	filters = {"designation": designation,"status": "Open", "company": ("in", company_set)}
	if job_opening:
		filters["name"] = ("!=", job_opening)

	job_openings = frappe.db.count("Job Opening", filters)

	return {"employee_count": employee_count, "job_openings": job_openings}
# staffing_plan = frappe.db.sql(f"""
		# 	SELECT * 
		# 	FROM `tabStaffing Plan` 
		# 	WHERE from_date <= '{self.request_date}' 
		# 	AND to_date >= '{self.request_date}' 
		# 	ORDER BY creation DESC 
		# 	LIMIT 1
		# """, as_dict=True)