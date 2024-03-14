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
            "fieldname": "governorate",
            "label": "Governorate",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 150
        },
        {
            "fieldname": "custom_previous_planned_manpower",
            "label": "Previous Planned Manpower",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "fieldname": "vacancies",
            "label": "Vacancies",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "fieldname": "current_count",
            "label": "Current Count",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "custom_total_planned_manpower",
            "label": "Total Planned Manpower",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "custom_basic_salary",
            "label": "Basic Salary",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "custom_allowances",
            "label": "Allowances",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "custom_incentive",
            "label": "Incentive",
            "fieldtype": "Data",
            "width": 150
        },
          {
            "fieldname": "estimated_cost_per_position",
            "label": "Estimated Cost Per Position",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "fieldname": "total_estimated_cost",
            "label": "Total Estimated Cost",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "custom_total_annually_estimated_cost",
            "label": "Total Annually Estimated Cost",
            "fieldtype": "Data",
            "width": 150
        }
        
    ]
    return columns

def get_data(filters):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    designation = filters.get("designation")
    department = filters.get("department")
    branch = filters.get("branch")
    governorate = filters.get("governorate")
    conditions = ""
    if designation:
        conditions += f"and spt.designation = '{designation}'"
    if governorate:
        conditions += f"and b.custom_governorate = '{governorate}'"
    if branch:
        conditions += f"and spt.custom_branch = '{branch}'"
    if department:
        conditions += f"and d.department = '{department}'"
    
    data = frappe.db.sql(f"""
                select sp.name,
                d.department as department,
                b.custom_governorate as governorate,
                spt.custom_branch as branch,
                spt.designation as designation,
                spt.custom_previous_planned_manpower as custom_previous_planned_manpower,
                spt.vacancies as vacancies,
                spt.current_count as current_count,
                spt.custom_total_planned_manpower as custom_total_planned_manpower,
                spt.custom_basic_salary as custom_basic_salary,
                spt.custom_allowances as custom_allowances,
                spt.custom_incentive as custom_incentive,
                spt.estimated_cost_per_position as estimated_cost_per_position,
                spt.total_estimated_cost as total_estimated_cost,
                spt.custom_total_annually_estimated_cost as custom_total_annually_estimated_cost
                from `tabStaffing Plan` sp
                join `tabStaffing Plan Detail` spt
                left join `tabDesignation` d on spt.designation = d.name
                left join `tabBranch` b on spt.custom_branch = b.name
                on sp.name = spt.parent
                where sp.docstatus = 1
                {conditions}
                and (from_date > '{from_date}' 
                or to_date < '{to_date}') 
                """,as_dict=1)
    if data:
        return data