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