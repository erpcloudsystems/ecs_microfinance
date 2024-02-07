# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TrainingBeforeJoining(Document):
    @frappe.whitelist()
    def get_attendance_no(doc, method=None):
        number_of_attendances = frappe.db.sql(f"""
                        SELECT
                           COUNT(*)
                        FROM `tabAttendance` AS a 
                        WHERE a.employee = '{doc.employee}'  
                            AND a.attendance_date BETWEEN '{doc.training_start_date}' AND '{doc.training_end_date}'
                            AND a.status = 'Present'
                        """)[0][0]

        doc.attendance_no = number_of_attendances

    @frappe.whitelist()
    def on_submit(doc, method=None):
        if doc.action == "تعيين(اقرار صلاحية)":
            frappe.db.sql(f"""
            UPDATE `tabEmployee`
            SET date_of_joining = '{doc.date_of_joining}', employment_type = '{doc.new_employment_type}'
            WHERE name = '{doc.employee}';
            """)

        record_name = str(doc.name) + str(doc.employee)
        frappe.db.sql(""" INSERT INTO `tabTraining Before Joining Logs`
        								(training_start_date, training_end_date, employment_type, new_employment_type, parent, parentfield, parenttype, name)
        						VALUES ('{training_start_date}', '{training_end_date}', '{employment_type}', '{new_employment_type}', '{parent}', '{parentfield}', '{parenttype}', '{record_name}')
        						""".format(training_start_date=doc.training_start_date, training_end_date=doc.training_end_date,
                                           employment_type=doc.employment_type,
                                           new_employment_type=doc.new_employment_type,
                                           parent=doc.employee, parenttype="Employee",
                                           parentfield="training_before_joining_logs", record_name=record_name))

    def on_cancel(doc):
        record_name = str(doc.name) + str(doc.employee)
        frappe.db.sql(""" DELETE FROM `tabTraining Before Joining Logs` where parent = '{parent}' and parentfield = '{parentfield}' and parenttype = '{parenttype}' and name = '{record_name}'
    		 """.format(parent=doc.employee, parenttype="Employee", parentfield="training_before_joining_logs",
                        record_name=record_name))