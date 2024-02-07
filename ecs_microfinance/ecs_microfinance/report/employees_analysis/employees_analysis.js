// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employees Analysis"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "Branch",
            "label": __("Branch"),
            "fieldtype": "Link",
            "options": "Branch"
        },
        {
            "fieldname": "Department",
            "label": __("Department"),
            "fieldtype": "Link",
            "options": "Department",
            "get_query": () => {
                let Branch = frappe.query_report.get_filter_value('Branch');
                return {
                    query: "ecs_microfinance.ecs_microfinance.report.employees_analysis.employees_analysis.get_department",
                    filters: {
                        Branch: Branch
                    }
                };
            }
        },
        {
            "fieldname": "Designation",
            "label": __("Designation"),
            "fieldtype": "Link",
            "options": "Designation",
            "get_query": () => {
                let Branch = frappe.query_report.get_filter_value('Branch');
                let Department = frappe.query_report.get_filter_value('Department');
                return {
                    query: "ecs_microfinance.ecs_microfinance.report.employees_analysis.employees_analysis.get_designation",
                    filters: {
                        Branch: Branch,
                        Department: Department
                    }
                };
            }
        }
    ]
};
