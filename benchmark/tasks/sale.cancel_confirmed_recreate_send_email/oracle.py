"""Oracle for sale.cancel_confirmed_recreate_send_email.

Cancel confirmed SO with ref BENCH-CANCEL-RESEND for Ironwood Distribution.
Create a new quotation for Clearwater Supply Co with:
  - Heavy-Duty Shelf Unit qty 8 price 145
  - Packing Tape Industrial qty 200 price 3.50
Set Customer Reference to CWS-REPLACE-01, Expiration to 07/15/2026.
Save. Send by Email with subject "Clearwater Supply - Replacement Order Proposal".
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_list_row,
    click_status_button,
    click_tab,
    clear_search_filters,
    fill_field,
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
    page.wait_for_timeout(1000)

    # Clear "My Quotations" filter so we can see all orders
    clear_search_filters(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Find and open the confirmed SO with ref BENCH-CANCEL-RESEND
    click_list_row(page, "BENCH-CANCEL-RESEND")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Cancel the SO
    cancel_btn = page.locator(
        "button[name='action_cancel']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Cancel')"
    ).first
    cancel_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Confirm the cancellation in the Odoo confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), "
            "button:has-text('Confirm'), "
            "button.btn-primary"
        ).first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)

    # Navigate back to sales list
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Clear filters again
    clear_search_filters(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Create new quotation
    click_create(page)
    page.wait_for_timeout(1500)

    # Set customer to Clearwater Supply Co
    set_many2one(page, "partner_id", "Clearwater Supply Co")
    page.wait_for_timeout(1000)

    # Add first line: Heavy-Duty Shelf Unit qty 8 price 145
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_template_id", "Heavy-Duty Shelf Unit")
    page.wait_for_timeout(800)
    set_o2m_field(page, 0, "product_uom_qty", "8")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "145")
    page.wait_for_timeout(500)

    # Add second line: Packing Tape Industrial qty 200 price 3.50
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_template_id", "Packing Tape Industrial")
    page.wait_for_timeout(800)
    set_o2m_field(page, 1, "product_uom_qty", "200")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "3.50")
    page.wait_for_timeout(500)

    # Set Customer Reference in Other Info tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "CWS-REPLACE-01")
    page.wait_for_timeout(500)

    # Set Expiration Date to 07/15/2026
    set_date(page, "validity_date", "07/15/2026")
    page.wait_for_timeout(500)

    # Save the form
    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click Send by Email / Send button
    click_status_button(page, "Send")
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # In the email compose wizard, set subject and send
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # Set the subject
        subject = modal.last.locator(
            ".o_field_widget[name='subject'] input"
        ).first
        subject.click()
        subject.fill("")
        subject.fill("Clearwater Supply - Replacement Order Proposal")
        subject.press("Tab")
        page.wait_for_timeout(1000)

        # Click Send in the modal
        modal.last.locator("button:has-text('Send')").first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
