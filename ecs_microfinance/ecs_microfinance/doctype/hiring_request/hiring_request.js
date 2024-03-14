// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Hiring Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Hiring Request", {
    get_current_staffing_plan: function(frm) {
        frappe.call({
            method: "set_hiring_request_details", // Name of the server-side method to call
            doc: frm.doc, // Passing the current form document to the server-side method
            callback: function(r) {
                frm.refresh();
            }
        });
        frm.refresh_field("hiring_request_details"); // Refreshing the specified field on the form
    }
});





