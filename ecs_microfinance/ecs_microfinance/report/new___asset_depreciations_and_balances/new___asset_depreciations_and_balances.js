// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["NEW___Asset Depreciations and Balances"] = {
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
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
			"reqd": 1
		},
		{
			"fieldname":"asset_category",
			"label": __("Asset Category"),
			"fieldtype": "Link",
			"options": "Asset Category"
		},
		{
			"fieldname":"fixed_asset_account",
			"label": __("Fixed Asset Account"),
			"fieldtype": "Link",
			"options": "Account"
		}
	]

};
