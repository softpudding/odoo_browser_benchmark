"""Oracle for delivery.configure_carrier_margin_rule_apply_to_order."""
from benchmark.oracle_helpers import (
    click_add_a_line,
    click_button,
    click_create,
    click_list_row,
    click_status_button,
    click_tab,
    fill_field,
    login,
    modal_click_button,
    modal_fill_field,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
)

def select_menu(page, field_name, value, *, modal=False):
    scope = page.locator(".modal:visible").last if modal else page
    widget = scope.locator(f".o_field_widget[name='{field_name}']").first
    inp = widget.locator("input.o_select_menu_input, input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    page.wait_for_timeout(500)
    page.locator(
        ".o-overlay-container .dropdown-item, .dropdown-menu .dropdown-item"
    ).filter(has_text=value).first.click()
    page.wait_for_timeout(500)


def oracle(page):
    login(page)
    navigate(page, "/odoo/delivery-methods")
    click_create(page)
    fill_field(page, "name", "Bench Margin Courier")
    select_menu(page, "delivery_type", "Based on Rules")
    set_many2one(page, "product_id", "Bench Margin Shipping")
    fill_field(page, "fixed_margin", "6.00")
    click_tab(page, "Pricing")
    click_add_a_line(page)
    select_menu(page, "variable", "Weight", modal=True)
    select_menu(page, "operator", "<=", modal=True)
    modal_fill_field(page, "max_value", "10")
    modal_fill_field(page, "list_base_price", "12.00")
    modal_fill_field(page, "list_price", "0")
    select_menu(page, "variable_factor", "Weight", modal=True)
    modal_click_button(page, "Save")
    save_form(page)

    navigate(page, "/odoo/sales")
    click_list_row(page, "MARGIN-DEL-01")
    click_button(page, "Add shipping")
    set_many2one(page, "carrier_id", "Bench Margin Courier")
    modal_click_button(page, "Add")
    click_status_button(page, "Confirm")

run_oracle(oracle)
