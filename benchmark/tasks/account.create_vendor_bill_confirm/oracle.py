"""Oracle for account.create_vendor_bill_confirm.

Navigate to vendor bills, create a new bill for Meridian Supply Co with
2 product lines, set bill date and reference, then confirm.
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
    _wait_no_loading,
    _wait_for_ready,
)


def _enable_product_column(page):
    """Toggle the Product column on in the invoice line list."""
    gear = page.locator(
        ".o_field_one2many[name='invoice_line_ids'] "
        ".o_optional_columns_dropdown_toggle"
    ).first
    gear.click()
    page.wait_for_timeout(500)

    product_item = page.locator(
        ".dropdown-menu:visible .dropdown-item"
    ).filter(has_text="Product").first
    # Only toggle if not already checked
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
    """Add a new product line at row index `row_idx`."""
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

    # Create new vendor bill — use the list's New button
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Set vendor
    set_many2one(page, "partner_id", "Meridian Supply Co")
    page.wait_for_timeout(500)

    # Set bill reference
    fill_field(page, "ref", "MSC-INV-4421")
    page.wait_for_timeout(500)

    # Set bill date (invoice_date) — renders as date button in Odoo 19
    try:
        set_date(page, "invoice_date", "05/01/2026")
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
        dp.type("05/01/2026")
        dp.press("Enter")
        page.wait_for_timeout(300)
        page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Product column is hidden by default — enable it so we can set product_id
    _enable_product_column(page)

    # Add first line: Cable Tray × 100 @ 12.50
    _add_line(page, 0, "Cable Tray", "100", "12.50")

    # Add second line: Junction Box × 50 @ 8.00
    _add_line(page, 1, "Junction Box", "50", "8.00")

    # Click outside to commit lines
    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Confirm the bill
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
