// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.query_reports["Staffing Plan"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options":"Designation"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options":"Department"
		},
		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options":"Branch"
		},
		{
			"fieldname": "governorate",
			"label": __("Governorate"),
			"fieldtype": "Link",
			"options":"Governorate"
		},

	]
};
