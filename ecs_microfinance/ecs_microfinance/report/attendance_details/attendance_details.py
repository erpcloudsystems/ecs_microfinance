# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime


def execute(filters=None):
    columns = get_columns()
    data=get_data(filters,columns)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Attendance"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Attendance",
            "width": 100
        },
        {
            "label": _("Date"),
            "fieldname": "attendance_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Code"),
            "fieldname": "code",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 70
        },
        {
            "label": _("Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 200
        },
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 170
        },
        {
            "label": _("Shift"),
            "fieldname": "shift",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },

        {
            "label": _("In Time"),
            "fieldname": "in_time",
            "fieldtype": "Datetime",
            "width": 120
        },
        {
            "label": _("Out Time"),
            "fieldname": "out_time",
            "fieldtype": "Datetime",
            "width": 120
        },
        {
            "label": _("Working Hours"),
            "fieldname": "working_hours",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Attendance Request"),
            "fieldname": "attendance_request",
            "fieldtype": "Link",
            "options": "Attendance Request",
            "width": 160
        },
        {
            "label": _("Leave Application"),
            "fieldname": "leave_application",
            "fieldtype": "Link",
            "options": "Leave Application",
            "width": 160
        },
        {
            "label": _("Overtime (min)"),
            "fieldname": "overtime",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Late (min)"),
            "fieldname": "lates",
            "fieldtype": "Float",
            "width": 100
        }
        ,
        {
            "label": _("Early Overtime (min)"),
            "fieldname": "early_come",
            "fieldtype": "Float",
            "width": 100
        }
         ,
        {
            "label": _(" Early Leave (min)"),
            "fieldname": "early_leave",
            "fieldtype": "Float",
            "width": 100
        }
    ]

def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_attendance_data(filters)
    return item_price_qty_data

def get_attendance_data(filters):
    from_dates = filters.get("from_date")
    to_dates = filters.get("to_date")
    conditions = []
    
    if 'department' in filters:
        conditions.append(f"(att.department = '{filters['department']}' )")
    if 'employee' in filters:
        conditions.append(f"(att.employee = '{filters['employee']}' )")
    if 'shift' in filters:
        conditions.append(f"(att.shift = '{filters['shift']}' )")
    if 'branch' in filters:
        conditions.append(f"(att.custom_branch = '{filters['branch']}' )")

    query = """
        SELECT
            att.name AS name,
            att.employee AS code,
            att.employee_name AS employee_name,
            att.custom_branch AS branch,
            att.department AS department,
            att.shift AS shift,
            att.status AS status,
            att.in_time AS in_time,
            att.out_time AS out_time,
            att.working_hours AS working_hours,
            att.attendance_date AS attendance_date,
            att.attendance_request AS attendance_request,
            att.leave_application AS leave_application,

        CASE
            WHEN  ( TIME_TO_SEC(TIME(in_time)) - TIME_TO_SEC(( SELECT (start_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) )) < 0 THEN 0
            ELSE ( TIME_TO_SEC(TIME(in_time)) - TIME_TO_SEC(( SELECT (start_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) )) / 60
        END AS lates,

        CASE
            WHEN  ( TIME_TO_SEC(TIME(in_time)) - TIME_TO_SEC(( SELECT (start_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) )) > 0 THEN 0
            ELSE ABS((TIME_TO_SEC(TIME(in_time)) - TIME_TO_SEC(( SELECT (start_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) )) / 60)
        END AS early_come,

        CASE
            WHEN ( TIME_TO_SEC(TIME(out_time)) - TIME_TO_SEC(( SELECT (end_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) ))  < 0 THEN 0
            ELSE ( TIME_TO_SEC(TIME(out_time)) - TIME_TO_SEC(( SELECT (end_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) )) / 60
        END AS overtime,
                                
        CASE
            WHEN ( TIME_TO_SEC(TIME(out_time)) - TIME_TO_SEC(( SELECT (end_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) ))  > 0 THEN 0
            ELSE ABS(( TIME_TO_SEC(TIME(out_time)) - TIME_TO_SEC(( SELECT (end_time) from `tabShift Type` where name =  att.shift  ORDER BY creation DESC LIMIT 1) )) / 60)
        END AS early_leave

        FROM
            `tabAttendance` att


        WHERE
            att.docstatus = 1
            AND att.attendance_date BETWEEN %s AND %s
    """.format(from_dates=from_dates, to_dates=to_dates)

    if conditions:
        query += " AND " + " AND ".join(conditions)

    item_results = frappe.db.sql(query, (from_dates, to_dates), as_dict=1)
    return item_results
    # frappe.msgprint(str(item_results))
    # result = []
    # if item_results:
    #     for item_dict in item_results:
    #         data = {
    #             'name': item_dict.name,
    #             'code': item_dict.code,
    #             'employee_name': item_dict.employee_name,
    #             'department': item_dict.department,
    #             'shift': item_dict.shift,
    #             'status': item_dict.status,
    #             'in_time': item_dict.in_time,
    #             'out_time': item_dict.out_time,
    #             'working_hours': item_dict.working_hours,
    #             'attendance_date': item_dict.attendance_date,
    #             'attendance_request': item_dict.attendance_request,
    #             'leave_application': item_dict.leave_application,
    #         }
    #         pp = frappe.get_last_doc('Shift Type', filters={"name": item_dict.shift})
            
    #         def calculate_difference(time1, time2):
    #             if time1 and time2:
    #                 time1 = datetime.strptime(str(time1.time()), '%H:%M:%S')
    #                 time2 = datetime.strptime(str(time2), '%H:%M:%S')
    #                 time_difference = (time1 - time2).total_seconds()
    #                 return int(time_difference) if time_difference > 0 else 0
    #             return 0

    #         data['lates'] = calculate_difference(item_dict.in_time, pp.start_time)
    #         data['overtime'] = calculate_difference(item_dict.out_time, pp.end_time)

    #         result.append(data)

    return result

