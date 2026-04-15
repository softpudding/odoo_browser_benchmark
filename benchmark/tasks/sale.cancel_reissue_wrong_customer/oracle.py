"""Oracle for sale.cancel_reissue_wrong_customer.

Find confirmed SO for Harbor Retail East with ref SALE-FIX-12.
Cancel it. Create new quotation for Harbor Retail West with same lines:
  - Counter Display qty 4 price 210
  - Shelf Signage Kit qty 7 price 48
Set Customer Reference to SALE-FIX-12-WEST. Confirm new order.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_button,
    click_create,
    click_list_row,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    modal_click_button,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the SO with ref SALE-FIX-12
    click_list_row(page, "SALE-FIX-12")
    page.wait_for_timeout(1000)

    # If the SO is locked, we need to unlock it first.
    unlock_btn = page.locator(
        "button[name='action_unlock']:visible, "
        "button:visible:has-text('Unlock')"
    )
    if unlock_btn.count() > 0:
        unlock_btn.first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    # Cancel the SO. The Cancel button has a `confirm` attribute which
    # triggers an Odoo ConfirmationDialog (NOT a native browser dialog).
    # We click Cancel, then confirm in the modal.
    cancel_btn = page.locator(
        "button[name='action_cancel']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Cancel')"
    ).first
    cancel_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Confirm the cancellation in the Odoo confirmation dialog
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        # Click Ok/Confirm button in the dialog
        modal.last.locator(
            "button:has-text('Ok'), "
            "button:has-text('Confirm'), "
            "button.btn-primary"
        ).first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)

    # Go back to sales list
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Create new quotation
    click_create(page)
    page.wait_for_timeout(1000)

    # Set customer to Harbor Retail West
    set_many2one(page, "partner_id", "Harbor Retail West")
    page.wait_for_timeout(500)

    # Add first line: Counter Display qty 4 price 210
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_template_id", "Counter Display")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "product_uom_qty", "4")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "210")
    page.wait_for_timeout(500)

    # Add second line: Shelf Signage Kit qty 7 price 48
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_template_id", "Shelf Signage Kit")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "product_uom_qty", "7")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "48")
    page.wait_for_timeout(500)

    # Set Customer Reference in Other Info tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "SALE-FIX-12-WEST")
    page.wait_for_timeout(500)

    # Confirm the new order
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Handle any confirmation dialog (e.g. "no email" warning)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        modal.last.locator(
            "button:has-text('Ok'), button:has-text('Confirm'), button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
