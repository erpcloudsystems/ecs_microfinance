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


# @frappe.whitelist()
# def get_job_request(doc,from_date,to_date, method=None):

#     emps = frappe.db.sql(""" select a.designation, a.no_of_positions, a.expected_salary, b.name,b.posting_date
#                                                                from `tabJob Request Detail` a join `tabJob Request` b
#                                                                on a.parent = b.name
#                                                                where b.posting_date >='{from1}'
#                                                                and b.posting_date <='{to}'

#                                                            """.format(from1=from_date,
#                                                                       to=to_date), as_dict=1)
#     if emps:
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
    #     return emps

    # else:
    #     frappe.throw("لا يوجد موظفين في هذه الفترة")



# @frappe.whitelist()
# def set_job_requisitions(designation):
#     requisitions = frappe.db.get_list(
#         "Job Requisition",
#         filters={"designation": designation},
#         fields=["name","designation", "no_of_positions", "expected_compensation","custom_branch","custom_branch","custom_basic_salary","custom_incentive","custom_allowances"],
#     )
#     total = 0.0
#     previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"custom_job_requisition": requisitions["name"]}, ["parent"])]
#     if previous_staffing_plan:
#         previous_staffing_plan_name =[name['name'] for name in frappe.db.get_all("Staffing Plan", {"name": ["in", previous_staffing_plan], "docstatus": 1}, ["name"])]
#         # frappe.msgprint("previous_staffing_plan_name:"+str(previous_staffing_plan_name))
#         previous_vacancies = frappe.db.get_all("Staffing Plan Detail", {"custom_job_requisition":requisitions["name"], "parent": ["in", previous_staffing_plan_name]}, ["vacancies"])
#         # frappe.msgprint("previous_custom_total_planned_manpower:"+str(previous_custom_total_planned_manpower))
#         for row in previous_vacancies:
#             total += row["vacancies"]

#         requisitions["total"] = total

#         # self.append(
#         #     "staffing_details",
#         #     {
#         #         "designation": req.designation,
#         #         "custom_job_requisition":req.name,
#         #         "vacancies": req.no_of_positions,
#         #         "estimated_cost_per_position": req.expected_compensation,
#         #         "custom_previous_planned_manpower": total,
#         #         "custom_branch":req.custom_branch,
#         #         "custom_basic_salary":req.custom_basic_salary,
#         #         "custom_incentive":req.custom_incentive,
#         #         "custom_allowances":req.custom_allowances
#         #     },
#         # )

#     return requisitions
        

# @frappe.whitelist()
# def set_job_requisitions(designation):
#     # Retrieve job requisitions based on the provided designation
#     requisitions = frappe.db.get_list(
#         "Job Requisition",
#         filters={"designation": designation},
#         fields=["name", "designation", "no_of_positions", "expected_compensation", "custom_branch", "custom_basic_salary", "custom_incentive", "custom_allowances"]
#     )

#     # Calculate total vacancies from previous staffing plans
#     # total = 0.0
#     # previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"custom_job_requisition": requisitions[0]["name"]}, ["parent"])]
#     # if previous_staffing_plan:
#     #     previous_staffing_plan_name = [name['name'] for name in frappe.db.get_all("Staffing Plan", {"name": ["in", previous_staffing_plan], "docstatus": 1}, ["name"])]
#     #     previous_vacancies = frappe.db.get_all("Staffing Plan Detail", {"custom_job_requisition": requisitions[0]["name"], "parent": ["in", previous_staffing_plan_name]}, ["vacancies"])
#     #     for row in previous_vacancies:
#     #         total += row["vacancies"]
        
#     #     requisitions["total"] = total

#     return requisitions
        
@frappe.whitelist()
def get_salary(designation,branch=None):
    designation_doc = frappe.get_value("Designation",{"name":designation},["*"],as_dict = 1)
    # Calculate total vacancies from previous staffing plans
    total = 0.0
    if branch:
        previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"designation":designation,"custom_branch":branch}, ["parent"])]
    else:
        previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"designation":designation,"custom_branch":""}, ["parent"])]

    if previous_staffing_plan:
        previous_staffing_plan_name = [name['name'] for name in frappe.db.get_all("Staffing Plan", {"name": ["in", previous_staffing_plan], "docstatus": 1}, ["name"])]
        previous_vacancies = frappe.db.get_all("Staffing Plan Detail", {"parent": ["in", previous_staffing_plan_name]}, ["vacancies"])
        for row in previous_vacancies:
            total += row["vacancies"]
        designation_doc["total"] = total
    return designation_doc

@frappe.whitelist()
def get_previous_planned(designation,branch = None):
    # Calculate total vacancies from previous staffing plans
    total = 0.0
    if branch:
        previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"designation":designation,"custom_branch":branch}, ["parent"])]
    else:
        previous_staffing_plan = [parent['parent'] for parent in frappe.db.get_all("Staffing Plan Detail", {"designation":designation,"custom_branch":""}, ["parent"])]

    if previous_staffing_plan:
        previous_staffing_plan_name = [name['name'] for name in frappe.db.get_all("Staffing Plan", {"name": ["in", previous_staffing_plan], "docstatus": 1}, ["name"])]
        previous_vacancies = frappe.db.get_all("Staffing Plan Detail", {"parent": ["in", previous_staffing_plan_name]}, ["vacancies"])
        for row in previous_vacancies:
            total += row["vacancies"]

    return total
