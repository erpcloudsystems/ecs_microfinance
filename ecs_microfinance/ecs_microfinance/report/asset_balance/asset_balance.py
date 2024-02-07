# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("رقم الأصل"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Asset",
            "width": 150
        },
        {
            "label": _("اسم الأصل"),
            "fieldname": "asset_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("مجموعة الاصول"),
            "fieldname": "asset_category",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("وصف الاصل"),
            "fieldname": "new_description",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("مكان التواجد"),
            "fieldname": "territory",
            "fieldtype": "Link",
            "options": "Territory",

            "width": 150
        },
        {
            "label": _("تاريخ الشراء"),
            "fieldname": "purchase_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("حالة الملكية"),
            "fieldname": "asset_status",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("العدد"),
            "fieldname": "count",
            "fieldtype": "Data",
            "width": 150
        },

        {
            "label": _("سعر الوحده"),
            "fieldname": "item_price",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("الاجمالي"),
            "fieldname": "total",
            "fieldtype": "int",
            "width": 150
        },
        {
            "label": _("العدد الفعلي"),
            "fieldname": "count1",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("الفرق"),
            "fieldname": "count2",
            "fieldtype": "Data",
            "width": 150
        },

    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data



def get_item_price_qty_data(filters):
    conditions = ""
    conditions1 = ""
    if filters.get("asset_category"):
        if len(filters.get("asset_category"))==1:
            filters.get('asset_category').append("None")
        conditions += f" and asset.asset_category in {tuple(filters.get('asset_category'))}"

    if filters.get("territory"):
        if len(filters.get("territory"))==1:
            filters.get('territory').append("None")
        conditions += f" and asset.territory in {tuple(filters.get('territory'))}"

    #
    # if filters.get("territory"):
    #     conditions += " and asset.territory =%(territory)s"
    if filters.get("from_date"):
        conditions += " and asset.purchase_date >=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and asset.purchase_date <=%(to_date)s"
    item_results = frappe.db.sql("""
            SELECT
             asset.name as name,
             asset.asset_name as asset_name,
             asset.asset_category as asset_category,
             asset.new_description as new_description,
             asset.territory as territory,
             asset.purchase_date as purchase_date,
             asset.asset_owner as asset_status,
             asset.asset_quantity as count,
             asset.gross_purchase_amount as item_price,
            ROUND((asset.asset_quantity * asset.gross_purchase_amount)) as total
            from `tabAsset` asset
            where asset.docstatus=1
            AND asset.workflow_state!="Cancelled"
            {conditions}
            ORDER BY asset.asset_name
        """.format(conditions=conditions), filters , as_dict=1)

    result = []
    if item_results:
        for item_dict in item_results:
            # Handle potential None values
            asset_name = item_dict.asset_name or ""
            new_description = item_dict.new_description or ""

            con_value = asset_name + " " + new_description

            data = {
                'name': item_dict.name,
                'asset_name': item_dict.asset_name,
                'asset_category': (item_dict.asset_category),
                'new_description': (item_dict.new_description),
                'territory': (item_dict.territory),
                'purchase_date': (item_dict.purchase_date),
                'asset_status': (item_dict.asset_status),
                'count': (item_dict.count),
                'item_price': (item_dict.item_price),
                'total': (item_dict.total),
                'con': con_value,
            }

            result.append(data)

    return result



