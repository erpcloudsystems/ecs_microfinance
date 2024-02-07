# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

from frappe.utils import (
    DATE_FORMAT,
    add_days,
    add_to_date,
    cint,
    comma_and,
    date_diff,
    flt,
    get_link_to_form,
    getdate,
)


class GroupedPayrollEntry(Document):
    @staticmethod
    def validate_employee_attendance(self):
        employees_to_mark_attendance = []
        days_in_payroll, days_holiday, days_attendance_marked = 0, 0, 0
        for employee_detail in self.employees:
            employee_joining_date = frappe.db.get_value(
                "Employee", employee_detail.employee, "date_of_joining"
            )
            start_date = self.start_date
            if employee_joining_date > getdate(self.start_date):
                start_date = employee_joining_date
            days_holiday = self.get_count_holidays_of_employee(
                employee_detail.employee, start_date
            )
            days_attendance_marked = self.get_count_employee_attendance(
                employee_detail.employee, start_date
            )
            days_in_payroll = date_diff(self.end_date, start_date) + 1
            if days_in_payroll > days_holiday + days_attendance_marked:
                employees_to_mark_attendance.append(
                    {
                        "employee": employee_detail.employee,
                        "employee_name": employee_detail.employee_name,
                    }
                )
        return employees_to_mark_attendance

    def make_filters(self):
        filters = frappe._dict()
        filters["company"] = self.company
        filters["branch"] = self.branch
        filters["department"] = self.department
        filters["designation"] = self.designation

        return filters

    @staticmethod
    def get_filter_condition(filters):
        cond = ""
        for f in ["company", "branch", "department", "designation"]:
            if filters.get(f):
                cond += " and t1." + f + " = " + frappe.db.escape(filters.get(f))

        return cond

    @staticmethod
    def get_joining_relieving_condition(start_date, end_date):
        cond = """
            and ifnull(t1.date_of_joining, '1900-01-01') <= '%(end_date)s'
            and ifnull(t1.relieving_date, '2199-12-31') >= '%(start_date)s'
        """ % {
            "start_date": start_date,
            "end_date": end_date,
        }
        return cond

    @staticmethod
    def get_sal_struct(
        company: str, currency: str, salary_slip_based_on_timesheet: int, condition: str
    ):
        return frappe.db.sql_list(
            """
            select
                name from `tabSalary Structure`
            where
                docstatus = 1 and
                is_active = 'Yes'
                and company = %(company)s
                and currency = %(currency)s and
                ifnull(salary_slip_based_on_timesheet,0) = %(salary_slip_based_on_timesheet)s
                {condition}""".format(
                condition=condition
            ),
            {
                "company": company,
                "currency": currency,
                "salary_slip_based_on_timesheet": salary_slip_based_on_timesheet,
            },
        )

    @staticmethod
    def get_emp_list_query(sal_struct, cond, end_date, payroll_payable_account):
        return frappe.db.sql(
            """
                select
                    distinct t1.name as employee, t1.employee_name, t1.department, t1.designation
                from
                    `tabEmployee` t1, `tabSalary Structure Assignment` t2
                where
                    t1.name = t2.employee
                    and t2.docstatus = 1
                    and t1.status != 'Inactive'
            %s order by t2.from_date desc
            """
            % cond,
            {
                "sal_struct": tuple(sal_struct),
                "from_date": end_date,
                "payroll_payable_account": payroll_payable_account,
            },
            as_dict=True,
        )

    @staticmethod
    def remove_payrolled_employees(emp_list, start_date, end_date):
        new_emp_list = []
        for employee_details in emp_list:
            if not frappe.db.exists(
                "Salary Slip",
                {
                    "employee": employee_details.employee,
                    "start_date": start_date,
                    "end_date": end_date,
                    "docstatus": 1,
                },
            ):
                new_emp_list.append(employee_details)

        return new_emp_list

    @staticmethod
    def check_mandatory(self):
        for fieldname in ["company", "start_date", "end_date"]:
            if not self.get(fieldname):
                frappe.throw(_("Please set {0}").format(self.meta.get_label(fieldname)))

    @staticmethod
    def get_emp_list(self):
        """
        Returns list of active employees based on selected criteria
        and for which salary structure exists
        """
        GroupedPayrollEntry.check_mandatory(self)
        filters = GroupedPayrollEntry.make_filters(self)
        cond = GroupedPayrollEntry.get_filter_condition(filters)
        cond += GroupedPayrollEntry.get_joining_relieving_condition(
            self.start_date, self.end_date
        )

        condition = ""
        if self.payroll_frequency:
            condition = """and payroll_frequency = '%(payroll_frequency)s'""" % {
                "payroll_frequency": self.payroll_frequency
            }

        sal_struct = GroupedPayrollEntry.get_sal_struct(
            self.company, self.currency, self.salary_slip_based_on_timesheet, condition
        )
        if sal_struct:
            cond += "and t2.salary_structure IN %(sal_struct)s "
            cond += "and t2.payroll_payable_account = %(payroll_payable_account)s "
            cond += "and %(from_date)s >= t2.from_date"
            emp_list = GroupedPayrollEntry.get_emp_list_query(
                sal_struct, cond, self.end_date, self.payroll_payable_account
            )
            emp_list = GroupedPayrollEntry.remove_payrolled_employees(
                emp_list, self.start_date, self.end_date
            )
            return emp_list

    def fill_employee_details(self, name):
        self_payroll = frappe.get_doc("Payroll Entry", name)
        self_payroll.set("employees", [])
        employees = self.get_emp_list(self_payroll)
        if not employees:
            error_msg = _(
                "No employees found for the mentioned criteria:<br>Company: {0}<br> Currency: {1}<br>Payroll Payable Account: {2}"
            ).format(
                frappe.bold(self_payroll.company),
                frappe.bold(self_payroll.currency),
                frappe.bold(self_payroll.payroll_payable_account),
            )
            if self_payroll.branch:
                error_msg += "<br>" + _("Branch: {0}").format(
                    frappe.bold(self_payroll.branch)
                )
            if self_payroll.department:
                error_msg += "<br>" + _("Department: {0}").format(
                    frappe.bold(self_payroll.department)
                )
            if self_payroll.designation:
                error_msg += "<br>" + _("Designation: {0}").format(
                    frappe.bold(self_payroll.designation)
                )
            if self_payroll.start_date:
                error_msg += "<br>" + _("Start date: {0}").format(
                    frappe.bold(self_payroll.start_date)
                )
            if self_payroll.end_date:
                error_msg += "<br>" + _("End date: {0}").format(
                    frappe.bold(self_payroll.end_date)
                )
            frappe.throw(error_msg, title=("No employees found"))

        for d in employees:
            self_payroll.append("employees", d)

        self_payroll.number_of_employees = len(self_payroll.employees)
        if self_payroll.validate_attendance:
            return self.validate_employee_attendance(self_payroll)
        self_payroll.save(ignore_permissions=True)

    def on_submit(self):
        counter = 0
        for branch in self.branches():
            if branch:
                new_payroll = frappe.get_doc(self.new_payroll_entry())
                new_payroll.branch = branch.custom_branch
                new_payroll.territory = branch.custom_territory
                new_payroll.insert(ignore_permissions=True)
                self.fill_employee_details(new_payroll.name)
                counter += 1
        if counter > 1:
            frappe.msgprint(
                "{} Payroll Entries have been created successfully  ".format(counter)
            )
        else:
            frappe.msgprint(
                "{} Payroll Entry has been created successfully".format(counter)
            )

    def branches(self):
        return frappe.get_all(
            "Salary Structure Assignment",
            filters={
                "docstatus": ["=", 1],
            },
            fields=["distinct custom_branch", "custom_territory"],
        )

    def new_payroll_entry(self):
        return {
            "doctype": "Payroll Entry",
            "payroll_date": self.posting_date,
            "company": self.company,
            "currency": self.currency,
            "exchange_rate": self.exchange_rate,
            "payroll_payable_account": self.payroll_payable_account,
            "payroll_frequency": self.payroll_frequency,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "deduct_tax_for_unclaimed_employee_benefits": self.deduct_tax_for_unclaimed_employee_benefits,
            "deduct_tax_for_unsubmitted_tax_exemption_proof": self.deduct_tax_for_unsubmitted_tax_exemption_proof,
            "project": self.project,
            "cost_center": self.cost_center,
            "payment_account": self.payment_account,
            "bank_account": self.bank_account,
            "grouped_payroll_entry": self.name,
        }

    # def on_cancel(self):
    #     frappe.delete_doc("Payroll Entry", {"grouped_payroll_entry": self.name})
