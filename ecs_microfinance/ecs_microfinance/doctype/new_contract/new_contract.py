# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class NewContract(Document):
	def validate(self):
		total_percent = self.upon_signature_percent + self.operation_review_percent + self.rating_comity_percent
		if total_percent!= 100:
			frappe.throw("Total Percentage Must Be 100%")
