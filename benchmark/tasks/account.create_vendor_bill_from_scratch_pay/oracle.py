"""Oracle for account.create_vendor_bill_from_scratch_pay.

Three sequential gates:
  1. Navigate Accounting > Vendors > Bills > New. Fill Vendor,
     Bill Date, Bill Reference. Enable the Product column on the
     invoice-line list (hidden by default on vendor bill forms), add
     a single product line (Bench Bill Item qty=2 price=75).
  2. Click Confirm in the statusbar to post the bill.
  3. Click Pay in the statusbar to open the account.payment.register
     wizard, then click the primary Create Payment button (accept all
     defaults). Do NOT click Discard.
"""

from benchmark.oracle_helpers import (
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


def _enable_product_column(page):
    """Toggle the Product optional column on in the invoice line list."""
    gear = page.locator(
        ".o_field_one2many[name='invoice_line_ids'] "
        ".o_optional_columns_dropdown_toggle"
    ).first
    if gear.count() == 0:
        return
    gear.click()
    page.wait_for_timeout(500)

    product_item = page.locator(
        ".dropdown-menu:visible .dropdown-item"
    ).filter(has_text="Product").first
    checkbox = product_item.locator("input[type='checkbox']")
    if checkbox.count() == 0 or not checkbox.first.is_checked():
        product_item.click()
        page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    _wait_no_loading(page)


def _click_add_line(page):
    """Click 'Add a line' anchor in the invoice_line_ids list."""
    anchor = page.locator(
        ".o_field_one2many[name='invoice_line_ids'] a"
    ).filter(has_text="Add a line").first
    anchor.click()
    page.wait_for_timeout(800)


def _add_line(page, row_idx: int, product: str, qty: str, price: str) -> None:
    """Add a product line at row index `row_idx`."""
    _click_add_line(page)
    set_o2m_many2one(page, row_idx, "product_id", product)
    page.wait_for_timeout(500)
    set_o2m_field(page, row_idx, "quantity", qty)
    page.wait_for_timeout(300)
    set_o2m_field(page, row_idx, "price_unit", price)
    page.wait_for_timeout(500)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/vendor-bills")
    _wait_no_loading(page)

    # ----- Gate 1: create the bill from scratch -----
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Vendor (partner_id)
    set_many2one(page, "partner_id", "Bench Bill Vendor")
    page.wait_for_timeout(500)

    # Bill Reference (ref)
    fill_field(page, "ref", "BENCH-VBILL-001")
    page.wait_for_timeout(500)

    # Bill Date (invoice_date) — renders as a date button in Odoo 19.
    try:
        set_date(page, "invoice_date", "05/10/2026")
    except Exception:
        btn = page.locator(
            ".o_field_widget[name='invoice_date'] button"
        ).first
        btn.click()
        page.wait_for_timeout(500)
        dp = page.locator(
            ".o_datetime_picker:visible input.o_datetime_input, "
            ".o_datetime_picker:visible input"
        ).first
        dp.click(click_count=3)
        dp.fill("")
        dp.type("05/10/2026")
        dp.press("Enter")
        page.wait_for_timeout(300)
        # Only dismiss the datepicker overlay, never the modal/form.
        page.evaluate(
            "document.querySelectorAll('.o_datetime_picker, .o_popover, "
            ".o_daterange_picker').forEach(e => e.remove());"
        )
    page.wait_for_timeout(500)

    # Product column is hidden by default on the vendor bill form.
    _enable_product_column(page)

    # Add the single product line: Bench Bill Item × 2 @ 75.00
    _add_line(page, 0, "Bench Bill Item", "2", "75.00")

    # Click outside (onto the form sheet) to commit the line without
    # auto-creating a second blank row.
    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # ----- Gate 2: post the bill -----
    click_status_button(page, "Confirm")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # ----- Gate 3: pay in full via the Register Payment wizard -----
    # Statusbar button text is "Pay" (the action is named
    # `action_register_payment`).
    pay_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Pay'):visible, "
        ".o_statusbar_buttons button:has-text('Register Payment'):visible"
    ).first
    pay_btn.click(force=True)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(1000)

    # Click the primary "Create Payment(s)" button. The button name is
    # action_create_payments regardless of singular/plural label.
    modal = page.locator(".modal:visible").last
    create_btn = modal.locator(
        "button.btn-primary[name='action_create_payments']"
    ).first
    if create_btn.count() == 0:
        # Fallback: any primary footer button labelled Create Payment(s).
        footer = modal.locator("footer, .modal-footer").first
        buttons = footer.locator("button.btn-primary")
        picked = None
        for i in range(buttons.count()):
            b = buttons.nth(i)
            try:
                t = b.inner_text().strip()
            except Exception:
                continue
            if t in ("Create Payment", "Create Payments"):
                picked = b
                break
        if picked is None and buttons.count() > 0:
            picked = buttons.first
        if picked is None:
            raise AssertionError(
                "Could not locate primary Create Payment button in wizard"
            )
        create_btn = picked

    create_btn.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)


run_oracle(oracle)
