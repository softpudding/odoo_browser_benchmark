"""Oracle for website_sale.publish_shop_product."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/ecommerce-products")
    _wait_no_loading(page)

    click_list_row(page, "Shop Special Chair")
    _wait_no_loading(page)

    fill_field(page, "list_price", "199.00")
    click_tab(page, "Sales")
    _wait_no_loading(page)

    desc = page.locator(
        ".o_field_widget[name='description_ecommerce'] .note-editable, "
        ".o_field_widget[name='description_ecommerce'] .odoo-editor-editable, "
        ".o_field_widget[name='description_ecommerce'] [contenteditable='true']"
    ).first
    desc.click()
    page.keyboard.press("Meta+a")
    page.keyboard.type("Ergonomic task chair ready for the online shop.")
    page.wait_for_timeout(300)

    publish_toggle = page.locator(".o_field_widget[name='is_published'] input[type='checkbox']").last
    if publish_toggle.count() > 0 and not publish_toggle.is_checked():
        publish_toggle.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
