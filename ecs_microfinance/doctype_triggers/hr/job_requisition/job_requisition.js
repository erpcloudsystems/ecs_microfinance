frappe.ui.form.on('Job Requisition', 'designation', function(frm) {
    frappe.call({
        method: "ecs_microfinance.doctype_triggers.hr.job_requisition.job_requisition.get_salary",
        args: {
            "designation": frm.doc.designation
        },
        callback: function(r) {
            // Handle the response here if necessary
            console.log(r.message);
            var total_allowances = r.message.custom_other_allowance + r.message.custom_mobile_allowance + r.message.custom_living_allowance + r.message.housing_allowance + r.message.transportation_allowance
            frm.set_value('custom_incentive', r.message.custom_incentives);
            frm.set_value('custom_allowances', total_allowances);
            frm.set_value('custom_basic_salary', r.message.basic_salary);
            frm.set_value('expected_compensation', r.message.basic_salary + total_allowances +  r.message.custom_incentives);
        }
    });

    frm.refresh_fields(["expected_compensation", "custom_incentive", "custom_allowances", "custom_basic_salary"]);
});

frappe.ui.form.on('Job Requisition','custom_basic_salary',function(frm){
    frm.set_value('expected_compensation', frm.doc.custom_basic_salary + frm.doc.custom_allowances + frm.doc.custom_incentive);
    frm.refresh_field("expected_compensation")
});
frappe.ui.form.on('Job Requisition','custom_allowances',function(frm){
    frm.set_value('expected_compensation', frm.doc.custom_basic_salary + frm.doc.custom_allowances + frm.doc.custom_incentive);
    frm.refresh_field("expected_compensation")
});
frappe.ui.form.on('Job Requisition','custom_incentive',function(frm){
    frm.set_value('expected_compensation', frm.doc.custom_basic_salary + frm.doc.custom_allowances + frm.doc.custom_incentive);
    frm.refresh_field("expected_compensation")
});