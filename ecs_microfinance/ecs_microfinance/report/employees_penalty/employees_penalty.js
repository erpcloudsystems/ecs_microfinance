// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employees Penalty"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.get_today()
		},
		{
			fieldname: "employee",
			label: __("Employee"),
			fieldtype: "Link",
			options:"Employee",
		},
		{
			fieldname: "shift",
			label: __("Shift"),
			fieldtype: "Link",
			options:"Shift Type",
		},
		{
			fieldname: "department",
			label: __("Department"),
			fieldtype: "Link",
			options:"Department",
		},
		{
			fieldname: "designation",
			label: __("Designation"),
			fieldtype: "Link",
			options:"Designation",
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options:"Branch",
		},
	]
};
