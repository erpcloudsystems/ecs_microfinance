from hrms.hr.doctype.attendance_request.attendance_request import AttendanceRequest

import frappe
from frappe import _
from frappe.utils import get_link_to_form ,getdate,date_diff,add_days
from hrms.hr.utils import validate_active_employee


class CustomAttendanceRequest(AttendanceRequest):
    def create_attendance_records(self):
        request_days = date_diff(self.to_date, self.from_date) + 1
        for day in range(request_days):
            attendance_date = add_days(self.from_date, day)
            # if self.should_mark_attendance(attendance_date):
            self.create_or_update_attendance(attendance_date)
    
    def validate(self):
        validate_active_employee(self.employee)
        validate_dates(self, self.from_date, self.to_date)
        self.validate_half_day()
        self.validate_request_overlap()
    def throw_overlap_error(self, overlapping_request: str):
        msg = _(
            "Employee {0} already has an Attendance Request {1} that overlaps with this period"
        ).format(
            frappe.bold(self.employee),
            get_link_to_form("Attendance Request", overlapping_request),
        )

        # frappe.msgprint(
        # 	msg, title=_("Overlapping Attendance Request"), indicator="orange"
        # )

def validate_dates(doc, from_date, to_date):
    date_of_joining, relieving_date = frappe.db.get_value(
        "Employee", doc.employee, ["date_of_joining", "relieving_date"]
    )
    if getdate(from_date) > getdate(to_date):
        frappe.throw(_("To date can not be less than from date"))
    # elif getdate(from_date) > getdate(nowdate()):
    #     frappe.throw(_("Future dates not allowed"))
    elif date_of_joining and getdate(from_date) < getdate(date_of_joining):
        frappe.throw(_("From date can not be less than employee's joining date"))
    elif relieving_date and getdate(to_date) > getdate(relieving_date):
        frappe.throw(_("To date can not greater than employee's relieving date"))
