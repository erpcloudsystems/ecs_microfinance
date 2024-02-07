from abc import ABC, abstractmethod
from .factory import Factory

from .constans import AppliedAttendancePolicy

import frappe


class _AttendancePolicy(ABC):
    @abstractmethod
    def get_amount(self, attendance) -> float:
        pass  # todo

    def get_salary_component(self, attendance) -> str:
        pass  # todo


class _LateEarlyPolicy(_AttendancePolicy):
    def get_amount(self, attendance, minutes_after_grace_period: float) -> float:
        policy_row = self.get_policy_row(minutes_after_grace_period)
        times_being_late = self._get_times_of_violating_policy(attendance, policy_row)
        self._recorder[(attendance.get_employee().get_id(), attendance.get_payroll_start_date(), policy_row)] += 1

        return self._policies[policy_row][
            f"{self._PREFIX_PENALTY_COLUMN_NAME}_{min(times_being_late, self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS - 1)}"]

    def get_salary_component(self, minutes_after_grace_period: float) -> str:
        policy_row = self.get_policy_row(minutes_after_grace_period)
        return self._policies[policy_row]['salary_component']

    def get_policy_row(self, minutes_after_grace_period: float) -> int:
        for policy in self._policies:
            if policy['from'] < minutes_after_grace_period <= policy['to']:
                return policy.policy_row
        return len(self._policies) - 1

    @abstractmethod
    def _get_times_of_violating_policy(self, attendance, policy_row: int) -> int:
        pass


class _LateArrivalPolicy(_LateEarlyPolicy):
    def __init__(self, shift_name: str):
        self._PREFIX_PENALTY_COLUMN_NAME: str = "no_of_late_arrival"
        self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS: int = 5
        self._shift_name: str = shift_name

        self._policies = frappe.db.sql(f"""
            SELECT from_after_grace_period AS `from`,
                    to_after_grace_period AS `to`,
                    /*
                     this following expression will generate:
                        no_of_late_arrival_0,
                        no_of_late_arrival_1,
                        no_of_late_arrival_2,
                        no_of_late_arrival_3,
                        no_of_late_arrival_4,
                     */
                    {''.join(f"{self._PREFIX_PENALTY_COLUMN_NAME}_{i}, "
                             for i in range(self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS))}
                   salary_component,
                   CAST((@row_number:=@row_number+1) AS UNSIGNED) AS policy_row           
            FROM 

                `tabLate Table`, (SELECT @row_number:=-1) AS r
            WHERE 
                `tabLate Table`.parent = '{shift_name}'
            ORDER BY
                `from`, `to`
        """, as_dict=1)
        self._recorder = {}

    def _get_times_of_violating_policy(self, attendance, policy_row: int) -> int:
        key = (attendance.get_employee().get_id(), attendance.get_payroll_start_date(), policy_row)
        if key not in self._recorder:
            self._recorder[key] = frappe.db.sql(
                f"""
                    SELECT COUNT(*)
                    FROM `tabExtra Salary` e 
                    WHERE 
                        e.employee = '{attendance.get_employee().get_id()}'
                        AND e.payroll_date between '{attendance.get_payroll_start_date()}' and '{attendance.get_date()}'
                        AND e.shift = '{attendance.get_shift().get_name()}'
                        AND e.applied_policy = '{AppliedAttendancePolicy.LATE}'
                        AND e.policy_row = {policy_row}
                """
            )[0][0]

        return self._recorder[key]


class _EarlyLeavePolicy(_LateEarlyPolicy):
    def __init__(self, shift_name: str):
        self._PREFIX_PENALTY_COLUMN_NAME: str = "no_of_early_leave"
        self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS: int = 5
        self._shift_name: str = shift_name
        self._policies = frappe.db.sql(f"""
                   SELECT 0 AS `from`,
                           1 AS `to`,
                           /*
                            this following expression will generate:
                               no_of_early_leave_0,
                               no_of_early_leave_1,
                               no_of_early_leave_2,
                               no_of_early_leave_3,
                               no_of_early_leave_4,
                            */
                           {''.join(f"{self._PREFIX_PENALTY_COLUMN_NAME}_{i}, "
                                    for i in range(self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS))}
                          salary_component,
                          CAST((@row_number:=@row_number+1) AS UNSIGNED) AS policy_row           
                   FROM 
                       `tabEarly Leave Table`, (SELECT @row_number:=-1) AS r
                   WHERE 
                       `tabEarly Leave Table`.parent = '{shift_name}'
                   ORDER BY
                       `from`, `to`
               """, as_dict=1)
        self._recorder = {}

    def _get_times_of_violating_policy(self, attendance, policy_row: int) -> int:
        key = (attendance.get_employee().get_id(), attendance.get_payroll_start_date(), policy_row)
        if key not in self._recorder:
            self._recorder[key] = frappe.db.sql(
                f"""
                    SELECT COUNT(*)
                    FROM `tabExtra Salary` e 
                    WHERE 
                        e.employee = '{attendance.get_employee().get_id()}'
                        AND e.payroll_date between '{attendance.get_payroll_start_date()}' and '{attendance.get_date()}'
                        AND e.shift = '{attendance.get_shift().get_name()}'
                        AND e.applied_policy = '{AppliedAttendancePolicy.EARLY}'
                        AND e.policy_row = {policy_row}
                """
            )[0][0]

        return self._recorder[key]


class _AbsentPolicy(_AttendancePolicy):
    def __init__(self, shift_name):
        self._PREFIX_PENALTY_COLUMN_NAME: str = "no_of_absent"
        self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS: int = 5
        self._shift_name: str = shift_name
        self._policies = frappe.db.sql(f"""
                           SELECT 
                                   /*
                                    this following expression will generate:
                                       no_of_early_leave_0,
                                       no_of_early_leave_1,
                                       no_of_early_leave_2,
                                       no_of_early_leave_3,
                                       no_of_early_leave_4,
                                    */
                                   {''.join(f"{self._PREFIX_PENALTY_COLUMN_NAME}_{i}, "
                                            for i in range(self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS))}
                                  salary_component
                           FROM 
                               `tabAbsent Table`
                           WHERE 
                               `tabAbsent Table`.parent = '{shift_name}'
                       """, as_dict=1)
        self._recorder = {}

    def get_amount(self, attendance) -> list[float]:
        times_being_absent = self._get_times_of_being_absent(attendance)
        self._recorder[(attendance.get_employee().get_id(), attendance.get_payroll_start_date())] += 1

        return [self._policies[i][
                    f"{self._PREFIX_PENALTY_COLUMN_NAME}_{min(times_being_absent, self._MAXIMUM_NUMBER_OF_POLICY_COLUMNS - 1)}"]
                for i in range(len(self._policies))]

    def get_salary_component(self) -> list[str]:
        return [row.salary_component for row in self._policies]

    def _get_times_of_being_absent(self, attendance):
        key = (attendance.get_employee().get_id(), attendance.get_payroll_start_date())
        if key not in self._recorder:
            self._recorder[key] = frappe.db.sql(f"""
                SELECT COUNT(*)
                FROM `tabExtra Salary` AS e 
                WHERE  e.employee = '{attendance.get_employee().get_id()}'
                        AND e.payroll_date between '{attendance.get_payroll_start_date()}' and '{attendance.get_date()}'
                        AND e.shift = '{attendance.get_shift().get_name()}'
                        AND e.applied_policy = '{AppliedAttendancePolicy.ABSENT}'
                        AND e.policy_row = 0
            """)[0][0]

        return self._recorder[key]


##############################################################

class LateArrivalPolicyFactory(Factory):
    _store = {}

    @staticmethod
    def create(shift_name: str):
        if shift_name in LateArrivalPolicyFactory._store:
            return LateArrivalPolicyFactory._store[shift_name]
        else:
            LateArrivalPolicyFactory._store[shift_name] = _LateArrivalPolicy(shift_name)
            return LateArrivalPolicyFactory._store[shift_name]


class EarlyLeavePolicyFactory(Factory):
    _store = {}

    @staticmethod
    def create(shift_name: str):
        if shift_name in EarlyLeavePolicyFactory._store:
            return EarlyLeavePolicyFactory._store[shift_name]
        else:
            EarlyLeavePolicyFactory._store[shift_name] = _EarlyLeavePolicy(shift_name)
            return EarlyLeavePolicyFactory._store[shift_name]


class AbsentPolicyFactory(Factory):
    _store = {}

    @staticmethod
    def create(shift_name: str):
        if shift_name in AbsentPolicyFactory._store:
            return AbsentPolicyFactory._store[shift_name]
        else:
            AbsentPolicyFactory._store[shift_name] = _AbsentPolicy(shift_name)
            return AbsentPolicyFactory._store[shift_name]


[{'from': 0, 'to': 15, 'no_of_late_arrival_0': 0.25, 'no_of_late_arrival_1': 0.5, 'no_of_late_arrival_2': 0.75,
  'no_of_late_arrival_3': 1.0, 'no_of_late_arrival_4': 1.0, 'salary_component': 'عدد التاخيرات قبل الساعة 12',
  'policy_row': 1.0},
 {'from': 15, 'to': 30, 'no_of_late_arrival_0': 0.5, 'no_of_late_arrival_1': 0.75, 'no_of_late_arrival_2': 1.0,
  'no_of_late_arrival_3': 1.0, 'no_of_late_arrival_4': 1.0, 'salary_component': 'عدد التاخيرات قبل الساعة 12',
  'policy_row': 2.0}]

