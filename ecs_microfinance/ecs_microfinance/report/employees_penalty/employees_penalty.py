# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Code"),
            "fieldname": "code",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 70
        },
        {
            "label": _("اسم المظف"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("القسم"),
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("الفرع"),
            "fieldname": "branch",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("الوظيفة"),
            "fieldname": "designation",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("غياب"),
            "fieldname": "num_absent",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "label": _("حضور"),
            "fieldname": "num_present",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "label": _("اجازة"),
            "fieldname": "On_Leave",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "label": _("اجازة بدون اجر"),
            "fieldname": "On_Leave_whithout_pay",
            "fieldtype": "Int",
            "width": 200
        },
        {
            "label": _("جزاء التأخيرات"),
            "fieldname": "late",
            "fieldtype": "float",
            "width": 200
        },
        {
            "label": _("جزاء الانصراف المبكر"),
            "fieldname": "early_leave",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("جزاء نسيان البصمة"),
            "fieldname": "missing_finger_print",
            "fieldtype": "Float",
            "width": 100
        }
        ,
        {
            "label": _("جزاء الغياب"),
            "fieldname": "absent",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("الجزاء الاداري"),
            "fieldname": "total_penalty",
            "fieldtype": "Float",
            "width": 100
        }
        
    ]

def get_data(filters, columns):
    employee_penalty = []
    employee_penalty = get_attendance_data(filters)
    return employee_penalty


def get_attendance_data(filters):
    from_dates = filters.get("from_date")
    to_dates = filters.get("to_date")
    conditions = ""
    if filters.get("department"):
        conditions += f" AND A.department = '{filters.get('department')}'"
    if filters.get("employee"):
        conditions += f" AND A.employee = '{filters.get('employee')}'"
    if filters.get("shift"):
        conditions += f" AND shift = '{filters.get('shift')}'"
    if filters.get("branch"):
        conditions += f" AND A.custom_branch = '{filters.get('branch')}'"
    if filters.get("designation"):
        conditions += f" AND E.designation = '{filters.get('designation')}'"

    query = """
    SELECT
        A.employee as code,
        A.name as name,
        A.employee_name as employee_name,
        A.department as department,
        A.custom_branch as branch,
        E.designation as designation,
        SUM(CASE WHEN Es.salary_component ="عدد ايام الغياب" THEN Es.amount ELSE 0 END) AS absent,
        SUM(CASE WHEN Es.salary_component ="عدد ايام نسيان البصمة" THEN Es.amount ELSE 0 END) AS missing_finger_print,
        SUM(CASE WHEN Es.salary_component ="عدد ايام جزاء الانصراف المبكر" THEN Es.amount ELSE 0 END) AS early_leave,
        SUM(CASE WHEN Es.salary_component ="عدد ايام التاخير" THEN Es.amount ELSE 0 END) AS late,
        COUNT(CASE WHEN A.status = 'Absent' THEN 1 ELSE NULL END) AS num_absent,
        COUNT(CASE WHEN A.status = 'Present' THEN 1 ELSE NULL END) AS num_present,
        COUNT(CASE WHEN A.status = 'On Leave' and A.leave_type != "أجازة بدون اجر" THEN 1 ELSE NULL END) AS On_Leave,
        COUNT(CASE WHEN A.status = 'On Leave' and A.leave_type = "أجازة بدون اجر" THEN 1 ELSE NULL END) AS On_Leave_whithout_pay,
        COUNT(CASE WHEN A.status = 'Half Day' THEN 1 ELSE NULL END) AS Half_Day
    FROM
        `tabAttendance` A 
    LEFT JOIN
        `tabExtra Salary` Es
    ON A.name = Es.attendance
    JOIN
        `tabEmployee` E
    ON A.employee = E.name
    WHERE
        A.docstatus = 1
        AND A.attendance_date BETWEEN '{from_dates}' AND '{to_dates}'
        {conditions}
    GROUP BY
        A.employee

    """.format(conditions=conditions, from_dates=from_dates, to_dates=to_dates)

    result = frappe.db.sql(query, as_dict=1)
    
    if result:
        for row in result:
            employee = row["code"]
            row["total_penalty"] =frappe.db.sql(""" 
                                                select sum(amount) 
                                                from `tabExtra Salary` 
                                                where employee = '{employee}' 
                                                and salary_component = 'عدد ايام الجزاء الاداري' 
                                                and payroll_date between '{from_dates}' AND '{to_dates}' 
                                                """.format(employee=employee,from_dates=from_dates, to_dates=to_dates), as_dict=1)[0]["sum(amount)"]
    return result




# frappe.db.get_value("Extra Salary", {"employee":row["code"],"salary_component":"عدد ايام الجزاء الاداري","payroll_date":["between",[from_dates,to_dates]]}, "sum(amount)")