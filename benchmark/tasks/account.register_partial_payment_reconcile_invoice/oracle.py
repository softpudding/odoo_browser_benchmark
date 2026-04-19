"""Oracle for account.register_partial_payment_reconcile_invoice.

Open the posted invoice BENCH-PARTIAL-001 for Bench Partial Co (NOT
the distractor BENCH-PARTIAL-DISTRACT), click the statusbar Pay
button to open the account.payment.register wizard, then OVERRIDE four
auto-filled wizard fields (the seed wires a 'Bench Secondary Bank'
journal with lower sequence so it wins the default pick):
  - Journal: 'Bench Secondary Bank' (default) -> 'Bank'
  - Amount: 500.00 (default) -> 200.00
  - Payment Date: today (default) -> 04/15/2026
  - Memo: 'INV/2026/NNN' (default) -> 'Partial 1 of 2 for BENCH-PARTIAL-001'
Order matters: Journal -> Amount -> Date -> Memo. Memo must be LAST or
later onchanges overwrite it. Finally click the primary
'Create Payment' button.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Open the TARGET posted invoice (not the distractor).
    click_list_row(page, "BENCH-PARTIAL-001")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click Pay in the header (Register Payment) to open the wizard.
    pay_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Pay'):visible"
    )
    pay_btn.first.click(force=True)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(1200)

    modal = page.locator(".modal:visible").last

    # Override the Journal first — changing journal can reset Amount and
    # other fields via onchange, so do this BEFORE Amount/Memo.
    journal_widget = modal.locator(
        ".o_field_widget[name='journal_id']"
    ).first
    journal_input = journal_widget.locator("input").first
    journal_input.click()
    journal_input.press("Control+a")
    journal_input.press("Delete")
    journal_input.fill("")
    journal_input.fill("Bank")
    page.wait_for_timeout(800)
    # Click the dropdown entry whose text is exactly 'Bank' (not
    # 'Bench Secondary Bank' which also contains 'Bank').
    dropdown = page.locator(".dropdown-menu:visible .dropdown-item")
    clicked = False
    for i in range(dropdown.count()):
        item_text = dropdown.nth(i).inner_text().strip()
        if item_text == "Bank":
            dropdown.nth(i).click()
            clicked = True
            break
    if not clicked:
        # Fallback: first dropdown whose text equals 'Bank' with any
        # whitespace around it.
        bank_only = page.locator(
            ".dropdown-menu:visible .dropdown-item"
        ).filter(has_text="Bank")
        # Pick shortest-text entry (most likely "Bank" vs. "Bench Secondary Bank")
        best = None
        best_len = 10**9
        for i in range(bank_only.count()):
            txt = bank_only.nth(i).inner_text().strip()
            if txt and len(txt) < best_len and txt == "Bank":
                best_len = len(txt)
                best = bank_only.nth(i)
        if best is not None:
            best.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Override the auto-filled Amount -> 200.00.
    modal = page.locator(".modal:visible").last
    amount_widget = modal.locator(
        ".o_field_widget[name='amount']"
    ).first
    amount_input = amount_widget.locator("input").first
    amount_input.click(force=True)
    amount_input.press("Control+a")
    amount_input.press("Delete")
    amount_input.fill("")
    amount_input.fill("200.00")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # Back-date Payment Date to 04/15/2026 BEFORE the memo override —
    # changing payment_date can re-compute communication via onchange.
    modal = page.locator(".modal:visible").last
    date_widget = modal.locator(".o_field_widget[name='payment_date']").first
    date_btn = date_widget.locator("button").first
    date_btn.click(force=True)
    page.wait_for_timeout(600)

    # The datepicker overlay now contains an input; type into active elem.
    page.keyboard.press("Control+a")
    page.keyboard.press("Delete")
    page.keyboard.type("04/15/2026")
    page.wait_for_timeout(400)
    # Remove ONLY the datepicker overlay (keep the modal). The modal
    # itself is an .o-overlay-item, so we must NOT blanket-remove all
    # .o-overlay-item. Target only the datepicker popover by class.
    page.evaluate(
        "document.querySelectorAll('.o_datetime_picker, .o_popover, .o_daterange_picker').forEach(e => e.remove());"
    )
    page.wait_for_timeout(400)

    # Memo LAST so no subsequent onchange can overwrite it.
    modal = page.locator(".modal:visible").last
    memo_widget = modal.locator(
        ".o_field_widget[name='communication']"
    ).first
    memo_input = memo_widget.locator("input, textarea").first
    memo_input.click(force=True)
    memo_input.press("Control+a")
    memo_input.press("Delete")
    memo_input.fill("")
    memo_input.fill("Partial 1 of 2 for BENCH-PARTIAL-001")
    # Blur the field to commit without Tab (Tab could advance focus
    # and trigger re-renders).
    memo_input.press("Enter")
    page.wait_for_timeout(500)

    # Click the primary "Create Payment" button (name=action_create_payments).
    modal = page.locator(".modal:visible").last
    create_btn = modal.locator(
        "button.btn-primary[name='action_create_payments']"
    ).first
    if create_btn.count() == 0:
        buttons = modal.locator("footer button")
        for i in range(buttons.count()):
            b = buttons.nth(i)
            text = b.inner_text().strip()
            if text in ("Create Payment", "Create Payments"):
                create_btn = b
                break
    create_btn.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)


run_oracle(oracle)
