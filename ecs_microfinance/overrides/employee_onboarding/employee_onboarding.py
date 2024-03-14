import frappe 
from hrms.controllers.employee_boarding_controller import EmployeeBoardingController
from frappe.utils import unique
class CustomEmployeeBoardingController(EmployeeBoardingController):
    def create_task_and_notify_user(self):
        # create the task for the given project and assign to the concerned person
        holiday_list = self.get_holiday_list()

        for activity in self.activities:
            if activity.task:
                continue

            dates = self.get_task_dates(activity, holiday_list)

            task = frappe.get_doc(
                {
                    "doctype": "Task",
                    "project": self.project,
                    "subject": activity.activity_name + " : " + self.employee_name,
                    "description": activity.description,
                    "department": self.department,
                    "company": self.company,
                    "task_weight": activity.task_weight,
                    "exp_start_date": dates[0],
                    "exp_end_date": dates[1],
                    "is_group":1
                }
            ).insert(ignore_permissions=True)
            activity.db_set("task", task.name)

            # fetch tasks for onboarding_task
            onboarding_task = frappe.db.get_all("Employee Boarding Tasks",{"parent":activity.onboarding_task},["*"])
            #create fetch task for each onboarding_task
            if onboarding_task:
                for row in onboarding_task:
                    onboarding_task = frappe.get_doc(
                            {
                                "doctype": "Task",
                                "project": self.project,
                                "subject": row.activity_name + " : " + self.employee_name,
                                "description": row.description,
                                "department": self.department,
                                "company": self.company,
                                "task_weight": row.task_weight,
                                "exp_start_date": dates[0],
                                "exp_end_date": dates[1],
                                "parent_task":task.name
                            }
                        ).insert(ignore_permissions=True)

            users = [activity.user] if activity.user else []
            if activity.role:
                user_list = frappe.db.sql_list(
                    """
                    SELECT
                        DISTINCT(has_role.parent)
                    FROM
                        `tabHas Role` has_role
                            LEFT JOIN `tabUser` user
                                ON has_role.parent = user.name
                    WHERE
                        has_role.parenttype = 'User'
                            AND user.enabled = 1
                            AND has_role.role = %s
                """,
                    activity.role,
                )
                users = unique(users + user_list)

                if "Administrator" in users:
                    users.remove("Administrator")

            # assign the task the users
            if users:
                self.assign_task_to_users(task, users)
