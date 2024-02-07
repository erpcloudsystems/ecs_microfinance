# Copyright (c) 2023, erpcloudsystems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.desk.form.assign_to import add
from decimal import *


def to_decimal(num):
    return Decimal(str(num))


class GroupedJournalEntries(Document):
    def validate_entries(self):
        # merge duplicate account logs
        new_account_logs = []
        accounts = []
        for log in self.accounts_logs:
            if log.account not in accounts:
                new_account_logs.append(log)
                accounts.append(log.account)
            else:
                for new_log in new_account_logs:
                    if new_log.account == log.account:
                        new_log.debit = new_log.debit + log.debit
                        new_log.credit = new_log.credit + log.credit
                        new_log.percent = new_log.percent + log.percent
        # using new merged account logs
        for account_log in new_account_logs:
            percent = Decimal("0.0")
            debit = Decimal("0.0")
            credit = Decimal("0.0")
            for entry in self.grouped_journal_entries:
                if account_log.account == entry.account and (
                    account_log.log_name == entry.account_log_name
                ):
                    debit = debit + to_decimal(entry.debit)
                    credit = credit + to_decimal(entry.credit)
                    percent = percent + to_decimal(entry.percent)

            #  if (
            #     round(debit, 2) != round(account_log.debit, 2)
            #     or round(credit, 2) != round(account_log.credit, 2)
            # ):

            if abs(debit - to_decimal(account_log.debit)) > Decimal("0.00001"):
                frappe.throw(
                    "Account Checking is {0}, <br>  debit: {1},  <br>  entries for this account is <br>  debit: {2} <br>  percent: {3}%. <br> Please Check Above Values and Resubmit".format(
                        account_log.account,
                        account_log.debit,
                        debit,
                        int(round(percent, 1)),
                    )
                )

            if abs(credit - to_decimal(account_log.credit)) > Decimal("0.00001"):
                frappe.throw(
                    "Account Checking is {0}, <br>  credit: {1}  <br>  entries for this account is <br> credit: {2} <br>  percent: {3}%. <br> Please Check Above Values and Resubmit".format(
                        account_log.account,
                        account_log.credit,
                        credit,
                        int(round(percent, 1)),
                    )
                )

            # if (abs(debit - credit) > Decimal('0.00001')):
            #     frappe.throw(f"debit: {debit} is not equal credit: {credit}")

    def create_journal_entry(self):
        accounts = []
        for entry in self.grouped_journal_entries:
            accounts.append(
                {
                    "account": entry.account,
                    "territory": entry.child_territory,
                    "debit_in_account_currency": round(to_decimal(entry.debit), 3),
                    "credit_in_account_currency": round(to_decimal(entry.credit), 3),
                    "party": entry.party,
                    "party_type": entry.party_type,
                }
            )
        ref_date = ""
        if self.reference_date:
            ref_date = datetime.datetime.strptime(self.reference_date, "%Y-%M-%d")
        doc = frappe.get_doc(
            {
                "doctype": "Journal Entry",
                "title": self.remarks,
                "accounts": accounts,
                "posting_date": self.posting_date,
                "user_remark": self.remarks,
                "grouped_journal_entries": self.name,
                "cheque_no": self.reference_number,
                "voucher_type": self.voucher_type,
                "cheque_date": ref_date,
            }
        )
        doc.insert()
        # self.save()
        todos = frappe.db.get_list(
            "ToDo",
            {
                "reference_type": "Grouped Journal Entries",
                "reference_name": self.name,
                "status": "Open",
            },
            ["allocated_to"],
        )
        allocates = []
        for row in todos:
            allocates.append(row.allocated_to)
        if allocates:
            add(
                {
                    "assign_to": allocates,
                    "doctype": "Journal Entry",
                    "name": doc.name,
                    "description": doc.user_remark,
                }
            )
        return doc.name

    def on_submit(self):
        self.validate_entries()
        JE_name = self.create_journal_entry()
        self.reference_journal = JE_name

    def on_cancel(self):
        if frappe.db.exists(
            "Journal Entry", {"grouped_journal_entries": self.name, "docstatus": 1}
        ):
            doc = frappe.get_doc(
                "Journal Entry", {"grouped_journal_entries": self.name}
            )
            doc.cancel()

        if frappe.db.exists(
            "Journal Entry", {"grouped_journal_entries": self.name, "docstatus": 0}
        ):
            doc = frappe.get_doc(
                "Journal Entry", {"grouped_journal_entries": self.name}
            )
            doc.delete()
