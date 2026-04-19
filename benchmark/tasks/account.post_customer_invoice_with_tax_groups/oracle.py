"""Oracle for account.post_customer_invoice_with_tax_groups.

Gates:
  1. Navigate Accounting > Customers > Invoices > New. Fill Customer,
     Invoice Date. Add exactly one invoice line: Bench Tax Service
     qty=1 price=200, and set the Taxes cell to the 'Bench Sale Tax 20%'
     many2many_tax_tags pill (NOT the 10% distractor). If a default tax
     pill got attached, remove it before adding the 20% one.
  2. Click Confirm in the statusbar to post the invoice.
"""

from benchmark.oracle_helpers import (
    click_status_button,
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


CUSTOMER_NAME = "Bench Tax Cust"
PRODUCT_NAME = "Bench Tax Service"
TAX_20_NAME = "Bench Sale Tax 20%"
TAX_10_NAME = "Bench Sale Tax 10%"


def _click_add_line(page):
    """Click 'Add a line' anchor in the invoice_line_ids list."""
    anchor = page.locator(
        ".o_field_one2many[name='invoice_line_ids'] a"
    ).filter(has_text="Add a line").first
    anchor.click()
    page.wait_for_timeout(800)


def _selected_row(page):
    return page.locator(
        ".o_form_view .o_list_renderer .o_data_row.o_selected_row"
    ).first


def _clear_tax_cell_on_selected_row(page):
    """Remove any existing tax pills from the selected row's Taxes cell."""
    row = _selected_row(page)
    tax_cell = row.locator("td[name='tax_ids']").first
    if tax_cell.count() == 0:
        return
    # Click into the cell to make it editable so pills are interactable.
    try:
        tax_cell.scroll_into_view_if_needed()
    except Exception:
        pass
    try:
        tax_cell.click()
        page.wait_for_timeout(300)
    except Exception:
        pass
    # Delete any x icons present.
    # many2many_tags renders each pill with a delete x (.o_delete).
    for _ in range(10):
        delete_icons = tax_cell.locator(
            ".o_delete, .o_tag .o_delete, .o_tag a.o_delete, "
            "button.o_delete, .badge .o_delete"
        )
        if delete_icons.count() == 0:
            break
        try:
            delete_icons.first.click()
            page.wait_for_timeout(200)
        except Exception:
            break


def _add_tax_tag_on_selected_row(page, tax_name):
    row = _selected_row(page)
    tax_cell = row.locator("td[name='tax_ids']").first
    try:
        tax_cell.scroll_into_view_if_needed()
    except Exception:
        pass
    tax_cell.click()
    page.wait_for_timeout(400)

    inp = tax_cell.locator("input").first
    inp.wait_for(state="visible", timeout=5000)
    inp.click()
    inp.fill("")
    inp.fill(tax_name)
    page.wait_for_timeout(900)

    dropdown = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete:visible .ui-menu-item"
    )
    # Pick the exact match -- the 20% option, not the 10% distractor.
    option = dropdown.filter(has_text=tax_name).first
    option.wait_for(state="visible", timeout=5000)
    option.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _add_invoice_line(page):
    _click_add_line(page)
    set_o2m_many2one(page, 0, "product_id", PRODUCT_NAME)
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "quantity", "1")
    page.wait_for_timeout(300)
    set_o2m_field(page, 0, "price_unit", "200.00")
    page.wait_for_timeout(500)

    # Remove any default tax that the product's onchange added (we
    # cleared taxes on the template in the seed, but be defensive).
    _clear_tax_cell_on_selected_row(page)
    page.wait_for_timeout(300)

    _add_tax_tag_on_selected_row(page, TAX_20_NAME)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # Gate 1: create invoice from scratch.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1200)
    _wait_for_ready(page)

    # Customer (partner_id)
    set_many2one(page, "partner_id", CUSTOMER_NAME)
    page.wait_for_timeout(500)

    # Invoice date.
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
        page.evaluate(
            "document.querySelectorAll('.o_datetime_picker, .o_popover, "
            ".o_daterange_picker').forEach(e => e.remove());"
        )
    page.wait_for_timeout(500)

    # Add the single product line with the 20% tax.
    _add_invoice_line(page)

    # Click outside to commit the line without auto-creating a blank row.
    try:
        page.locator(".o_form_sheet").first.click()
        page.wait_for_timeout(500)
    except Exception:
        pass
    _wait_no_loading(page)

    # Gate 2: post the invoice.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
