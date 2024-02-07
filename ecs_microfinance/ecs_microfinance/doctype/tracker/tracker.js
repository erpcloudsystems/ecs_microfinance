// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tracker", "tracker_template", function(frm){
	if(frm.doc.tracker_template){
		frappe.model.with_doc("Tracker Template", frm.doc.tracker_template, function() {
			var tabletransfer= frappe.model.get_doc("Tracker Template", frm.doc.tracker_template);
			cur_frm.clear_table("tasks_table");
			$.each(tabletransfer.tasks_table, function(d, row){
				d = frm.add_child("tasks_table");
				d.step = row.step;
				cur_frm.refresh_field("tasks_table");
			});
		});
	}
});
