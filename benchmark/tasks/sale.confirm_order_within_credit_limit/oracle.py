"""Oracle for sale.confirm_order_within_credit_limit.

Create a new quotation for Atlas Field Systems with an expiration date and the
credit-compliant final quantities, send it by email with the required content,
then confirm it.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_add_a_line,
    click_create,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    save_form,
    set_date,
    set_o2m_field,
    set_o2m_many2one,
    run_oracle,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    clear_search_filters(page)
    page.wait_for_timeout(500)
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    set_many2one(page, "partner_id", "Atlas Field Systems")
    page.wait_for_timeout(500)

    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_template_id", "Field Router Kit")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "product_uom_qty", "3")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "400")
    page.wait_for_timeout(500)

    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_template_id", "On-site Commissioning")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "product_uom_qty", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "1100")
    page.wait_for_timeout(500)

    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "CREDIT-OPS-09")
    page.wait_for_timeout(500)
    set_date(page, "validity_date", "05/22/2026")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_status_button(page, "Send")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    recipient_input = modal.locator(
        ".o_field_widget[name='partner_ids'] input"
    ).last
    recipient_input.click()
    recipient_input.fill("creditdesk@atlas-field.example.com")
    page.wait_for_timeout(1000)
    recipient_item = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text="creditdesk@atlas-field.example.com").first
    recipient_item.click()
    page.wait_for_timeout(500)

    subject = modal.locator(".o_field_widget[name='subject'] input").first
    subject.click()
    subject.fill("")
    subject.fill("Atlas credit-cleared quotation")
    subject.press("Tab")
    page.wait_for_timeout(500)

    body = modal.locator(
        ".o_field_widget[name='body'] .odoo-editor-editable, "
        ".o_field_widget[name='body'] [contenteditable='true']"
    ).first
    body.click()
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.wait_for_timeout(200)
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    page.keyboard.insert_text(
        "Please review the adjusted quotation within the remaining credit allowance."
    )
    page.wait_for_timeout(500)
    body.press("Tab")
    page.wait_for_timeout(300)

    modal.locator("button:has-text('Send')").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
