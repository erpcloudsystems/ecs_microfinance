// Copyright (c) 2024, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Critical Key Positions', {
	get_designation: function(frm) {
		frm.doc.cows = []
		frappe.call({
			doc: frm.doc,
			method: "get_designation",
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		});
	}
});
