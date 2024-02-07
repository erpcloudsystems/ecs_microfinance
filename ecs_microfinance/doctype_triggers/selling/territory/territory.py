from __future__ import unicode_literals
import frappe
from frappe import _


@frappe.whitelist()
def before_insert(doc, method=None):
    new_code = increase_code_territory(doc)
    doc.code = new_code
    path = get_path_to_parent(doc)
    doc.territory_name = path + '' + str(doc.code) + ' ' + doc.territory_name


@frappe.whitelist()
def onload(doc, method=None):
    pass


@frappe.whitelist()
def after_insert(doc, method=None):
    pass


@frappe.whitelist()
def before_validate(doc, method=None):
    pass


@frappe.whitelist()
def validate(doc, method=None):
    pass


@frappe.whitelist()
def on_save(doc, method=None):
    pass


@frappe.whitelist()
def on_update(doc, method=None):
    pass


@frappe.whitelist()
def on_submit(doc, method=None):
    pass


# def increase_code_territory(doc):
#     last_code = get_path_to_parent(doc)
#     new_code = increase_current_max_code_territory(last_code)
#     return new_code

def get_path_to_parent(doc):

    query = f"""
        WITH RECURSIVE territory_tree AS (
        SELECT name, old_parent, parent_territory, 1 AS level,
            IF(`name` <> 'All Territories', `name`, '') AS path
        FROM `tabTerritory`
        WHERE parent_territory IS NULL
        UNION ALL
        SELECT t.name, t.old_parent, t.parent_territory, tt.level + 1,
            CONCAT(IF(tt.path = '', '', CONCAT(tt.path, '')), t.code)
        FROM `tabTerritory` t
        INNER JOIN territory_tree tt ON tt.name = t.parent_territory
    )
    SELECT path
    FROM territory_tree
    WHERE name = '{doc.parent_territory}'
    """
    result = frappe.db.sql(query, as_dict=1)
    return result[0]['path']


def increase_code_territory(doc):
    last_code = get_max_code_territory(doc)
    new_code = increase_current_max_code_territory(last_code)
    return new_code


def increase_current_max_code_territory(last_code):
    new_code = 1
    if last_code and last_code[0]['code']:
        current_max_code = int(last_code[0]['code'])
        new_code = current_max_code + 1
    return new_code


def get_max_code_territory(doc):
    query = f"""
    SELECT parent_territory, old_parent, name, code
    FROM tabTerritory
    WHERE parent_territory = '{doc.parent_territory}'
    ORDER BY code DESC
    LIMIT 1;
    """
    last_code = frappe.db.sql(query, as_dict=1)
    return last_code
