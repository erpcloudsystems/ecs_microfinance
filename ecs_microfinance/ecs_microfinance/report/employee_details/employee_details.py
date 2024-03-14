# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns=get_columns(filters)
    data=get_data(filters)
    return columns, data

def get_columns(filters):
    return[
        {
            "fieldname": "name",
            "label": "Name",
            "fieldtype":"Link",
            "options":"Employee"
        }
        ,
        {
            "fieldname":"employee_name",
			"label":"اسم الموظف",
			"fieldtype":"Data",

        },
        {
            "fieldname":"designation",
            "label":"الوظيفة",
            "fieldtype":"Link",
            "options":"Designation"
        },
        {
            "fieldname":"department",
            "label":"الادارة",
            "fieldtype":"Link",
            "options":"Department"
        },
        {
            "fieldname":"branch",
            "label":"الفرع",
            "fieldtype":"Link",
            "options":"Branch"
        },



        {
            "fieldname":"custom_birth_certificate1",
            "label":"شهادة الميلاد",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_medical_certificate1",
            "label":"نموذج 111",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_end_of_service_certificate_from_pw1",
            "label":"شهادة نهاية الخدمة بالعمل السابق",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_original_academic_certificate1",
            "label":"اصل الشهادة العلمية",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_military_certificate1",
            "label":"الشهادة العسكرية",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_print_insurance_status1",
            "label":"الموقف التأميني",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_workheal1",
            "label":"كعب العمل",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_criminal_status_certificate1",
            "label":"الحالة الجنائية",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_previous_work_income_document1",
            "label":"اثبات الدخل السابق",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_original_experience_certificates1",
            "label":"اصل شهادة الخبرة",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_national_id_card1",
            "label":"الرقم القومي",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_work_permit_for_foreigner1",
            "label":"الترخيص بالعمل إن كان الطالب من الأجانب",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_6_personal_photos1",
            "label":"عدد 6 صور شخصية فوتوغرافية",
            "fieldtype":"Data",
        },
        {
            "fieldname":"custom_social_status_endorsement1",
            "label":"إقرار موقع عليه من العامل يبين فيه حالته الاجتماعية",
            "fieldtype":"Data",
        },

    ]

def get_data(filters):
    name=filters.get('name')
    conditions = ""
    if name:
        conditions += f"AND name = '{name}'"
    designation=filters.get('designation')
    if filters.get('designation'):
        conditions += f"AND designation = '{designation}'"
    department=filters.get('department')
    if filters.get('department'):
        conditions += f"AND department = '{department}'"
    branch=filters.get('branch')
    if filters.get('branch'):
        conditions += f"AND branch = '{branch}'"
    data = frappe.db.sql(f""" 
                    select name, employee_name, designation, department ,
                        branch as branch,custom_birth_certificate1 ,
                        custom_original_academic_certificate1 ,
                        custom_medical_certificate1 ,
                            custom_end_of_service_certificate_from_pw1 ,
                            custom_military_certificate1 ,
                            custom_print_insurance_status1 ,
                        custom_workheal1 ,
                            custom_criminal_status_certificate1 ,
                        custom_previous_work_income_document1 ,
                            custom_original_experience_certificates1 ,
                        custom_national_id_card1 ,
                            custom_work_permit_for_foreigner1 ,
                        custom_6_personal_photos1 ,
                            custom_social_status_endorsement1 
                    from `tabEmployee` 
                    where 
                        1=1
                        {conditions}     """,as_dict = 1)
    if data :
        return data
