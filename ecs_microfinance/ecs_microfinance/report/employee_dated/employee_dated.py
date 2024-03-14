# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns=get_columns(filters)
    data=get_data(filters)
    return columns, data

def get_columns(filters):
    return[
        {
            "fieldname": "name",
            "label": "Employee Code  ",
            "fieldtype":"Link",
            "options":"Employee",
            "width":100
        },
        {
            "fieldname": "employee_name",
            "label": "Employee Name ",
            "fieldtype":"Link",
            "options":"Employee",
            "width":200
        }
        ,
        {
			"fieldname":"designation",
			"label":"Designation",
			"fieldtype":"Link",
			"options":"Designation",
            "width":200
		},
		{
			"fieldname":"department",
			"label":"Department",
			"fieldtype":"Link",
			"options":"Department"
		},
		{
			"fieldname":"branch",
			"label":"Branch",
			"fieldtype":"Link",
			"options":"Branch"
		},
        {
            "fieldname": "probation_end_date",
            "label": "Probation End Date",
            "fieldtype":"Date"
            
        },
        {
            "fieldname": "contract_end_date",
            "label": "Contract End Date",
            "fieldtype":"Date"
        }
            
	]

def get_data(filters):
    conditions = ""
    name=filters.get('name')
    if name:
        conditions += f"AND name = '{name}'"
    designation=filters.get('designation')
    if filters.get('designation'):
        conditions += f"AND designation = '{designation}'"
    department=filters.get('department')
    if filters.get('department'):
        conditions += f"AND department = '{department}'"
    branch=filters.get('branch')
    if filters.get('branch'):
        conditions += f"AND branch = '{branch}'"
    from_date=filters.get('from_date')
    to_date=filters.get('to_date')
    if filters.get('selected_date')=='Probation End Date':
        conditions += f"AND probation_end_date between '{from_date}'  and '{to_date}'"
        
    if filters.get('selected_date')=='Contract End Date':
        conditions += f"AND contract_end_date between '{from_date}'  and '{to_date}'"

        
    
    data = frappe.db.sql(f"""Select
                                    name,employee_name,designation,department,branch,
                                    probation_end_date,contract_end_date
                             from 
                                   `tabEmployee` 
                             where
                                1=1
                                
                                 {conditions}""", as_dict=1)
    if data :
        return data


