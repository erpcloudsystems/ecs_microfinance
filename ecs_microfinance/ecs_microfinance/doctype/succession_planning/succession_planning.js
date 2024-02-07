// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Succession Planning', {
	get_employee: function(frm) {
		frm.doc.cows = []
		frappe.call({
			doc: frm.doc,
			method: "get_employee",
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		});
	}
});

frappe.ui.form.on('Succession Planning', {
	get_employees: function(frm) {
		frm.doc.cows = []
		frappe.call({
			doc: frm.doc,
			method: "get_employees",
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		});
	}
});

