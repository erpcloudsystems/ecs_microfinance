import frappe

@frappe.whitelist()
def get_designation(f_employee,s_employee):
    f_employee_data = get_employee_details(f_employee)
    s_employee_data = get_employee_details(s_employee)
    designate_1 = frappe.get_doc("Designation",f_employee_data[0]['designation'])
    designate_2 = frappe.get_doc("Designation",s_employee_data[0]['designation'])
    goals_1 = []
    goals_2 = []
    competencies_template_1 = []
    competencies_template_2 = []
    evaluation_1 = []
    evaluation_2 = []
    if designate_1.appraisal_template:

        appraisal_template = frappe.get_doc("Appraisal Template",designate_1.appraisal_template)
        goals_1.extend(appraisal_template.goals)
        competencies_template_1.extend(appraisal_template.competencies_template)
    if designate_2.appraisal_template:

        appraisal_template = frappe.get_doc("Appraisal Template",designate_2.appraisal_template)
        goals_2.extend(appraisal_template.goals)
        competencies_template_2.extend(appraisal_template.competencies_template)

    if designate_1.custom_assessor_evaluation:
        evaluation_template = frappe.get_doc("Assessor Evaluation Template", designate_1.custom_assessor_evaluation)
        evaluation_1.extend(evaluation_template.assessor_evaluation_table)

    if designate_2.custom_assessor_evaluation:
        evaluation_template = frappe.get_doc("Assessor Evaluation Template", designate_2.custom_assessor_evaluation)
        evaluation_2.extend(evaluation_template.assessor_evaluation_table)

    f_appraisals = get_annual_appraisal(designate_1.name , f_employee)
    s_appraisals = get_annual_appraisal(designate_2.name , s_employee)
    f_assessor = get_annual_assessor(designate_1.name , f_employee)
    s_assessor = get_annual_assessor(designate_2.name , s_employee)
    data = {
        "goals_1":goals_1,
        "goals_2":goals_2,
        "competencies_template_1":competencies_template_1,
        "competencies_template_2":competencies_template_2,
        "evaluation_1":evaluation_1,
        "evaluation_2":evaluation_2,
        "f_employee": (calculate_avg_kpi(f_appraisals) , calculate_avg_competencies(f_appraisals), len(f_appraisals),get_kpi_competencies_weight_appraisal(designate_1.name , f_employee), f_employee_data, get_kpi_competencies_weight_appraisal_last_year(designate_1.name , f_employee), calculate_avg_competencies_assessor(f_assessor), len(f_assessor), get_competencies_weight_assessor(designate_1.name , f_employee)),
        "s_employee" :(calculate_avg_kpi(s_appraisals) , calculate_avg_competencies(s_appraisals), len(s_appraisals),get_kpi_competencies_weight_appraisal(designate_2.name , s_employee), s_employee_data,get_kpi_competencies_weight_appraisal_last_year(designate_2.name , s_employee), calculate_avg_competencies_assessor(s_assessor), len(s_assessor), get_competencies_weight_assessor(designate_2.name , s_employee))
    }
    return data

def get_employee_details(employee):
    return frappe.db.sql( f"""
        SELECT
            *
        FROM
            `tabEmployee`
        WHERE
            name = '{employee}'
    """,as_dict = 1)

def get_annual_appraisal(designation , employee):
    return frappe.db.sql( f"""
        SELECT
            `tabAppraisal`.name as name
        FROM
            `tabAppraisal`
        JOIN
            `tabAppraisal Cycle`
        ON
            `tabAppraisal Cycle`.name = `tabAppraisal`.appraisal_cycle
        WHERE
            YEAR(`tabAppraisal Cycle`.start_date) = YEAR(CURDATE()) 
            AND `tabAppraisal`.employee = '{employee}'
            AND `tabAppraisal`.designation = '{designation}';
    """,as_dict = 1)

def get_kpi_competencies_weight_appraisal(designation , employee):
    return frappe.db.sql( f"""
        SELECT
            SUM(`tabAppraisal`.kpi_weight)  / COUNT(`tabAppraisal`.name)  as kpi_weight,
            SUM(`tabAppraisal`.competencies_weight) / COUNT(`tabAppraisal`.name) as competencies_weight,
            SUM(`tabAppraisal`.kpi_total_weight)  / COUNT(`tabAppraisal`.name) as kpi_total_weight,
            SUM(`tabAppraisal`.competencies_total_weight)  / COUNT(`tabAppraisal`.name) as competencies_total_weight
        FROM
            `tabAppraisal`
        JOIN
            `tabAppraisal Cycle`
        ON
            `tabAppraisal Cycle`.name = `tabAppraisal`.appraisal_cycle
        WHERE
            YEAR(`tabAppraisal Cycle`.start_date) = YEAR(CURDATE()) 
            AND `tabAppraisal`.employee = '{employee}'
            AND `tabAppraisal`.designation = '{designation}';
    """,as_dict = 1)

def get_kpi_competencies_weight_appraisal_last_year(designation , employee):
    return frappe.db.sql( f"""
        SELECT
            SUM(`tabAppraisal`.kpi_weight)  / COUNT(`tabAppraisal`.name)  as kpi_weight,
            SUM(`tabAppraisal`.competencies_weight) / COUNT(`tabAppraisal`.name) as competencies_weight,
            SUM(`tabAppraisal`.kpi_total_weight)  / COUNT(`tabAppraisal`.name) as kpi_total_weight,
            SUM(`tabAppraisal`.competencies_total_weight)  / COUNT(`tabAppraisal`.name) as competencies_total_weight
        FROM
            `tabAppraisal`
        JOIN
            `tabAppraisal Cycle`
        ON
            `tabAppraisal Cycle`.name = `tabAppraisal`.appraisal_cycle
        WHERE
            YEAR(`tabAppraisal Cycle`.start_date) = YEAR(CURDATE()) - 1
            AND `tabAppraisal`.employee = '{employee}'
            AND `tabAppraisal`.designation = '{designation}';
    """,as_dict = 1)

def calculate_avg_kpi(appraisals):
    kpi = []
    for appraisal in appraisals:
        goals = frappe.get_doc("Appraisal", appraisal.name).goals
        if goals:
            kpi.extend(goals)
    sorted_kpi = sorted(kpi, key=lambda x: x.idx)

    # Create a dictionary to store the sums for each unique idx
    idx_sums = {}
    # Iterate through the list and accumulate sums
    for item in sorted_kpi:
        idx = item.idx
        target = item.get("target", 0)
        achieved = item.get("achieved", 0)
        achieve_weight = item.get("achieve_weight", 0)
        per_weightage = item.get("per_weightage", 0)
        key_result_area = item.get("kra")
        # Update sums for the current idx
        if idx not in idx_sums:
            idx_sums[idx] = {"kpi": key_result_area, "per_weightage": per_weightage, "target": target, "achieved": achieved, "achieve_weight": achieve_weight}
        else:
            idx_sums[idx]["target"] += target
            idx_sums[idx]["achieved"] += achieved
            idx_sums[idx]["achieve_weight"] += achieve_weight
            idx_sums[idx]["per_weightage"] += per_weightage
        
    return idx_sums
    pass

def calculate_avg_competencies(appraisals):
    competencies = []
    for appraisal in appraisals:
        competencies_template = frappe.get_doc("Appraisal", appraisal.name).competencies_template
        if competencies_template:
            competencies.extend(competencies_template)
    sorted_kpi = sorted(competencies, key=lambda x: x.idx)

    # Create a dictionary to store the sums for each unique idx
    idx_sums = {}
    # Iterate through the list and accumulate sums
    for item in sorted_kpi:
        idx = item.get("idx")
        target = item.get("target", 0)
        manager_score1 = item.get("manager_score1", 0)
        achieve_weight = item.get("achieve_weight", 0)
        
        # Update sums for the current idx
        if idx not in idx_sums:
            idx_sums[idx] = {"competencies": item.competencies,"target": target, "manager_score1": manager_score1, "achieve_weight": achieve_weight}
        else:
            idx_sums[idx]["target"] += target
            idx_sums[idx]["manager_score1"] += manager_score1
            idx_sums[idx]["achieve_weight"] += achieve_weight
    return idx_sums
    pass

def get_annual_assessor(designation , employee):
    return frappe.db.sql( f"""
        SELECT
             `tabAssessor Evaluation`.name as name
        FROM
            `tabAssessor Evaluation`
        WHERE
            YEAR(`tabAssessor Evaluation`.start_date) = YEAR(CURDATE()) 
            AND  `tabAssessor Evaluation`.employee = '{employee}'
            AND  `tabAssessor Evaluation`.designation = '{designation}';
    """,as_dict = 1)

def calculate_avg_competencies_assessor(assessors):
    competencies = []
    for assessor in assessors:
        assessor_evaluation_table = frappe.get_doc("Assessor Evaluation", assessor.name).assessor_evaluation_table
        if assessor_evaluation_table:
            competencies.extend(assessor_evaluation_table)
    sorted_kpi = sorted(competencies, key=lambda x: x.idx)

    # Create a dictionary to store the sums for each unique idx
    idx_sums = {}
    # Iterate through the list and accumulate sums
    for item in sorted_kpi:
        idx = item.get("idx")
        target = item.get("target", 0)
        achieved = item.get("achieved", 0)
        percentage = item.get("percentage", 0)
        
        # Update sums for the current idx
        if idx not in idx_sums:
            idx_sums[idx] = {"competencies": item.competencies,"target": target, "achieved": achieved, "percentage": percentage}
        else:
            idx_sums[idx]["target"] += target
            idx_sums[idx]["achieved"] += achieved
            idx_sums[idx]["percentage"] += percentage
    return idx_sums

def get_competencies_weight_assessor(designation , employee):
    return frappe.db.sql( f"""
        SELECT
            SUM(`tabAssessor Evaluation`.total_achieved_weight)  / COUNT(`tabAssessor Evaluation`.name)  as total_achieved_weight
        FROM
            `tabAssessor Evaluation`
        WHERE
            YEAR(`tabAssessor Evaluation`.start_date) = YEAR(CURDATE()) 
            AND `tabAssessor Evaluation`.employee = '{employee}'
            AND `tabAssessor Evaluation`.designation = '{designation}';
    """,as_dict = 1)