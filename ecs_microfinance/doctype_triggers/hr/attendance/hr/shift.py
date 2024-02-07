from datetime import datetime, timedelta

import frappe

from .attendance_policy.late_arrival_policy import LateArrivalPolicyFactory
from .attendance_policy.early_leave_policy import EarlyLeavePolicyFactory
from .attendance_policy.absent_policy import AbsentPolicyFactory
from .attendance_policy.missing_fingerprint_policy import MissingFingerprintPolicyFactory
from .constans import AppliedAttendancePolicy, DATE_FORMAT
from .factory  import Factory, DAO
from .helpers  import get_dates_different_in_minutes


class ShiftService:
    @staticmethod
    def apply_late_arrival_policy(attendance):
        shift = attendance.get_shift()
        if not shift.is_late_arrival_policy_enabled():
            return
        
        if not attendance.is_late():
            return
        if  attendance.is_missed_fingerprint():
            return
        ShiftService._apply_policy(attendance, shift.get_late_arrival_policy())

    @staticmethod
    def apply_early_leave_policy(attendance):
        shift = attendance.get_shift()
        if not shift.is_early_leave_policy_enabled():
            return
        if not attendance.is_early():
            return

        if not attendance.get_checkout():
            frappe.msgprint(
                f"{attendance.get_employee().get_id()} does not have checkout time on date {attendance.get_date()}")
            return
        if  attendance.is_missed_fingerprint():
            return
        ShiftService._apply_policy(attendance, shift.get_early_leave_policy())

    @staticmethod
    def apply_missing_fingerprint_policy(attendance):
        shift = attendance.get_shift()
        if not shift.is_missing_fingerprint_policy_enabled():
            return
        if not attendance.is_missed_fingerprint():
            return
        
        ShiftService._apply_policy(attendance, shift.get_missing_fingerprint_policy())

    @staticmethod
    def apply_absent_policy(attendance):
        shift = attendance.get_shift()
        if not shift.is_absent_policy_enabled():
            return
        if not attendance.is_absent():
            return
        
        ShiftService._apply_policy(attendance, shift.get_absent_policy())

    @staticmethod
    def apply_overtime_policy(attendance):
        shift = attendance.get_shift()
        if not shift.is_overtime_policy_enabled():
            return

        if not attendance.get_checkout():
            frappe.msgprint(
                f"{attendance.get_employee().get_id()} does not have checkout time on date {attendance.get_date()}")
            return

        if ShiftService.get_overtime_amount(attendance) <= 0:
            return

        new_doc = frappe.get_doc({
            "doctype": "Extra Salary",
            "employee": attendance.get_employee().get_id(),
            "shift": shift.get_name(),
            "payroll_date": attendance.get_date(),
            "applied_policy": AppliedAttendancePolicy.OVERTIME,
            "amount": ShiftService.get_overtime_amount(attendance),
            "salary_component": shift.get_overtime_salary_component(),
            "attendance": attendance.get_name(),
            'minutes_of_late_early_overtime': ShiftService.get_overtime_amount(attendance),
            'company': frappe.get_value('Employee', {'name': attendance.get_employee().get_id()}, 'company')
        })
        new_doc.insert()

    @staticmethod
    def _apply_policy(attendance, policy):
        shift = attendance.get_shift()

        amounts, salary_components, policy_rows, minutes = policy.apply(attendance)

        for amount, salary_component, policy_row, minutes in zip(amounts, salary_components, policy_rows, minutes):
            new_doc = frappe.get_doc({
                "doctype": "Extra Salary",
                "employee": attendance.get_employee().get_id(),
                "shift": shift.get_name(),
                "payroll_date": attendance.get_date(),
                "amount": amount,
                "salary_component": salary_component,
                "applied_policy": policy.get_name(),
                "policy_row": policy_row,
                "attendance": attendance.get_name(),
                'minutes_of_late_early_overtime': minutes,
                'company': frappe.get_value('Employee', {'name': attendance.get_employee().get_id()}, 'company')
            })
            new_doc.insert(new_doc)

    @staticmethod
    def get_overtime_amount(attendance) -> float:
        shift = attendance.get_shift()
        overtime_in_minutes = get_dates_different_in_minutes(
            datetime.strptime(attendance.get_checkout(), DATE_FORMAT),
            shift.get_shift_end_date(attendance.get_date()))
        if overtime_in_minutes - shift.get_overtime_starts_after() > 0:
            return overtime_in_minutes
        return 0

    # @staticmethod
    # def get_absent_salary_component(attendance):
    #     return attendance.get_shift().get_absent_policy().get_salary_component()

    # @staticmethod
    # def get_absent_amount(attendance):
    #     shift = attendance.get_shift()
    #     return shift.get_absent_policy().get_amount(attendance)


class _Shift:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

    def get_name(self):
        return self._name

    def get_month_start_day(self):
        return self._month_start_day

    def get_month_end_day(self):
        return self._month_end_day

    def get_late_arrival_policy(self):
        return self._late_arrival_policy

    def get_early_leave_policy(self):
        return self._early_leave_policy

    def get_absent_policy(self):
        return self._absent_policy

    def get_overtime_salary_component(self):
        return self._overtime_salary_component

    def get_overtime_starts_after(self):
        return self._overtime_starts_after

    def get_missing_fingerprint_policy(self):
        return self._missing_fingerprint_policy

    def get_shift_start_date(self, date: str) -> datetime:
        return datetime.strptime(f"{date} {self._start_time}", '%Y-%m-%d %H:%M:%S')

    def get_shift_end_date(self, date: str) -> datetime:
        return self.get_shift_start_date(date) + timedelta(
            hours=self.get_length())

    def get_length(self):
        start = self._start_time
        end = self._end_time
        if end >= start:
            return (end - start).total_seconds() / 3600
        return 24 - (start - end).total_seconds() / 3600

    def get_arrival_minutes_after_grace_period(self, attendance):
        shift_start_date: datetime = self.get_shift_start_date(attendance.get_date())
        checkin_date: datetime = datetime.strptime(attendance.get_checkin(), '%Y-%m-%d %H:%M:%S')
        minutes_after_shift_start_time: float = get_dates_different_in_minutes(checkin_date, shift_start_date)
        minutes_after_grace_period: float = minutes_after_shift_start_time - (
            self._late_entry_grace_period if self._enable_entry_grace_period else 0)
        return minutes_after_grace_period

    def get_leave_minutes_before_grace_period(self, attendance):
        minutes_before_shift_end = get_dates_different_in_minutes(self.get_shift_end_date(attendance.get_date()),
                                                                  datetime.strptime(attendance.get_checkout(),
                                                                                    DATE_FORMAT))
        minutes_before_grace_period: float = minutes_before_shift_end - (
            self._early_exit_grace_period if self._enable_exit_grace_period else 0)
        return minutes_before_grace_period

    def get_shift_start_date(self, date: str) -> datetime:
        return datetime.strptime(f"{date} {self._start_time}", '%Y-%m-%d %H:%M:%S')

    def get_shift_end_date(self, date: str) -> datetime:
        return self.get_shift_start_date(date) + timedelta(
            hours=self.get_length())

    def is_late_arrival_policy_enabled(self):
        return self._enable_late_arrival_policy

    def is_early_leave_policy_enabled(self):
        return self._enable_early_leave_policy

    def is_absent_policy_enabled(self):
        return self._enable_absent_policy

    def is_overtime_policy_enabled(self):
        return self._enable_overtime_policy

    def is_missing_fingerprint_policy_enabled(self):
        return self._enable_missing_fingerprint_policy


class _ShiftDao(DAO):
    @staticmethod
    def create(name: str) -> _Shift:
        shift_dict = {'_late_arrival_policy': LateArrivalPolicyFactory.create(name),
                      '_early_leave_policy': EarlyLeavePolicyFactory.create(name),
                      '_absent_policy': AbsentPolicyFactory.create(name),
                      '_missing_fingerprint_policy': MissingFingerprintPolicyFactory.create(name)}
        for key, value in _ShiftDao._get_shift_properties_from_db(name).items():
            shift_dict[f"_{key}"] = value

        return _Shift(shift_dict)

    @staticmethod
    def _get_shift_properties_from_db(shift_name):
        return frappe.db.sql(f"""
                                SELECT
                                    name,
                                    start_time,
                                    end_time, 
                                    month_start_in AS month_start_day,
                                    month_end_in AS month_end_day,
                                    enable_entry_grace_period, 
                                    late_entry_grace_period,
                                    enable_exit_grace_period,   
                                    early_exit_grace_period,
                                    last_sync_of_checkin,
                                    overtime_starts_after,
                                    overtime AS overtime_salary_component,
                                    enable_early_leave_policy,
                                    enable_late_arrival_policy,
                                    enable_absent_policy,
                                    enable_overtime_policy,
                                    enable_missing_fingerprint_policy
                                FROM `tabShift Type`
                                WHERE name = '{shift_name}'
                            """, as_dict=1)[0]


class ShiftFactory(Factory):
    _store = {}
    _shiftDao = _ShiftDao()

    @staticmethod
    def create(shift_name: str):
        if shift_name in ShiftFactory._store:
            return ShiftFactory._store[shift_name]
        else:
            ShiftFactory._store[shift_name] = ShiftFactory._shiftDao.create(shift_name)
            return ShiftFactory._store[shift_name]
