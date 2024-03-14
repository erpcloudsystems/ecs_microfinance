# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Assesment(Document):
	pass
from random import sample

@frappe.whitelist()
def get_random_questions(event, num_questions=2):
    # Fetch all questions linked to the specified event
    questions = frappe.get_all("LMS Question", filters={"event": event}, fields=["name"])

    # Extract question names from the fetched questions
    question_names = [question.name for question in questions]

    # Select a random sample of questions
    random_questions = sample(question_names, min(num_questions, len(question_names)))

    # Return the list of random question names
    return random_questions
