// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Insurance Data"] = {
	"filters": [
		{
			fieldname: 'name',
			label: __('Employee'),
			fieldtype: 'Link',
			Options: "Employee",
		  },
	
		  

	]
};
