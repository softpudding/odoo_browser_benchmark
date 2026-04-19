"""Oracle for delivery.country_rule_and_free_threshold_apply_to_so."""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    add_many2many_tag,
    clear_search_filters,
    click_button,
    click_create,
    click_list_row,
    click_tab,
    click_status_button,
    ensure_list_view,
    fill_field,
    login,
    modal_set_many2one,
    navigate,
    run_oracle,
    save_form,
    set_boolean,
    set_many2one,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/delivery-methods")
    _wait_no_loading(page)
    ensure_list_view(page)
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    fill_field(page, "name", "US Harbor Freight")
    set_boolean(page, "free_over", True)
    fill_field(page, "amount", "100.00")
    set_many2one(page, "product_id", "US Harbor Shipping")
    fixed_price = page.locator(".o_field_widget[name='fixed_price'] input").first
    fixed_price.click(force=True)
    fixed_price.press("Control+a")
    fixed_price.press("Backspace")
    fixed_price.fill("15")
    fixed_price.press("Tab")
    page.wait_for_timeout(400)

    click_tab(page, "Availability")
    page.wait_for_timeout(500)
    add_many2many_tag(page, "country_ids", "United States")

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(800)
    click_list_row(page, "Bench US Customer")
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    page.get_by_text("Add shipping", exact=True).click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    page.wait_for_selector(".modal:visible", timeout=10000)
    modal_set_many2one(page, "carrier_id", "US Harbor Freight")
    page.wait_for_timeout(500)
    page.locator(
        ".modal:visible .modal-footer button:has-text('Add'), "
        ".modal:visible .modal-footer button.btn-primary"
    ).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
