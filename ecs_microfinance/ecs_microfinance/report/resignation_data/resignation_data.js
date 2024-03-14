// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.query_reports["Resignation Data"] = {
	"filters": [
		{
			fieldname: "name",
			label: "Employee Name",
			fieldtype: "Link",
			options: "Resignation"
		},
		{
			fieldname: "designation",
			label: "Designation",
			fieldtype: "Link",
			options: "Designation"
		},
		{
			fieldname: "department",
			label: "Department",
			fieldtype: "Link",
			options: "Department"
		},
		{
			fieldname: "branch",
			label: "Branch",
			fieldtype: "Link",
			options: "Branch"
		},
		{
			fieldname: "docstatus",
			label: "Selected Satus",
			fieldtype: "Select",
			options: ["", "Pending", "Approved"]
		}

	]
};
