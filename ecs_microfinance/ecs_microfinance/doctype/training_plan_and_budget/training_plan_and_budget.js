// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Plan And Budget', {
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



frappe.ui.form.on('Training Plan And Budget', {
    validate: function(frm) {
        // Add a listener for when a row is deleted in training_need_table
        frm.fields_dict['training_need_table'].grid.wrapper.on('grid-row-delete', function(frm) {
            var deleted_row = frm.selected_children[0];
            var employee_to_delete = deleted_row.employee;

            // Remove corresponding rows in training_budget_table where employee = employee_to_delete
            var budget_table = frm.doc.training_budget_table || [];
            frm.doc.training_budget_table = budget_table.filter(function(row) {
                return row.employee !== employee_to_delete;
            });

            frm.refresh_field('training_budget_table');
        });
    }
});
