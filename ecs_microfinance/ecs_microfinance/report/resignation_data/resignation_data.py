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
            "fieldname": "employee",
            "label": "Employee Code  ",
            "fieldtype":"Link",
            "options":"Employee"
        },
        {
            "fieldname": "name",
            "label": "Employee Name (Resignation ID)",
            "fieldtype":"Link",
            "options":"Resignation"
        }
        ,
        {
            "fieldname":"designation",
            "label":"Designation",
            "fieldtype":"Link",
            "options":"Designation"
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
            "fieldname":"last_working_date",
            "label":"Last Working Date",
            "fieldtype":"Data"
        },
        {
            "fieldname":"docstatus",
            "label":"Status",
            "fieldtype":"Data"
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
    docstatus=filters.get('docstatus')
    if filters.get('docstatus'):
        if docstatus == 'Approved':
            conditions += f"AND docstatus =1"
        elif docstatus=='Pending':
            conditions += f"AND docstatus = 0"
    data = frappe.db.sql(f"""Select
                                    employee,name,designation,department,branch,docstatus,last_working_date
                             from 
                                   `tabResignation` 
                             where
                                1=1
                                 {conditions}""", as_dict=1)
    # frappe.msgprint(str(data))
    result =[]
    for row in data:
        final_data ={}
        if row.docstatus == 1:
            final_data['docstatus']  = "Approved"
        elif row.docstatus == 0:
            final_data['docstatus']  = "Pending"
        final_data['name']=row['name']
        final_data['employee']=row['employee']
        final_data['designation']=row['designation']
        final_data['department']=row['department']
        final_data['branch']=row['branch']
        final_data['last_working_date']=row['last_working_date']
        result.append(final_data)
    return result