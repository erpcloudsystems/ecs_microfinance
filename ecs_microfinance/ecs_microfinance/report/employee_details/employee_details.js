// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Details"] = {
	"filters": [
		{
			fieldname: "name",
			label: "Name ",
			fieldtype:"Link",
			options:"Employee"
		},
		{
			fieldname:"designation",
			label:"Designation",
			fieldtype:"Link",
			options:"Designation"
		},
		{
			fieldname:"department",
			label:"Department",
			fieldtype:"Link",
			options:"Department"
		},
		{
			fieldname:"branch",
			label:"Branch",
			fieldtype:"Link",
			options:"Branch"
		}

	]
};
