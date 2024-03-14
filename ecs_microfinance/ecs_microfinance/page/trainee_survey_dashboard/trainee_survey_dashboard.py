import frappe
import json
from datetime import datetime

@frappe.whitelist()
def get_employee(userId, role):
	if  role == "true":
		query = f"""
					Select * from `tabUser` where name = '{userId}'
				"""
		data =  frappe.db.sql(query, as_dict = 1)
		
		# from frappe.utils import get_roles
		# user_roles = get_roles(frappe.session.user)
		# frappe.msgprint(user_roles)
		return data
	else:
		query = f"""
				Select * from `tabEmployee` where user_id = '{userId}'
			"""
		data =  frappe.db.sql(query, as_dict = 1)
		
		if not data:
			frappe.throw("You are not Employee please link ur account to employee")
		# from frappe.utils import get_roles
		# user_roles = get_roles(frappe.session.user)
		# frappe.msgprint(user_roles)
		return data
	pass

@frappe.whitelist()
def get_trainnig_event_for_employee(employee, role):
	frappe.msgprint(f"{employee} :: {role}")
	if role == "true" :
		query = f"""
				Select  TE.parent as training_events  from `tabTraining Event Employee` TE where  docstatus = 1 group by training_events
			"""
		return frappe.db.sql(query, as_dict = 1)
		
	else:
		query = f"""
				Select  TE.parent as training_events  from `tabTraining Event Employee` TE where employee = '{employee}' and docstatus = 1 group by training_events
			"""
		return frappe.db.sql(query, as_dict = 1)

@frappe.whitelist()
def get_completed_trainnig_event_for_employee(employee, role):
	if  role == "true": 
		query = f"""
				Select Count(name) num_of_events from `tabTraining Event` TE where event_status = 'Completed' and docstatus = 1
			"""
		return frappe.db.sql(query, as_dict = 1)
		
	else:
		query = f"""
				Select Count(TE.parent) num_of_events from `tabTraining Event Employee` TE where employee = '{employee}' and status = 'Completed' and docstatus = 1
			"""
		return frappe.db.sql(query, as_dict = 1)
		

@frappe.whitelist()
def get_total_hours_trainnig_event_for_employee(employee, role):
	training_events = None
	if  role == "true": 
		query = f"""
				Select SUM(total_hour) total_hour from `tabTraining Event` TE where docstatus = 1
			"""
		
		return frappe.db.sql(query, as_dict = 1)
	else:
		query = f"""
				Select TE.parent training_events from `tabTraining Event Employee` TE where employee = '{employee}' and docstatus = 1
			"""
		
		training_events =  frappe.db.sql(query, as_dict = 1)
		conditions = []
		for training in training_events:
			conditions.append(f"name = '{training['training_events']}'")
		filters = ""
		
		query = f"""
				Select SUM(total_hour) total_hour from `tabTraining Event` TE where docstatus = 1 
			"""
		if conditions:
			query += " AND (" + " OR ".join(conditions) + ")"
		total_hour =  frappe.db.sql(query, as_dict = 1)
		return total_hour


@frappe.whitelist()
def get_total_hours_completed_trainnig_event_for_employee(employee, role):
	training_events = None
	if  role == "true": 
		query = f"""
				Select  SUM(total_hour) total_hour from `tabTraining Event` TE where  event_status = 'Completed' and docstatus = 1 
			"""
		
		training_events =  frappe.db.sql(query, as_dict = 1)
		return  training_events
	else:
		query = f"""
			Select TE.parent training_events from `tabTraining Event Employee` TE where employee = '{employee}' and status = 'Completed' and docstatus = 1 
		"""
	
		training_events =  frappe.db.sql(query, as_dict = 1)
		conditions = []
		for training in training_events:
			conditions.append(f"name = '{training['training_events']}'")
		filters = ""
		
		query = f"""
				Select SUM(total_hour) total_hour from `tabTraining Event` TE where docstatus = 1 
			"""
		if conditions:
			query += " AND (" + " OR ".join(conditions) + ")"
		total_hour =  frappe.db.sql(query, as_dict = 1)
		return total_hour

@frappe.whitelist()
def get_feedback_survey_data(filters):
	conditions = ""

	if filters != "":
		conditions += f" and `tabTrainee Survey`.training_event ='{filters}'"
	grades = [ "ممتاز", "جيد جدا", "جيد", "متوسط", "ضعيف"]
	questions =  ['question_1','question_2','question_3','question_4','question_5','question_6','question_7','question_8','question_9','question_10','question_11','question_12','question_13']
	def get_question_count(grade, question_no):
		return frappe.db.sql( f"""
						select 
							count(name) as count 
							from
								`tabTrainee Survey`
							where
									1=1		   
								{conditions}
							  and `tabTrainee Survey`.{question_no}  = '{grade}'

						""", as_dict = 1)[0]['count']
	result = []
	for question in questions:
		data = {
			'excellent': get_question_count("ممتاز", question),
			'very_good': get_question_count("جيد جدا", question),
			'good': get_question_count("جيد", question),
			'intermediate': get_question_count("متوسط", question),
			'bad': get_question_count("ضعيف", question),
		}
		result.append(data)

	return result

@frappe.whitelist()
def get_assements_for_employee(employee, training_events, role):
	if  role == "true": 
		query = f"""
			SELECT 
				TRE.* 
			FROM 
				`tabTraining Result` TR
			JOIN
				`tabTraining Result Employee`  TRE
			ON 
				TR.name =  TRE.parent
			where  TR.training_event = '{training_events}'
		"""
		return frappe.db.sql(query , as_dict = 1)
	else:
		query = f"""
			SELECT 
				TRE.* 
			FROM 
				`tabTraining Result` TR
			JOIN
				`tabTraining Result Employee`  TRE
			ON 
				TR.name =  TRE.parent
			where  TRE.employee = '{employee}' and TR.training_event = '{training_events}'
		"""
		x=  frappe.db.sql(query , as_dict = 1)
		frappe.msgprint(f"{x}")
		return x
	pass

@frappe.whitelist()
def create_assignment(employee, training_events):
	new_doc = frappe.get_doc(
		{
			"doctype":"Upload Assignment",
			"training_event": training_events,
			"employee":employee
		}
	)
	new_doc.insert()
	return new_doc.name

@frappe.whitelist()
def create_assesment(employee, training_events):
	new_doc = frappe.get_doc(
		{
			"doctype":"Upload Assessment",
			"training_event": training_events,
			"employee":employee
		}
	)
	new_doc.insert()
	return new_doc.name
# @frappe.whitelist()
# def get_question_count(grade, question_no):
# 		import ast
# 		data= []
# 		my_list = ast.literal_eval(question_no)
# 		for question in my_list:
# 			frappe.msgprint(f"{question	}")
# 			data.append(frappe.db.sql( f"""
# 						select 
# 							count(name) as count 
# 							from
# 								`tabTrainee Survey`
# 							where
# 									1=1		   
# 							  and `tabTrainee Survey`.{question} = '{grade}'

# 						""")[0][0])
# 		return data

@frappe.whitelist()
def get_survey_link_for_training_event(training_events):
	query = f"""
				Select  * from `tabTraining Event` TE where name='{training_events}'
			"""
		
	training_events =  frappe.db.sql(query, as_dict = 1)
	return  training_events	