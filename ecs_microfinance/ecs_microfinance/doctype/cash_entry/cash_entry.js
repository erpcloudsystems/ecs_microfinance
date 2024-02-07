// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt


frappe.ui.form.on('Cash Entry', 'mode_of_payment',  function(frm) {
   if(cur_frm.doc.payment_type == "Receive"){
       frappe.call({ method: "frappe.client.get_value",
args: { doctype: "Mode of Payment Account",
fieldname: "default_account",
parent: "Mode of Payment",
filters: { 'parent': cur_frm.doc.mode_of_payment},
}, callback: function(r)
{cur_frm.set_value("account_paid_to", r.message.default_account);
  } });
   }
if(cur_frm.doc.payment_type == "Pay"){
       frappe.call({ method: "frappe.client.get_value",
args: { doctype: "Mode of Payment Account",
fieldname: "default_account",
parent: "Mode of Payment",
filters: { 'parent': cur_frm.doc.mode_of_payment},
}, callback: function(r)
{cur_frm.set_value("account_paid_from", r.message.default_account);
  } });
   }
});

/*
frappe.ui.form.on('Cash Entry',{

    setup: function(frm) {
  cur_frm.fields_dict['expense_entry_account'].grid.get_field("party_type").get_query = function(doc, cdt, cdn)
  {
  	return {
    filters:  [
    	["DocType","name", "in", ["Customer","Supplier","Employee"]]
    ]
    	};
  };
	}
});
*/


frappe.ui.form.on('Cash Entry',{
    setup: function(frm) {
        cur_frm.fields_dict['expense_entry_account'].grid.get_field("party_type").get_query = function(doc, cdt, cdn){
            if(locals[cdt][cdn].account_type == "Payable"){
                return {
                    filters:  [
                        ["DocType","name", "in", "Customer"]
                    ]
                };
            }
            if(locals[cdt][cdn].account_type == "Receivable"){
                return {
                    filters:  [
                        ["DocType","name", "in", ["Supplier","Employee"]]
                    ]
                };
            }
            else{
                return {
                    filters:  [
                        ["DocType","name", "=", "C"]
                    ]
                };
            }
        };
	}
});

/*
frappe.ui.form.on('Cash Entry',{
    setup: function(frm) {
        cur_frm.fields_dict['expense_entry_account'].grid.get_field("party_type").get_query = function(doc, cdt, cdn){
            if(locals[cdt][cdn].account_type == "Receivable"){
                return {
                    filters:  [
                        ["DocType","name", "in", ["Supplier","Employee"]]
                    ]
                };
            }
        };
	}
});
*/



frappe.ui.form.on('Cash Entry',{
    setup: function(frm) {
  cur_frm.fields_dict['expense_entry_account'].grid.get_field("account").get_query = function(doc, cdt, cdn)
  {
  	return {
    filters:  [
    	["Account","is_group", "=", 0]
    ]
    	};
  };
	}
});




