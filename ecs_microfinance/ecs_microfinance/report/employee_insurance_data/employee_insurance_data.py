# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [

        {
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 250
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 210,
			"hidden": 1
        },
        {
            "label": _("Insurance Number"),
            "fieldname": "health_insurance_no",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("National Id"),
            "fieldname": "national_id",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": _("Date of Joining"),
            "fieldname": "date_of_joining",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Gender"),
            "fieldname": "gender",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": _("Gross Salary"),
            "fieldname": "gross_salary",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Insurance Salary"),
            "fieldname": "insurance_salary",
            "fieldtype": "Currency",
            "width": 150
        }
        
        


    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
   
    if filters.get("name"):
        conditions += " and `tabEmployee`.name =%(name)s"
    item_results = frappe.db.sql("""
                select
                        `tabEmployee`.name as name,
                        `tabEmployee`.employee_name as employee_name,
                        `tabEmployee`.health_insurance_no as health_insurance_no,
                        `tabEmployee`.national_id as national_id,
                        `tabEmployee`.date_of_joining as date_of_joining,
                        `tabEmployee`.gender as gender,
                        (SELECT gross from `tabSalary Structure Assignment` where `tabSalary Structure Assignment`.employee = `tabEmployee`.name and `tabSalary Structure Assignment`.docstatus = 1  Order by from_date DESC LIMIT 1)
                        as  gross_salary,
                        (SELECT insurance_salary from `tabSalary Structure Assignment` where `tabSalary Structure Assignment`.employee = `tabEmployee`.name and `tabSalary Structure Assignment`.docstatus = 1 Order by from_date DESC LIMIT 1)
                        as  insurance_salary
                        
                    from
                        `tabEmployee`
                    
                    where
                        `tabEmployee`.status="Active"   
                {conditions}


                """.format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            gross_salsry_cent = 0
            gross_salsry_pound = 0
            insurance_salary_cent = 0
            insurance_salary_pound = 0
            
            if item_dict.gross_salary:
                gross_salsry= str(item_dict.gross_salary).split(".")
                gross_salsry_pound = gross_salsry[0]
                if len(gross_salsry)>1:
                    gross_salsry_cent = gross_salsry[1]
                
            if item_dict.insurance_salary:
                insurance_salary= str(item_dict.insurance_salary).split(".")
                insurance_salary_pound = insurance_salary[0]
                if len(insurance_salary)>1:
                    insurance_salary_cent = insurance_salary[1]

            data = {
                'employee': item_dict.name,
                'employee_name': item_dict.employee_name,
                'health_insurance_no': item_dict.health_insurance_no,
                'national_id': item_dict.national_id,
                'date_of_joining': item_dict.date_of_joining,
                'gender': item_dict.gender,
                'gross_salary': item_dict.gross_salary,
                'insurance_salary': item_dict.insurance_salary,
                "gross_salsry_pound" : gross_salsry_pound,
                "gross_salsry_cent" : gross_salsry_cent,
                "insurance_salary_pound" : insurance_salary_pound,
                "insurance_salary_cent": insurance_salary_cent
                
            }
            result.append(data)

    return result


# def get_price_map(price_list_names, buying=0, selling=0):
#     price_map = {}

#     if not price_list_names:
#         return price_map

#     rate_key = "Buying Rate" if buying else "Selling Rate"
#     price_list_key = "Buying Price List" if buying else "Selling Price List"

#     filters = {"name": ("in", price_list_names)}
#     if buying:
#         filters["buying"] = 1
#     else:
#         filters["selling"] = 1

#     pricing_details = frappe.get_all("Item Price",
#                                      fields=["name", "price_list", "price_list_rate"], filters=filters)

#     for d in pricing_details:
#         name = d["name"]
#         price_map[name] = {
#             price_list_key: d["price_list"],
#             rate_key: d["price_list_rate"]
#         }

#     return price_map
