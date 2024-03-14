# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeContracts(Document):
	def on_submit(self):
		frappe.db.set_value("Employee", self.employee, "contract_end_date", self.new_contract_end_date)
		record_name = str(self.name) + str(self.employee)
		frappe.db.sql(""" INSERT INTO `tabContract History Logs`
										(date_of_joining, current_contract_end_date, renewal_period, new_contract_start_date, new_contract_end_date, parent, parentfield, parenttype, name)
								VALUES ('{date_of_joining}', '{current_contract_end_date}', '{renewal_period}', '{new_contract_start_date}', '{new_contract_end_date}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
								""".format(date_of_joining=self.date_of_joining, renewal_period=self.renewal_period,
											new_contract_start_date=self.new_contract_start_date, new_contract_end_date=self.new_contract_end_date,
											parent=self.employee, parenttype="Employee", current_contract_end_date=self.current_contract_end_date,
											parentfield="contract_history_logs", record_name=record_name))



	def on_cancel(self):
		frappe.db.set_value("Employee", self.employee, "contract_end_date", self.current_contract_end_date)
		record_name = str(self.name) + str(self.employee)
		frappe.db.sql(""" DELETE FROM `tabContract History Logs` where parent = '{parent}' and parentfield = '{parentfield}' and parenttype = '{parenttype}' and name = '{record_name}'
			 """.format(parent=self.employee, parenttype="Employee", parentfield="contract_history_logs", record_name=record_name))