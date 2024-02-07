from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    pass
@frappe.whitelist()
def after_insert(doc, method=None):
    as_qty = 0
    pr = frappe.db.sql(""" select
                                PRI.name as name,PRI.new_description as new_description,
                                PRI.territory as territory,
                                PRI.assets_qty,
                                PRI.received_stock_qty as received_stock_qty
                            from
                                 `tabPurchase Receipt Item` PRI
                            where
                                  PRI.parent = '{parent}'
                            and 
                                PRI.net_rate = '{gross_purchase_amount}'
                            and 
                                PRI.asset_location = '{asset_location}'
                            and 
                                PRI.received_stock_qty > PRI.assets_qty
                        """.format(parent=doc.purchase_receipt, gross_purchase_amount=doc.gross_purchase_amount,asset_location=doc.location), as_dict=1)
    for b in pr:
        doc.new_description = b.new_description
        doc.territory = b.territory
        as_qty = b.assets_qty +1
        
        frappe.db.set_value('Asset', doc.name, 'territory', b.territory)
        frappe.db.set_value('Asset', doc.name, 'purchase_res_item_name', b.name)
        frappe.db.set_value('Asset', doc.name, 'new_description', b.new_description)
        frappe.db.set_value('Asset', doc.name, 'assets_qty', as_qty)
        # frappe.db.sql(""" update PRI set assets_qty = '{as_qty}' where name = '{name}' """.format(as_qty=as_qty, name=b.name))
        # frappe.db.sql(""" update `tabAsset` set new_description = '{new_description}' where name = '{name}' and purchase_res_item_name ="" """.format(new_description=b.new_description, name=doc.name))
        # frappe.db.sql(""" update `tabAsset` set territory = '{territory}' where name = '{name}' and purchase_res_item_name ="" """.format(territory=b.territory, name=doc.name))
    frappe.db.set_value('Asset', doc.name, 'asset_quantity', 1)
    # frappe.db.sql(""" update `tabAsset` set asset_quantity = 1 where name = '{name}' """.format(name=doc.name))
    #doc.save()
    frappe.db.commit()


@frappe.whitelist()
def onload(doc, method=None):
    # new_des = frappe.db.get_value('Purchase Receipt Item',{"parent":doc.purchase_receipt},fieldname = ['new_description'])
    # frappe.db.set_value('Asset', doc.name, 'new_description', new_des)
    # frappe.db.commit()
    pass

@frappe.whitelist()
def before_validate(doc, method=None):
    pass

@frappe.whitelist()
def validate(doc, method=None):
    new_des = frappe.db.get_value('Purchase Receipt Item',{"parent":doc.purchase_receipt},fieldname = ['new_description'])
    frappe.db.set_value('Asset', doc.name, 'new_description', new_des)
    frappe.db.commit()

@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass
