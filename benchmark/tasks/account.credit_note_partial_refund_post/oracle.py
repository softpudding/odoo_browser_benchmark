"""Oracle for account.credit_note_partial_refund_post.

Open posted invoice INV/BENCH/001 for Bench AR Co, open the Reverse
wizard (labeled "Credit Note" on the invoice header), fill the reason
"Wrong qty", leave the default (today) date, click "Reverse" (the
primary refund_moves button — NOT "Reverse and Create Invoice"), then
on the generated draft credit note change Bench Item A qty from 4 to 2,
delete the Bench Item B line, and post the credit note via the header
Confirm button.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    modal_click_button,
    modal_fill_field,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Open the posted invoice
    click_list_row(page, "INV/BENCH/001")
    page.wait_for_timeout(1200)

    # The invoice-level reversal button is labeled "Credit Note" in the
    # statusbar (it opens the account.move.reversal wizard).
    click_status_button(page, "Credit Note")
    page.wait_for_timeout(1200)

    # Fill the reason; leave reversal date at today's default.
    modal_fill_field(page, "reason", "Wrong qty")
    page.wait_for_timeout(400)

    # Primary-action button in the wizard footer is "Reverse"
    # (refund_moves). "Reverse and Create Invoice" (modify_moves) is the
    # secondary alternative and MUST NOT be clicked.
    modal = page.locator(".modal:visible").last
    reverse_btn = modal.locator(
        "button.btn-primary[name='refund_moves']"
    ).first
    if reverse_btn.count() == 0:
        # Fallback: match by visible text, but prefer the exact-match
        # button so "Reverse and Create Invoice" is not picked.
        buttons = modal.locator("footer button")
        for i in range(buttons.count()):
            b = buttons.nth(i)
            if b.inner_text().strip() == "Reverse":
                reverse_btn = b
                break
    reverse_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # We are now on the draft credit note (out_refund) with both source
    # lines copied over. Delete the Bench Item B row first.
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    row_count = rows.count()
    if row_count == 0:
        rows = page.locator(".o_list_view .o_data_row")
        row_count = rows.count()

    deleted = False
    for i in range(row_count):
        row = rows.nth(i)
        text = row.inner_text()
        if "Bench Item B" in text:
            delete_btn = row.locator(
                ".o_list_record_remove, "
                "button.o_list_record_remove, "
                ".fa-trash-o, "
                ".o_list_record_delete, "
                "td.o_list_record_remove button, "
                "i.fa-trash-o"
            )
            if delete_btn.count() > 0:
                delete_btn.first.click()
            else:
                trash = row.locator("td:last-child button, td:last-child i")
                if trash.count() > 0:
                    trash.first.click()
            deleted = True
            page.wait_for_timeout(900)
            _wait_no_loading(page)
            break

    if not deleted:
        raise AssertionError("Could not locate Bench Item B row to delete")

    # Now update Bench Item A qty from 4 to 2. After deleting Item B, the
    # remaining row should be Item A.
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    if rows.count() == 0:
        rows = page.locator(".o_list_view .o_data_row")

    target_row = None
    for i in range(rows.count()):
        row = rows.nth(i)
        if "Bench Item A" in row.inner_text():
            target_row = row
            break
    if target_row is None:
        raise AssertionError("Could not locate Bench Item A row after deleting B")

    qty_cell = target_row.locator("td[name='quantity']").first
    qty_cell.click()
    page.wait_for_timeout(400)
    qty_input = qty_cell.locator("input").first
    qty_input.fill("")
    qty_input.fill("2")
    qty_input.press("Tab")
    page.wait_for_timeout(900)
    _wait_no_loading(page)

    # Post the credit note via the header Confirm button.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
