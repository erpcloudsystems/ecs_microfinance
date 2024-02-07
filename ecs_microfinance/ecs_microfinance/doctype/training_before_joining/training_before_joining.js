// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Before Joining', {
    get_attendance_no: function (frm) {
        frm.doc.cows = []
        frappe.call({
            doc: frm.doc,
            method: "get_attendance_no",
            callback: function (r) {
                frm.refresh_fields();
                frm.refresh();
            }
        });
    }
});
