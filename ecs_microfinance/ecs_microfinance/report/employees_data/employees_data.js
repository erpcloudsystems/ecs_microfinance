// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["employees data"] = {
	"filters": [
		{
			fieldname: 'name',
			label: __('Employee'),
			fieldtype: 'Link',
			Options: "Employee",
		  },
	
		  

	]
};
