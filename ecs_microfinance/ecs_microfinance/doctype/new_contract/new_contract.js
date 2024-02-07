// Copyright (c) 2023, erpcloudsystems and contributors
// For license information, please see license.txt

frappe.ui.form.on("New Contract", "upon_signature_percent", function(frm, cdt, cdn) {
	var upon_signature_amount = frm.doc.bond_size * frm.doc.upon_signature_percent / 100;
	frm.set_value("upon_signature_amount", upon_signature_amount);
});

frappe.ui.form.on("New Contract", "operation_review_percent", function(frm, cdt, cdn) {
	var operation_review_amount = frm.doc.bond_size * frm.doc.operation_review_percent / 100;
	frm.set_value("operation_review_amount", operation_review_amount);
});

frappe.ui.form.on("New Contract", "rating_comity_percent", function(frm, cdt, cdn) {
	var rating_committee_amount = frm.doc.bond_size * frm.doc.rating_comity_percent / 100;
	frm.set_value("rating_committee_amount", rating_committee_amount);
});

frappe.ui.form.on('New Contract', {
	refresh: function(frm, cdt, cdn) {
		if (frm.doc.docstatus == 1 && frm.doc.transaction_type == "Corporate Bond"){
			frm.add_custom_button(__("Corporate Tracker"), function() {
				var child = locals[cdt][cdn];
				frappe.route_options = {
					"contract": frm.doc.name,
					"issuer": frm.doc.client,
					"applicant_form": frm.doc.applicant_form,
					"tracker_template": "Corporate Tracker",
				};
				frappe.new_doc("Tracker");
			}, __("Create"));
		}
		if (frm.doc.docstatus == 1 && frm.doc.transaction_type == "Securitization"){
			frm.add_custom_button(__("Securitization Tracker"), function() {
				var child = locals[cdt][cdn];
				frappe.route_options = {
					"contract": frm.doc.name,
					"issuer": frm.doc.client,
					"applicant_form": frm.doc.applicant_form,
					"tracker_template": "Securitization Tracker",
				};
				frappe.new_doc("Tracker");
			}, __("Create"));
		}
		if (frm.doc.docstatus == 1){
			frm.add_custom_button(__("Increase Of Fees"), function() {
				var child = locals[cdt][cdn];
				frappe.route_options = {
					"contract": frm.doc.name,
					"applicant": frm.doc.client,
				};
				frappe.new_doc("Increase Of Fees");
			}, __("Create"));
		}
		if (frm.doc.docstatus == 1){
			frm.add_custom_button(__("Decrease Of Fees"), function() {
				var child = locals[cdt][cdn];
				frappe.route_options = {
					"contract": frm.doc.name,
					"applicant": frm.doc.client,
				};
				frappe.new_doc("Decrease Of Fees");
			}, __("Create"));
		}
	}
});