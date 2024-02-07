from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, get_fullname, add_days, nowdate, get_datetime, time_diff, time_diff_in_hours, time_diff_in_seconds, get_last_day, get_first_day
from hrms.hr.utils import set_employee_name, get_leave_period, share_doc_with_approver
from hrms.hr.doctype.leave_block_list.leave_block_list import get_applicable_block_dates
from erpnext.setup.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import daterange
from hrms.hr.doctype.leave_ledger_entry.leave_ledger_entry import create_leave_ledger_entry
from frappe.model.document import Document
import datetime

from datetime import timedelta, datetime

class HourlyLeaveApplication(Document):

	def on_cancel(self):
		self.cancel_trans()

	def before_validate(self):
		self.set_date()


	def validate(self):
		# self.validate_balance()
		pass
	def before_insert(self):
		self.validate_balance()
		pass

	def on_submit(self):
		self.update_checkin()

		# self.create_extra()

	def set_date(self):
		cur_date = self.date
		period = frappe.db.sql(""" select start_date as start_date , end_date as end_date from `tabPayroll Period` where '{cur_date}' >= start_date and  '{cur_date}' <= end_date """.format(cur_date=cur_date),as_dict=1)
		for x in period:
			self.start_date = x.start_date
			self.end_date = x.end_date


	def validate_balance(self):
		date = datetime.strptime(str(self.date), '%Y-%m-%d')
		count_per_month = frappe.db.sql(
			"""
            SELECT COUNT(name) as count,
            sum(hours) as hours
            FROM `tabHourly Leave Application`
            WHERE employee=%s 
            AND MONTH(date) = MONTH(%s)
            AND docstatus=0
            """, (self.employee, self.date), as_dict=True)
		duplicates_hourly_leave = frappe.db.sql(
			"""
            SELECT name
            FROM `tabHourly Leave Application`
            WHERE employee=%s 
            AND date = %s
            AND docstatus != 2             """, (self.employee, self.date), as_dict=True)
		if duplicates_hourly_leave:
			frappe.throw(
				f"You Are Only Allowed 1 time per day.")
		count = count_per_month[0]['count']
		hours = count_per_month[0]['hours']
		# if count >= 2:
		# 	frappe.throw("You Are Only Allowed Two Excuse Per Month")
		if (int((hours or 0)) + int(self.hours)) > 4:
			remaining = 4 - (hours or 0)
			frappe.throw(
				f"You Are Only Allowed 4 Hours per Month. Used: {hours} Minutes. You have Only{remaining} Minutes In This Month.")

		# for m in count_per_month:
		# 	if m.count > 2 and self.hours == "2":
		# 		#frappe.msgprint(month_end)
		# 		frappe.throw("You Are Only Allowed For One Hourly Leave Application Per Month !")
				#self.description = m.total_hours

			# if m.count == 2 and self.hours ==:
			# 	#frappe.msgprint(month_end)
			# 	frappe.throw("You Are Only Allowed For One Hourly Leave Application Per Month !")
			# else:
			# 	pass


	def update_checkin(self):
		date = self.date
		employee = self.employee
		if self.leave_type == "IN":
			checkins = frappe.db.sql("""select name as name , time as time from `tabEmployee Checkin` where date(time) = '{date}' and employee = '{employee}' and log_type = 'IN' and custom_hour_leave_applied =0""".format(employee=employee,date=date),as_dict=1)
			for x in checkins:
				if self.hours ==1:
					newtime = (x.time + timedelta(hours=(-1))).strftime('%y-%m-%d %H:%M:%S')
				else:
					newtime = (x.time + timedelta(hours=(-2))).strftime('%y-%m-%d %H:%M:%S')
				newcheckin = x.name
				frappe.db.sql(""" update `tabEmployee Checkin` set time = '{newtime}' where name ='{newcheckin}' """.format(newcheckin=newcheckin,newtime=newtime))
				frappe.db.sql(""" update `tabEmployee Checkin` set custom_hour_leave_applied = 1 where name ='{newcheckin}' """.format(newcheckin=newcheckin))
		elif self.leave_type == "OUT":
			checkins = frappe.db.sql(
				"""select name as name , time as time from `tabEmployee Checkin` where date(time) = '{date}' and employee = '{employee}' and log_type = 'OUT' and custom_hour_leave_applied =0""".format(
					employee=employee, date=date), as_dict=1)
			for x in checkins:
				if self.hours ==1:
					newtime = (x.time + timedelta(hours=(1))).strftime('%y-%m-%d %H:%M:%S')
				else:
					newtime = (x.time + timedelta(hours=(2))).strftime('%y-%m-%d %H:%M:%S')
				newcheckin = x.name
				frappe.db.sql(""" update `tabEmployee Checkin` set time = '{newtime}' where name ='{newcheckin}' """.format(newcheckin=newcheckin, newtime=newtime))
				frappe.db.sql(""" update `tabEmployee Checkin` set custom_hour_leave_applied = 1 where name ='{newcheckin}' """.format(newcheckin=newcheckin))
		'''
		if self.hours == '2':
			compo = frappe.db.get_value("Company", self.company, "late")
			new_doc_hd = frappe.get_doc(dict(
				doctype='Extra Salary',
				currency='EGP',
				employee=self.employee,
				company=self.company,
				salary_component=compo,
				ref_doctype='Hourly Leave Application',
				ref_docname=self.name,
				amount=1,
				payroll_date=self.date,
				overwrite_salary_structure_amount=1
			))
			new_doc_hd.insert()
			new_doc_hd.submit()
		'''
	def cancel_trans(self):
		date = self.date
		employee = self.employee
		if self.leave_type == "IN":
			checkins = frappe.db.sql("""select name as name , time as time from `tabEmployee Checkin` where date(time) = '{date}' and employee = '{employee}' and log_type = 'IN' and custom_hour_leave_applied =1""".format(employee=employee,date=date),as_dict=1)
			for x in checkins:
				if self.hours ==1:
					newtime = (x.time + timedelta(hours=(1))).strftime('%y-%m-%d %H:%M:%S')
				else:
					newtime = (x.time + timedelta(hours=(2))).strftime('%y-%m-%d %H:%M:%S')
				#newtime = (x.time + timedelta(hours=(1))).strftime('%y-%m-%d %H:%M:%S')
				newcheckin = x.name
				frappe.db.sql(""" update `tabEmployee Checkin` set time = '{newtime}' where name ='{newcheckin}' """.format(newcheckin=newcheckin,newtime=newtime))
				frappe.db.sql(""" update `tabEmployee Checkin` set custom_hour_leave_applied = 0 where name ='{newcheckin}' """.format(newcheckin=newcheckin))
		elif self.leave_type == "OUT":
			checkins = frappe.db.sql(
				"""select name as name , time as time from `tabEmployee Checkin` where date(time) = '{date}' and employee = '{employee}' and log_type = 'OUT' and custom_hour_leave_applied =1""".format(
					employee=employee, date=date), as_dict=1)
			for x in checkins:
				if self.hours ==1:
					newtime = (x.time + timedelta(hours=(-1))).strftime('%y-%m-%d %H:%M:%S')
				else:
					newtime = (x.time + timedelta(hours=(-2))).strftime('%y-%m-%d %H:%M:%S')
				#newtime = (x.time + timedelta(hours=(-1))).strftime('%y-%m-%d %H:%M:%S')
				newcheckin = x.name
				frappe.db.sql(""" update `tabEmployee Checkin` set time = '{newtime}' where name ='{newcheckin}' """.format(newcheckin=newcheckin, newtime=newtime))
				frappe.db.sql(""" update `tabEmployee Checkin` set custom_hour_leave_applied = 0 where name ='{newcheckin}' """.format(newcheckin=newcheckin))




	pass
