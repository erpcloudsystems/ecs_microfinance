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
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 140
		},
		{
			"label": _("Employee No"),
			"fieldname": "employee_number",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": _("Designation"),
			"fieldname": "designation",
			"fieldtype": "Link",
			"options": "Designation",
			"width": 140
		},
		{
			"label": _("Branch"),
			"fieldname": "branch",
			"fieldtype": "Link",
			"options": "Branch",
			"width": 140
		},
		{
			"label": _("Company mobile"),
			"fieldname": "cell_number",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Personal Mobile"),
			"fieldname": "mobile_2",
			"fieldtype": "Data",
			"width": 95
		},
		
		{
			"label": _("Age"),
			"fieldname": "age",
			"fieldtype": "Data",
			"width": 80
		},
		{
			"label": _("Date of Joining"),
			"fieldname": "date_of_joining",
			"fieldtype": "Date",
			"width": 150
		},
		{
			"label": _("Reliving Date"),
			"fieldname": "relieving_date",
			"fieldtype": "date",
			"width": 120
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
						`tabEmployee`.employee_number as employee_number,
						`tabEmployee`.employee_name as employee_name,
						`tabEmployee`.designation as designation,
						`tabEmployee`.branch as branch,
						`tabEmployee`.cell_number as cell_number,
						`tabEmployee`.mobile_2 as mobile_2,
						`tabEmployee`.status as status,
						`tabEmployee`.date_of_joining as date_of_joining,
						`tabEmployee`.relieving_date as relieving_date
					from
						`tabEmployee`
					where
							   1=1		   
				{conditions}


				""".format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'employee_number': item_dict.employee_number,
				'employee_name': item_dict.employee_name,
				'status': item_dict.status,
				'designation': item_dict.designation,
				'branch': item_dict.branch,
				'cell_number': item_dict.cell_number,
				'mobile_2': item_dict.mobile_2,
				'date_of_joining': item_dict.date_of_joining,
				'relieving_date': item_dict.relieving_date
            }
            result.append(data)

    return result


def get_price_map(price_list_names, buying=0, selling=0):
    price_map = {}

    if not price_list_names:
        return price_map

    rate_key = "Buying Rate" if buying else "Selling Rate"
    price_list_key = "Buying Price List" if buying else "Selling Price List"

    filters = {"name": ("in", price_list_names)}
    if buying:
        filters["buying"] = 1
    else:
        filters["selling"] = 1

    pricing_details = frappe.get_all("Item Price",
                                     fields=["name", "price_list", "price_list_rate"], filters=filters)

    for d in pricing_details:
        name = d["name"]
        price_map[name] = {
            price_list_key: d["price_list"],
            rate_key: d["price_list_rate"]
        }

    return price_map
