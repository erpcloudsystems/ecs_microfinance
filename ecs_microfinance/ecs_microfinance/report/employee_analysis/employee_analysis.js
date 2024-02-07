// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee analysis"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"parameter",
			"label": __("Parameter"),
			"fieldtype": "Select",
			"options": ["Branch","Grade","Department","Designation", "Employment Type"],
			"reqd": 1
		},
		{
			"fieldname":"Branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Branch",
			
		},
		{
			"fieldname":"Department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			
		},
		{
			"fieldname":"Designation",
			"label": __("Designation"),
			"fieldtype": "Link",
			"options": "Designation",
			
		}
		
	]
};
