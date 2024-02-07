# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DecreaseOfFees(Document):
	def validate(self):
		if self.current_bond_size <= self.new_bond_size:
			frappe.throw("New Bond Size Must Be Smaller Than Current Bond Size")
