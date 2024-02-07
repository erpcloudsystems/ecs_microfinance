# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CashEntry(Document):
	@frappe.whitelist()
	def before_validate(self):
		sum1 = len(self.expense_entry_account)
		percent = 0
		for x in self.expense_entry_account:
			x.account = self.account
			if self.type == "Automatic":
				x.percentage = 100 / sum1
				x.amount = (float(self.amount) * float(x.percentage))/100

			if self.type == "Manual":
				x.amount = (float(self.amount) * float(x.percentage))/100

			if self.type == "Amount":
				x.percentage = (x.amount / self.amount)*100
				percent += x.percentage
		if percent > 100:
			frappe.throw(" percent Cannot Be Greater than 100% ")
	@frappe.whitelist()
	def validate(self):
		self.total_amount = 0
		for x in self.expense_entry_account:
			if x.is_credit == 0:
				self.total_amount += x.amount

	@frappe.whitelist()
	def before_submit(self):
		totals = 0
		for x in self.expense_entry_account:
			totals += x.amount

		#if self.total_amount != (self.amount + totals):
			#frappe.throw(" Amount Must Be Equal To Total Amount Of Accounts Table ... Difference is " + str(self.amount - self.total_amount))

	@frappe.whitelist()
	def on_submit(self):
		if self.payment_type == "Pay":
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_from,
					"credit": self.amount,
					"debit": 0,
					"credit_in_account_currency": self.amount
				}
			]

			for x in self.expense_entry_account:
				if x.is_credit == 1:
					accounts.append({
					"doctype": "Journal Entry Account",
					"account": x.account,
					"credit": x.amount,
					"debit": 0,
					"territory": x.territory,
					"credit_in_account_currency": x.amount
				})
				else:
					accounts1 = {
						"doctype": "Journal Entry Account",
						"account": x.account,
						"credit": 0,
						"debit": x.amount,
						"debit_in_account_currency": x.amount,
						"party_type": x.party_type,
						"party": x.party,
						"cost_center": x.cost_center,
						"branch": x.branch,
						"project": x.project,
						"territory": x.territory,
						"user_remark": x.user_remark
					},
					accounts.extend(accounts1)

			new_doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"reference_doctype": "Cash Entry",
				"reference_link": self.name,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"payment_type": self.payment_type,
				"company": self.company,
				"user_remark": self.remarks
			})

			new_doc.insert(ignore_permissions=True)
			new_doc.submit()

		if self.payment_type == "Receive":
			accounts = [
				{
					"doctype": "Journal Entry Account",
					"account": self.account_paid_to,
					"credit": 0,
					"debit": self.amount,
					"debit_in_account_currency": self.amount				}
			]

			for x in self.expense_entry_account:
				accounts1 = {
								"doctype": "Journal Entry Account",
								"account": x.account,
								"credit": x.amount,
								"debit": 0,
								"credit_in_account_currency": x.amount,
								"party_type": x.party_type,
								"party": x.party,
								"cost_center": x.cost_center,
								"branch": x.branch,
								"project": x.project,
								"territory": x.territory,
								"user_remark": x.user_remark
							},
				accounts.extend(accounts1)

			new_doc = frappe.get_doc({
				"doctype": "Journal Entry",
				"voucher_type": "Journal Entry",
				"reference_doctype": "Cash Entry",
				"reference_link": self.name,
				"cheque_no": self.name,
				"cheque_date": self.posting_date,
				"posting_date": self.posting_date,
				"accounts": accounts,
				"payment_type": self.payment_type,
				"company": self.company,
				"user_remark": self.remarks
			})

			new_doc.insert(ignore_permissions=True)
			new_doc.submit()