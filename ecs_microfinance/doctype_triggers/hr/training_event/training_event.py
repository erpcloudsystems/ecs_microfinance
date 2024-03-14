from __future__ import unicode_literals
import frappe
from frappe import _
import random
import json


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    pass
@frappe.whitelist()
def onload(doc, method=None):
	pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass
@frappe.whitelist()
def validate(doc, method=None):
        # emps = frappe.db.sql(""" select a.employee, a.designation,a.training_fielded,b.name,b.posting_date
        #                                                         from `tabTraining Budget Table` a join `tabTraining Budget` b
        #                                                         on a.parent = b.name
        #                                                         where a.training_fielded = '{field}'
        #                                                         and b.posting_date >='{from1}'
        #                                                         and b.posting_date <='{to}'
        #                                                         and b.docstatus = 1
        #
        #                                                     """.format(field=doc.training_field,from1=doc.from_date,to=doc.to_date), as_dict=1)
        # if emps:
        #     doc.employees =[]
        #     for y in emps:
        #         items = doc.append("employees", {})
        #         items.employee = y.employee
        #         items.designation = y.designation
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    pass
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass


@frappe.whitelist()
def get_employee(doc,training_field,from_date,to_date, method=None):

    emps = frappe.db.sql(""" select a.employee, a.employee_name, a.designation,a.training_fielded,b.name,b.posting_date
                                                               from `tabTraining Budget Table` a join `tabTraining Budget` b
                                                               on a.parent = b.name
                                                               where a.training_fielded = '{field}'
                                                               and b.posting_date >='{from1}'
                                                               and b.posting_date <='{to}'
                                                               and b.docstatus = 1

                                                           """.format(field=training_field, from1=from_date,
                                                                      to=to_date), as_dict=1)
    if emps:
        # event = frappe.get_doc('Training Event', doc)
        # event.employees = []
        #
        # for y in emps:
        #     items = event.append("employees", {})
        #     items.employee = y.employee
        #     items.employee_name = y.employee_name
        #     items.designation = y.designation
        return emps

    else:
        frappe.throw("لا يوجد موظفين في هذه الفترة")

@frappe.whitelist()
def get_random_questions(custom_training_event):
    # Fetch random questions from the LMS Question doctype based on the training event name
    questions = frappe.db.sql('''
        SELECT name, question, type, option_1, option_2, option_3, option_4
        FROM `tabLMS Question` 
        WHERE custom_training_event = %s
        ORDER BY RAND() 
        LIMIT 10
    ''', custom_training_event, as_dict=True)
    return questions



@frappe.whitelist()
def process_assessment_results(assessment_data):
    try:
        assessment_data = json.loads(assessment_data)

        assessment_results = []
        assessment_result = frappe.get_doc({
                    'doctype': 'Assessment Results',
                    'training_event': assessment_data['training_event'],
                    'submitting_datetime': frappe.utils.now_datetime(),
                    'user': frappe.session.user,
                   
                })
        assessment_result.assessment_results_schedule = []

        for item in assessment_data['assessment_results']:
                question_id = item['name']
                trainee_answer = item['trainee_answer']
                question_type = item['question_type']

                # Construct assessment result object
                result = ""
                if get_correct_answers(question_id, trainee_answer, question_type) and question_type != "User Input":
                    result = "Correct"
                elif  get_correct_answers(question_id, trainee_answer, question_type) == 0 and question_type != "User Input":
                    result = "False"

                correct_answers = ""

                # Retrieve values of option_1 to option_4 and is_correct_1 to is_correct_4
                for i in range(1, 5):
                    option = frappe.db.get_value("LMS Question", question_id, "option_" + str(i))
                    is_correct = frappe.db.get_value("LMS Question", question_id, "is_correct_" + str(i))
                    
                    # Check if is_correct is set to 1
                    if is_correct == 1:
                        correct_answers = option
                assessment_result.append('assessment_results_schedule',{
                    'question': question_id,
                    'trainee_answer': trainee_answer,
                    'result': result,# You can set a default result if needed,
                     'correct_answer': correct_answers
                }) 

        assessment_result.insert(ignore_permissions=True)
        # frappe.msgprint(f"{assessment_result.name}")


        assessment_results.append(assessment_result)

        return "Assessment results saved successfully"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Assessment Results Saving Error"))
        return "Error saving assessment results: {}".format(str(e))



def get_correct_answers(question_id, answer , question_type = "Choices"):
    if question_type == "Choices":
        correct_answers = frappe.db.get_value("LMS Question", question_id,
                                            ["is_correct_1", "is_correct_2", "is_correct_3", "is_correct_4", "option_1", "option_2", "option_3", "option_4"])
        key = {}
        
        key[correct_answers[4]] = correct_answers[0]
        key[correct_answers[5]] = correct_answers[1]
        key[correct_answers[6]] = correct_answers[2]
        key[correct_answers[7]] = correct_answers[3]
        
        return key[answer]
    else:
        return 0

def save_assessment_results(assessment_results):
    for result in assessment_results:
        assessment_result = frappe.new_doc("Assessment Results")
        assessment_result.update(result)
        assessment_result.insert()
