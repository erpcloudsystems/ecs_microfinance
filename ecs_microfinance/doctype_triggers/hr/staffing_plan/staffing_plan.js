//// Copyright (c) 2023, erpcloudsystems and contributors
//// For license information, please see license.txt
//
//frappe.ui.form.on('Staffing Plan', {
//	get_job_request: function(frm) {
//		frm.doc.cows = []
//		frappe.call({
//			doc: frm.doc,
//			method: "get_job_request",
//			callback: function(r) {
//				frm.refresh_fields();
//				frm.refresh();
//			}
//		});
//	}
//});

// frappe.ui.form.on('Staffing Plan Detail', {
//     designation: function(frm, cdt, cdn) {
//         let child = locals[cdt][cdn];
//         console.log("kkkk");
//         if (child.designation){
//         frappe.call({
//             method: "ecs_microfinance.doctype_triggers.hr.staffing_plan.staffing_plan.set_job_requisitions",
//             args: {
//                 designation: child.designation,
//             },
//             callback: function(r) {
//                 if (r.message) {
//                     console.log(r.message);
//                     // frm.set_value('custom_job_requisition', r.message.name);
//                     frappe.model.set_value(cdt,cdn,'vacancies', r.message.no_of_positions);
//                     frappe.model.set_value(cdt.cdn,'estimated_cost_per_position', r.message.expected_compensation);
//                     // frm.set_value('custom_previous_planned_manpower', r.message.total);
//                     frappe.model.set_value(cdt,cdn,'custom_branch', r.message.custom_branch);
//                     frappe.model.set_value(cdt,cdn,'custom_basic_salary', r.message.custom_basic_salary);
//                     frappe.model.set_value(cdt,cdn,'custom_incentive', r.message.custom_incentive);
//                     frappe.model.set_value(cdt,cdn,'custom_allowances', r.message.custom_allowances );
//                  }
            
//                     }
//         });
//         frm.refresh_fields(["custom_job_requisition", "vacancies", "estimated_cost_per_position", "estimated_cost_per_position"
//     ,"custom_previous_planned_manpower","custom_branch","custom_basic_salary","custom_incentive","custom_allowances"]);
//     }}
// });

frappe.ui.form.on('Staffing Plan Detail',{
    designation: function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
    if (child.designation){
    frappe.call({
        method: "ecs_microfinance.doctype_triggers.hr.staffing_plan.staffing_plan.get_salary",
        args: {
            designation: child.designation,
            branch: child.custom_branch
        },
        callback: function(r) {
            // Handle the response here if necessary
            console.log(r.message);
            var total_allowances = r.message.custom_other_allowance + r.message.custom_mobile_allowance + r.message.custom_living_allowance + r.message.housing_allowance + r.message.transportation_allowance
            frappe.model.set_value(cdt,cdn,'custom_basic_salary', r.message.basic_salary);
            frappe.model.set_value(cdt,cdn,'custom_allowances',total_allowances);
            frappe.model.set_value(cdt,cdn,'custom_incentive',r.message.custom_incentives);
            frappe.model.set_value(cdt,cdn,'custom_previous_planned_manpower',r.message.total);
            frappe.model.set_value(cdt,cdn,'estimated_cost_per_position',r.message.basic_salary + total_allowances +  r.message.custom_incentives);
        //     frm.set_value('expected_compensation', r.message.basic_salary + total_allowances +  r.message.custom_incentives);
        }
    });}
    }
});

frappe.ui.form.on('Staffing Plan',{
    refresh: function(frm) {
        cur_frm.fields_dict['staffing_details'].grid.get_field("designation").get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['Designation', 'department', '=',frm.doc.department],
                ]
            };
        };
    }
});


frappe.ui.form.on('Staffing Plan',{
    refresh: function(frm) {
        cur_frm.fields_dict['staffing_details'].grid.get_field("custom_branch").get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['Branch', 'custom_governorate', '=',frm.doc.custom_governorate],
                ]
            };
        };
    }
});


frappe.ui.form.on('Staffing Plan Detail',{
    custom_branch:  function(frm, cdt, cdn){
        let child = locals[cdt][cdn];
        if (child.designation){
            frappe.call({
                method: "ecs_microfinance.doctype_triggers.hr.staffing_plan.staffing_plan.get_previous_planned",
                args: {
                    designation: child.designation,
                    branch: child.custom_branch
                },
                callback:function(r){
                    frappe.model.set_value(cdt,cdn,'custom_previous_planned_manpower',r.message);
                }

            })

    }}
})

frappe.ui.form.on('Staffing Plan Detail',{
    custom_others:  function(frm, cdt, cdn){
        let child = locals[cdt][cdn];
        if (child.estimated_cost_per_position){
        frappe.model.set_value(cdt,cdn,'estimated_cost_per_position',child.custom_incentive + child.custom_allowances +  child.custom_basic_salary + child.custom_others);
        }
        else{
        frappe.model.set_value(cdt,cdn,'estimated_cost_per_position',child.custom_incentive + child.custom_allowances +  child.custom_basic_salary);
        }

    }
    })