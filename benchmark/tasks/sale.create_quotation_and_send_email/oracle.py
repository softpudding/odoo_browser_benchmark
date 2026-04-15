"""Oracle for sale.create_quotation_and_send_email.

Create new quotation for Riverton Supply Co with lines:
  - Industrial Fan qty 6 price 185
  - Air Filter Cartridge qty 12 price 45
Set Expiration Date to 05/15/2026. Save. Send by Email.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_status_button,
    click_tab,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Create new quotation
    click_create(page)
    page.wait_for_timeout(1000)

    # Set customer
    set_many2one(page, "partner_id", "Riverton Supply Co")
    page.wait_for_timeout(500)

    # Add first line: Industrial Fan qty 6 price 185
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_template_id", "Industrial Fan")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "product_uom_qty", "6")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "185")
    page.wait_for_timeout(500)

    # Add second line: Air Filter Cartridge qty 12 price 45
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_template_id", "Air Filter Cartridge")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "product_uom_qty", "12")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "45")
    page.wait_for_timeout(500)

    # Set Expiration Date via the calendar date picker
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    vd_widget = page.locator(".o_field_widget[name='validity_date']").first
    vd_btn = vd_widget.locator("button, .o_input").first
    vd_btn.click()
    page.wait_for_timeout(500)
    # Click the day "15" in the calendar picker
    picker = page.locator(".o_popover:visible .o_datetime_picker").first
    day_15 = picker.locator(".o_date_item_cell:has-text('15'):not(.o_out_of_range)")
    day_15.first.click()
    page.wait_for_timeout(300)
    # Apply
    apply_btn = page.locator(".o_popover:visible button:has-text('Apply')")
    if apply_btn.count() > 0:
        apply_btn.first.click()
    page.wait_for_timeout(300)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # Save the form
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click Send button
    click_status_button(page, "Send")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # In the compose wizard / send dialog, click Send
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator("button:has-text('Send')").first.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)


run_oracle(oracle)
