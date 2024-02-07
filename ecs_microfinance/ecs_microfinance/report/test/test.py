# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from itertools import groupby
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import frappe
from frappe import _


Filters = frappe._dict


def execute(filters: Optional[Filters] = None) -> Tuple:
	if filters.to_date <= filters.from_date:
		frappe.throw(_('"From Date" can not be greater than or equal to "To Date"'))
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns() -> List[Dict]:
	return [
		{
			"label": _("Leave(s) Expired Date"),
			"fieldtype": "date",
			"fieldname": "leaves_expired_date",
			"width": 140,
		}
	]


def get_data(filters: Filters) -> List:
	leave_types = frappe.db.get_list("Leave Type", pluck="name", order_by="name")
	active_employees = frappe.get_list(
		"Employee",
		fields=["name", "employee_name", "department", "user_id", "leave_approver"],
	)

	data = []
	for leave_type in leave_types:
		if len(active_employees) > 1:
			data.append({"leave_type": leave_type})
		else:
			row = frappe._dict({"leave_type": leave_type})

		for employee in active_employees:
			if frappe.db.exists("Leave Allocation",{"employee":employee.name,"leave_type":leave_type}):
					leave_doc= frappe.get_doc("Leave Allocation",{"employee":employee.name,"leave_type":leave_type})
					if leave_doc.carry_forward == 1:
						leave_type= frappe.get_doc("Leave Type",leave_type)
						from_date = leave_doc.from_date
						days_to_add = leave_type.expire_carry_forwarded_leaves_after_days
						new_date = from_date + timedelta(days=days_to_add)
						row.leaves_expired_date = new_date
			else:
				row.leaves_expired_date = None

	return data


