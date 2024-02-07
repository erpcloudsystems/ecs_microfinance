from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    for d in doc.items:
        if (frappe.db.get_value("Item", d.item_code, "is_fixed_asset")) == 0:
            d.assets_qty = 0
        else:
            d.assets_qty = d.qty
@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    for d in doc.items:
        if (frappe.db.get_value("Item", d.item_code, "is_fixed_asset")) == 0:
            d.assets_qty = 0
        else:
            d.assets_qty = d.qty
@frappe.whitelist()
def validate(doc, method=None):
    pass
@frappe.whitelist()
def on_submit(doc, method=None):
    pass
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
