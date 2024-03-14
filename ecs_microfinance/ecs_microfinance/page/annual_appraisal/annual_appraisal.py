import frappe

@frappe.whitelist()
def get_designation(designation,employee, selected_date):
    designate = frappe.get_doc("Designation",designation)
    if designate.appraisal_template:

        appraisal_template = frappe.get_doc("Appraisal Template",designate.appraisal_template)
        # return appraisal_template.goals, appraisal_template.competencies_template
        appraisals = get_annual_appraisal(designation , employee, selected_date)
        return calculate_avg_kpi(appraisals) , calculate_avg_competencies(appraisals), len(appraisals),get_kpi_competencies_weight_appraisal(designation , employee, selected_date), get_employee_details(employee)
        return get_annual_appraisal(designation , employee, selected_date)

def get_employee_details(employee):
    return frappe.db.sql( f"""
        SELECT
            *
        FROM
            `tabEmployee`
        WHERE
            name = '{employee}'
    """,as_dict = 1)
def get_annual_appraisal(designation , employee, selected_date):
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
            YEAR(`tabAppraisal Cycle`.start_date) = YEAR('{selected_date}') 
            AND `tabAppraisal`.employee = '{employee}'
            AND `tabAppraisal`.designation = '{designation}';
    """,as_dict = 1)

def get_kpi_competencies_weight_appraisal(designation , employee, selected_date):
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
            YEAR(`tabAppraisal Cycle`.start_date) = YEAR('{selected_date}') 
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