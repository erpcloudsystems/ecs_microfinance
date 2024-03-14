# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_column()
    data = get_data(filters)
    return columns, data

def get_column():
    columns = [
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 150
        },
        {
            "fieldname": "designation",
            "label": "Designation",
            "fieldtype": "Link",
            "options": "Designation",
            "width": 150
        },
        {
            "fieldname": "employee",
            "label": "Potential Successor Code",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150
        },

        {
            "fieldname": "employee_name",
            "label": "Employee Name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "governorate",
            "label": "Governorate",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "fieldname": "performance_level",
            "label": "Performance Level",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "potential_level",
            "label": "Potential Level",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "readiness_level",
            "label": "Readiness Level",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "gaps_in_competencies",
            "label": "Gaps In Competencies",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "developmental_plan_to_bridge_gaps",
            "label": "Bridge Gaps",
            "fieldtype": "Data",
            "width": 150
        },
    ]
    return columns

def get_data(filters):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    
    data = frappe.db.sql("""
                select sp.name,
                spt.department as department,
                sp.potential_successors_governorate as governorate,
                sp.potential_successors_branch as branch,
                spt.designation as designation,
                spt.employee_name as employee_name,
                spt.employee as employee,
                spt.developmental_plan_to_bridge_gaps as developmental_plan_to_bridge_gaps,
                spt.gaps_in_competencies as gaps_in_competencies,
                spt.readiness_level as readiness_level,
                spt.potential_level as potential_level,
                spt.performance_level as performance_level
                from `tabSuccession Planning` sp
                join `tabSuccession Planning Table` spt
                on sp.name = spt.parent
                where sp.docstatus = 1
                and posting_date between '{0}' and '{1}' 
                """.format(from_date,to_date),as_dict=1)
    if data:
        return data