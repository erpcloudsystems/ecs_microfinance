from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    try:
        doc.journal_month = doc.posting_date.split("-")[1]
        doc.journal_year = doc.posting_date.split("-")[0]
    except AttributeError:
        journal_month = doc.posting_date.strftime("%Y-%m-%d")
        doc.journal_month = journal_month.split("-")[1]
        journal_year = doc.posting_date.strftime("%Y-%m-%d")
        doc.journal_year = journal_year.split("-")[0]
    last_code = frappe.db.sql(
        """ select max(journal_no) as max from `tabJournal Entry` 
        where name != '{name}' and journal_month = '{month}' and journal_year = '{year}'
        """.format(
            name=doc.name, month=doc.journal_month, year=doc.journal_year
        ),
        as_dict=1,
    )
    for x in last_code:
        if not x.max:
            doc.journal_no = 1
        else:
            if doc.amended_from:
                doc.journal_no = int(x.max)
            if not doc.amended_from:
                doc.journal_no = int(x.max) + 1


@frappe.whitelist()
def after_insert(doc, method=None):
    pass


@frappe.whitelist()
def onload(doc, method=None):
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


@frappe.whitelist()
def validate(doc, method=None):
    pass


@frappe.whitelist()
def on_submit(doc, method=None):
    pass


@frappe.whitelist()
def on_cancel(doc, method=None):
    # name  = frappe.db.get_value("Grouped Journal Entries", {"reference_journal" :doc.name}, ["name"])
    # if name:
    #     name.cancel()
    # journal_doc = frappe.get_doc("Journal Entry", doc.name)
    # journal_doc.cancel()
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

@frappe.whitelist()
def before_delete(doc, method=None):
    frappe.throw('hiiii')
    pass