// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

// frappe.ui.form.on("End of Service", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("End of Service", {
    employee: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: "get_employee_data",
                doc: frm.doc,
                callback: function(r) {
                    frm.refresh();
                }
            });
        }
    }
});


frappe.ui.form.on("End of Service", {
    last_working_date: function(frm) {
        if (frm.doc.last_working_date) {
            frappe.call({
                method: "calculte_days",
                doc: frm.doc,
                callback: function(r) {
                    frm.refresh();
                }
            });
        }
    }
});