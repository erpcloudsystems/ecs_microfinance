// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.query_reports["Employee Dated (probation )"] = {
	"filters": [
		{
			fieldname: "name",
			label: "Employee Name",
			fieldtype: "Link",
			options: "Employee"
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
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1)
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		}

	

	]
};
