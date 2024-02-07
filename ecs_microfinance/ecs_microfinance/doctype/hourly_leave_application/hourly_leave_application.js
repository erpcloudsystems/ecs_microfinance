// Copyright (c) 2021, erpcloud.systems and contributors
// For license information, please see license.txt
/*
frappe.ui.form.on("Hourly Leave Application", "validate", function(frm, cdt, cdn){

    var depreciation_start_date = moment(frm.doc.date).startOf('month').format('YYYY-MM-DD');
    var depreciation_end_date = moment(frm.doc.date).endOf('month').format('YYYY-MM-DD');
    var cur_month_days = moment(frm.doc.date).endOf('month').format('DD');
    var prev_month = frappe.datetime.add_months(frm.doc.date, -1);
    var prev_month_days = moment(prev_month).endOf('month').format('DD');
        if(prev_month_days == '31'){
            cur_frm.doc.start_date = frappe.datetime.add_days(depreciation_start_date, -6);
        }
        if(cur_month_days == '31'){
            cur_frm.doc.end_date = frappe.datetime.add_days(depreciation_end_date, -6);
        }
        if(prev_month_days == '30'){
            cur_frm.doc.start_date = frappe.datetime.add_days(depreciation_start_date, -5);
        }
        if(cur_month_days == '30'){
            cur_frm.doc.end_date = frappe.datetime.add_days(depreciation_end_date, -5);
        }
        if(prev_month_days == '29'){
            cur_frm.doc.start_date = frappe.datetime.add_days(depreciation_start_date, -4);
        }
        if(cur_month_days == '29'){
            cur_frm.doc.end_date = frappe.datetime.add_days(depreciation_end_date, -4);
        }
        if(prev_month_days == '28'){
            cur_frm.doc.start_date = frappe.datetime.add_days(depreciation_start_date, -3);
        }
        if(cur_month_days == '28'){
            cur_frm.doc.end_date = frappe.datetime.add_days(depreciation_end_date, -3);
        }
        refresh_field("start_date");
        refresh_field("end_date");

});
*/