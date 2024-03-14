from hrms.hr.doctype.attendance.attendance import Attendance
from frappe.utils import getdate
import frappe

class CustomAttendance(Attendance):
    def validate_attendance_date(self):
        date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")

        # # leaves can be marked for future dates
        # if (
        #     self.status != "On Leave"
        #     and not self.leave_application
        #     and getdate(self.attendance_date) > getdate(nowdate())
        # ):
            # frappe.throw(
            # 	_("Attendance can not be marked for future dates: {0}").format(
            # 		frappe.bold(format_date(self.attendance_date)),
            # 	)
            # )
        if date_of_joining and getdate(self.attendance_date) < getdate(date_of_joining):
            frappe.throw(
                _("Attendance date {0} can not be less than employee {1}'s joining date: {2}").format(
                    frappe.bold(format_date(self.attendance_date)),
                    frappe.bold(self.employee),
                    frappe.bold(format_date(date_of_joining)),
                )
            )
    