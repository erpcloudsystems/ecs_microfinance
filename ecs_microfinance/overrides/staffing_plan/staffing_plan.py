from hrms.hr.doctype.staffing_plan.staffing_plan import StaffingPlan , get_designation_counts
from frappe.utils import cint, flt
import frappe
from frappe.utils.nestedset import get_descendants_of
class CustomStaffingPlan(StaffingPlan):
	# def onload(self):
	#     frappe.msgprint("kkkkkkkk")
	@frappe.whitelist()
	def set_job_requisitions(self, job_reqs):
		if job_reqs:
			requisitions = frappe.db.get_list(
				"Job Requisition",
				filters={"name": ["in", job_reqs]},
				fields=["name","designation", "no_of_positions", "expected_compensation","custom_branch","custom_branch","custom_basic_salary","custom_incentive","custom_allowances"],
			)
			# frappe.msgprint(str(job_reqs))
			self.staffing_details = []
			for req in requisitions:
				total = 0.0
				previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"custom_job_requisition": req.name}, ["parent"])]
				if previous_staffing_plan:
					previous_staffing_plan_name =[name['name'] for name in frappe.db.get_all("Staffing Plan", {"name": ["in", previous_staffing_plan], "docstatus": 1}, ["name"])]
					# frappe.msgprint("previous_staffing_plan_name:"+str(previous_staffing_plan_name))
					previous_vacancies = frappe.db.get_all("Staffing Plan Detail", {"custom_job_requisition": req.name, "parent": ["in", previous_staffing_plan_name]}, ["vacancies"])
					# frappe.msgprint("previous_custom_total_planned_manpower:"+str(previous_custom_total_planned_manpower))
					for row in previous_vacancies:
						total += row["vacancies"]
				# frappe.msgprint("total:"+str(total))

				self.append(
					"staffing_details",
					{
						"designation": req.designation,
						"custom_job_requisition":req.name,
						"vacancies": req.no_of_positions,
						"estimated_cost_per_position": req.expected_compensation,
						"custom_previous_planned_manpower": total,
						"custom_branch":req.custom_branch,
						"custom_basic_salary":req.custom_basic_salary,
						"custom_incentive":req.custom_incentive,
						"custom_allowances":req.custom_allowances
					},
				)

		return self

	def set_total_estimated_budget(self):
			self.total_estimated_budget = 0
			self.custom_total_annually_estimated_budget = 0
			for detail in self.get("staffing_details"):
				# Set readonly fields
				self.set_number_of_positions(detail)
				if detail.custom_branch:
					designation_counts = get_designation_counts(detail.designation,self.company, detail.custom_branch)
				else:
					designation_counts = get_designation_counts(detail.designation,self.company)
				detail.current_count = designation_counts["employee_count"]
				detail.current_openings = designation_counts["job_openings"]

				detail.total_estimated_cost = 0
				if detail.number_of_positions > 0:
					if detail.vacancies and detail.estimated_cost_per_position:
						detail.custom_total_planned_manpower = cint(detail.vacancies) + cint(detail.custom_previous_planned_manpower)
						detail.total_estimated_cost = cint(detail.vacancies)  * flt(detail.estimated_cost_per_position)
						detail.custom_total_annually_estimated_cost = cint(detail.total_estimated_cost) * 12
				self.total_estimated_budget += detail.total_estimated_cost
				self.custom_total_annually_estimated_budget += detail.custom_total_annually_estimated_cost

	def validate_details(self):
		for detail in self.get("staffing_details"):
			# self.validate_overlap(detail)
			self.validate_with_subsidiary_plans(detail)
			self.validate_with_parent_plan(detail)


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