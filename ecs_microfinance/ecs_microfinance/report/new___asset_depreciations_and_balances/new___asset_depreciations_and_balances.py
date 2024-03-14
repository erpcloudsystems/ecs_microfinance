# Copyright (c) 2024, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import add_days, flt, formatdate


def execute(filters=None):
    filters.day_before_from_date = add_days(filters.from_date, -1)
    columns, data = get_columns(filters), get_data(filters)
    return columns, data


def get_data(filters):
    data = []

    asset_categories = get_asset_categories(filters)
    assets = get_assets(filters)
        


    for asset_category in asset_categories:
        row = frappe._dict()
        # row.asset_category = asset_category
        row.update(asset_category)

        row.fixed_asset_account = asset_category.get("fixed_asset_account", "")

        row.cost_as_on_to_date = (
            flt(row.cost_as_on_from_date)
            + flt(row.cost_of_new_purchase)
            - flt(row.cost_of_sold_asset)
            - flt(row.cost_of_scrapped_asset)
        )

        row.update(
            next(
                asset
                for asset in assets
                if asset["asset_category"] == asset_category.get("asset_category", "")
            )
        )
        row.accumulated_depreciation_as_on_to_date = (
            flt(row.accumulated_depreciation_as_on_from_date)
            + flt(row.depreciation_amount_during_the_period)
            - flt(row.depreciation_eliminated_during_the_period)
        )

        row.net_asset_value_as_on_from_date = flt(row.cost_as_on_from_date) - flt(
            row.accumulated_depreciation_as_on_from_date
        )

        row.net_asset_value_as_on_to_date = flt(row.cost_as_on_to_date) - flt(
            row.accumulated_depreciation_as_on_to_date
        )

        data.append(row)

    return data


def refactor_data(data, filters):
    response = []
    if filters.get("fixed_asset_account"):
        for row in data:
            if row.get("fixed_asset_account"):
                if row.get("fixed_asset_account") == filters.get("fixed_asset_account"):
                    response.append(row)
    else:
        response = data

    return response

def get_asset_categories(filters):
    condition = ""
    if filters.get("fixed_asset_account"):
        condition = "AND acc.fixed_asset_account = %(fixed_asset_account)s"

    return frappe.db.sql(
        """
        SELECT a.asset_category, 
                acc.fixed_asset_account as fixed_asset_account,
               ifnull(sum(case when a.purchase_date < %(from_date)s then
                               case when ifnull(a.disposal_date, 0) = 0 or a.disposal_date >= %(from_date)s then
                                    a.gross_purchase_amount
                               else
                                    0
                               end
                           else
                                0
                           end), 0) as cost_as_on_from_date,
               ifnull(sum(case when a.purchase_date >= %(from_date)s then
                                       gross_purchase_amount
                                  else
                                          0
                                  end), 0) as cost_of_new_purchase,
               ifnull(sum(case when ifnull(a.disposal_date, 0) != 0
                                       and a.disposal_date >= %(from_date)s
                                       and a.disposal_date <= %(to_date)s then
                               case when a.status = "Sold" then
                                       a.gross_purchase_amount
                               else
                                       0
                               end
                           else
                                0
                           end), 0) as cost_of_sold_asset,
               ifnull(sum(case when ifnull(a.disposal_date, 0) != 0
                                       and a.disposal_date >= %(from_date)s
                                       and a.disposal_date <= %(to_date)s then
                               case when a.status = "Scrapped" then
                                       a.gross_purchase_amount
                               else
                                       0
                               end
                           else
                                0
                           end), 0) as cost_of_scrapped_asset
        FROM `tabAsset` a
        LEFT JOIN `tabAsset Category Account` acc ON a.asset_category = acc.parent
        WHERE a.docstatus = 1 AND a.company = %(company)s AND a.purchase_date <= %(to_date)s {condition}
        GROUP BY asset_category
    """.format(condition=condition),
        {"to_date": filters.to_date, "from_date": filters.from_date, "company": filters.company,
         "fixed_asset_account": filters.get("fixed_asset_account")},
        as_dict=1,
    )

def get_assets(filters):
    condition = ""
    if filters.get("fixed_asset_account"):
        condition = "AND acc.fixed_asset_account = %(fixed_asset_account)s"

    return frappe.db.sql(
        """
        SELECT results.asset_category,
               sum(results.accumulated_depreciation_as_on_from_date) as accumulated_depreciation_as_on_from_date,
               sum(results.depreciation_eliminated_during_the_period) as depreciation_eliminated_during_the_period,
               sum(results.depreciation_amount_during_the_period) as depreciation_amount_during_the_period
        FROM (SELECT a.asset_category,
                     acc.fixed_asset_account as fixed_asset_account,

                   ifnull(sum(case when gle.posting_date < %(from_date)s and (ifnull(a.disposal_date, 0) = 0 or a.disposal_date >= %(from_date)s) then
                                   gle.debit
                              else
                                   0
                              end), 0) as accumulated_depreciation_as_on_from_date,
                   ifnull(sum(case when ifnull(a.disposal_date, 0) != 0 and a.disposal_date >= %(from_date)s
                                        and a.disposal_date <= %(to_date)s and gle.posting_date <= a.disposal_date then
                                   gle.debit
                              else
                                   0
                              end), 0) as depreciation_eliminated_during_the_period,
                   ifnull(sum(case when gle.posting_date >= %(from_date)s and gle.posting_date <= %(to_date)s
                                        and (ifnull(a.disposal_date, 0) = 0 or gle.posting_date <= a.disposal_date) then
                                   gle.debit
                              else
                                   0
                              end), 0) as depreciation_amount_during_the_period
            FROM `tabAsset` a
            join `tabGL Entry` gle
			on
			gle.against_voucher = a.name
            LEFT JOIN `tabAsset Category Account` acc ON a.asset_category = acc.parent
            WHERE a.docstatus = 1 AND a.company = %(company)s AND a.purchase_date <= %(to_date)s
               {condition}
            GROUP BY a.asset_category
            UNION
            SELECT a.asset_category,
                acc.fixed_asset_account as fixed_asset_account,

                   ifnull(sum(case when ifnull(a.disposal_date, 0) != 0 and (a.disposal_date < %(from_date)s or a.disposal_date > %(to_date)s) then
                                    0
                               else
                                    a.opening_accumulated_depreciation
                               end), 0) as accumulated_depreciation_as_on_from_date,
                   ifnull(sum(case when a.disposal_date >= %(from_date)s and a.disposal_date <= %(to_date)s then
                                   a.opening_accumulated_depreciation
                              else
                                   0
                              end), 0) as depreciation_eliminated_during_the_period,
                   0 as depreciation_amount_during_the_period
            FROM `tabAsset` a
            LEFT JOIN `tabAsset Category Account` acc ON a.asset_category = acc.parent
            WHERE a.docstatus = 1 AND a.company = %(company)s AND a.purchase_date <= %(to_date)s {condition}
            GROUP BY a.asset_category) AS results
        GROUP BY results.asset_category
    """.format(condition=condition),
        {"to_date": filters.to_date, "from_date": filters.from_date, "company": filters.company,
         "fixed_asset_account": filters.get("fixed_asset_account")},
        as_dict=1,
    )


def get_columns(filters):
    return [
        {
            "label": _("Asset Category"),
            "fieldname": "asset_category",
            "fieldtype": "Link",
            "options": "Asset Category",
            "width": 120,
        },
        {
            "label": _("Fixed Asset Account"),
            "fieldname": "fixed_asset_account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 120,
        },

        {
            "label": _("Cost as on") + " " + formatdate(filters.day_before_from_date),
            "fieldname": "cost_as_on_from_date",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Cost of New Purchase"),
            "fieldname": "cost_of_new_purchase",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Cost of Sold Asset"),
            "fieldname": "cost_of_sold_asset",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Cost of Scrapped Asset"),
            "fieldname": "cost_of_scrapped_asset",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Cost as on") + " " + formatdate(filters.to_date),
            "fieldname": "cost_as_on_to_date",
            "fieldtype": "Currency",
            "width": 140,
        },
        {
            "label": _("Accumulated Depreciation as on") + " " + formatdate(filters.day_before_from_date),
            "fieldname": "accumulated_depreciation_as_on_from_date",
            "fieldtype": "Currency",
            "width": 270,
        },
        {
            "label": _("Depreciation Amount during the period"),
            "fieldname": "depreciation_amount_during_the_period",
            "fieldtype": "Currency",
            "width": 240,
        },
        {
            "label": _("Depreciation Eliminated due to disposal of assets"),
            "fieldname": "depreciation_eliminated_during_the_period",
            "fieldtype": "Currency",
            "width": 300,
        },
        {
            "label": _("Accumulated Depreciation as on") + " " + formatdate(filters.to_date),
            "fieldname": "accumulated_depreciation_as_on_to_date",
            "fieldtype": "Currency",
            "width": 270,
        },
        {
            "label": _("Net Asset value as on") + " " + formatdate(filters.day_before_from_date),
            "fieldname": "net_asset_value_as_on_from_date",
            "fieldtype": "Currency",
            "width": 200,
        },
        {
            "label": _("Net Asset value as on") + " " + formatdate(filters.to_date),
            "fieldname": "net_asset_value_as_on_to_date",
            "fieldtype": "Currency",
            "width": 200,
        },
    ]
