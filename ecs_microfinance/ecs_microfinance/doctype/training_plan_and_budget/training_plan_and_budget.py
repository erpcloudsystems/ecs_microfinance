# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TrainingPlanAndBudget(Document):
    @frappe.whitelist()
    def get_employee(doc, method=None):
        selected_employee = {}
        # doc.training_need_table = []
        # doc.training_budget_table = []

        # Construct the base SQL query
        sql_query = """
            SELECT 
                `tabEmployee`.name as name, 
                `tabEmployee`.employee_name as employee_name, 
                `tabEmployee`.department as department,
                `tabEmployee`.designation as designation, 
                `tabEmployee`.territory as territory, 
                `tabEmployee`.branch
            FROM 
                `tabEmployee`
            WHERE 
                `tabEmployee`.status = "Active"
        """

        # Add conditions for department and branch if they are selected
        if doc.department:
            sql_query += " AND `tabEmployee`.department = '{department}'".format(department=doc.department)
        if doc.branch:
            sql_query += " AND `tabEmployee`.branch = '{branch}'".format(branch=doc.branch)

        # Fetch the governorate from the branch
        if doc.governorate:
            branches = frappe.get_all('Branch', filters={'custom_governorate': doc.governorate}, fields=['name'])
            branch_names = [branch.name for branch in branches]
            if branch_names:
                sql_query += " AND `tabEmployee`.branch IN ({})".format(', '.join(["'{}'".format(branch) for branch in branch_names]))
            else:
                # If no branches found for the selected governorate, return empty result
                return

        selected_employee = frappe.db.sql(sql_query, as_dict=1)

        for i in selected_employee:
            doc.append("training_need_table", {
                "employee": i.name,
                "employee_name": i.employee_name,
                "department": i.department,
                "designation": i.designation,
                "territory": i.territory,
            })
            doc.append("training_budget_table", {
                "employee": i.name,
                "employee_name": i.employee_name,
                "department": i.department,
                "designation": i.designation,
                "territory": i.territory,
            })


    @frappe.whitelist()
    def on_submit(self, method=None):
        for row in self.preparation_table :
            new_doc = frappe.get_doc({
                "doctype": "Task",
                "custom_training_plan_and_budget":self.name,
                "department": row.department,
                "company": "Finbi Microfinance",
                "description": row.description,
                "subject": "Preparation For:" + self.name
            
            })
            new_doc.insert(ignore_permissions=True)
 
    @frappe.whitelist()
    def validate(doc, method=None):
        table_length = len(doc.training_budget_table)

        # Set the trainer_fees for each row in the child table
        for x in doc.training_budget_table:
            x.trainer_fees = doc.trainer_fees / table_length
            x.test_fees = doc.test_fees / table_length
            x.administrative_fees = doc.administrative_fees / table_length
            x.training_material_fees = doc.training_material_fees / table_length
            x.training_tools_fees = doc.training_tools_fees / table_length
            x.transportation_fees = doc.transportation_fees / table_length
            x.housing_fees = doc.housing_fees / table_length
            x.examcertificate_fees = doc.exam_certificate_fees / table_length
            x.others = doc.others / table_length
    # @frappe.whitelist()
    # def delete_budget_rows(employee):
    #     frappe.db.delete('Training Budget Table', {'employee': employee}, ignore_permissions=True)