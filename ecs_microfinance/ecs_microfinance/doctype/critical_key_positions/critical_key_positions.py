# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CriticalKeyPositions(Document):
	@frappe.whitelist()
	def get_designation(doc, method=None):
		selected_designation = {}

		if doc.designation:
			condition = ""
			designation = doc.designation
			critical_key = doc.critical_key

			if designation:
				condition += f"AND `tabDesignation`.name = '{designation}'"
			
			if critical_key:
				condition +=f"AND `tabDesignation`.custom_critical_key = '{critical_key}'"


			selected_designation = frappe.db.sql("""
			select `tabDesignation`.name as name, `tabDesignation`.custom_critical_key as custom_critical_key, `tabDesignation`.department as department
			from `tabDesignation`
			where `tabDesignation`.department = '{department}'
			{condition}
			""".format(department=doc.department, condition = condition), as_dict=1)


		if selected_designation != []:
			for i in selected_designation:
				doc.append("designation_critical_key", {
					"designation": i.name,
					"critical_key": i.custom_critical_key,
					"department": i.department,
				})


	
