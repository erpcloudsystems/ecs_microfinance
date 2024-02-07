// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset Balance"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_default("year_start_date")
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_default("year_end_date")
		},


		{
			"fieldname": "asset_category",
			"label": __("مجموعة الاصول"),
			"fieldtype": "MultiSelectList",
            get_data: function(txt) {
				return frappe.db.get_link_options('Asset Category', txt);
			}
		},


		{
			"fieldname": "territory",
			"label": __("مكان التواجد"),
			"fieldtype": "MultiSelectList",
            get_data: function(txt) {
				return frappe.db.get_link_options('Territory', txt);
			}
		},

//
//		{
//			"fieldname": "territory",
//			"label": __("مكان التواجد"),
//			"fieldtype": "Link",
//			"options":"Territory",
//		},

	]
}

