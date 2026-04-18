"""Oracle for event_product.create_event_product_link_to_ticket.

Two-part workflow:
  1. Inventory > Products > New: create 'Conference Pass Std' as a
     Service product, list_price=100, service_tracking='event'
     ('Event Registration' option).
  2. Events > 'Spring Summit' > Tickets tab > Add a line: pick the
     product, set name='Standard Pass', price=100, seats_max=200.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


EVENT_NAME = "Spring Summit"
PRODUCT_NAME = "Conference Pass Std"
TICKET_NAME = "Standard Pass"


def _clear_filters(page):
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break


def _switch_to_list(page):
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)


def _click_add_a_line(page):
    add_link = page.locator(
        "a.o_field_x2many_list_row_add:visible, "
        "td.o_field_x2many_list_row_add a:visible"
    )
    add_link.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _set_product_type_service(page):
    """The product type is a radio-like selection. Pick 'Service'."""
    # In Odoo 19, type is rendered as a selection with options. Try a
    # selectOption first, then fall back to dropdown click.
    selector = ".o_field_widget[name='type'] select"
    select_loc = page.locator(selector)
    if select_loc.count() > 0:
        try:
            select_loc.first.select_option(value="service")
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            return
        except Exception:
            pass
    # Fallback: open the radio/badge group.
    radio = page.locator(
        ".o_field_widget[name='type'] input[type='radio'][data-value='service'], "
        ".o_field_widget[name='type'] label:has-text('Service')"
    )
    if radio.count() > 0:
        radio.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)


def _set_service_tracking_event(page):
    """The service_tracking selection. 'event' option label is
    'Event Registration'."""
    selector = ".o_field_widget[name='service_tracking'] select"
    select_loc = page.locator(selector)
    if select_loc.count() > 0:
        try:
            select_loc.first.select_option(value="event")
            page.wait_for_timeout(500)
            _wait_no_loading(page)
            return
        except Exception:
            pass
    # Fallback: it might be rendered as a dropdown with text.
    dropdown_btn = page.locator(
        ".o_field_widget[name='service_tracking'] input"
    )
    if dropdown_btn.count() > 0:
        dropdown_btn.first.click()
        page.wait_for_timeout(400)
        page.locator(
            ".dropdown-menu .dropdown-item:has-text('Event Registration')"
        ).first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)


def oracle(page):
    # ============================================================
    # STEP 1 — Create the product
    # ============================================================
    login(page)
    # Navigate to Products list. The Products menu xmlid action is
    # accessible via /odoo/inventory/products and /odoo/action-..., but
    # the simplest cross-app path is the inventory products list.
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Click the Products top-level menu item.
    products_menu = page.locator(
        ".o_navbar button[data-menu-xmlid$='products_menu']:visible, "
        ".o_navbar a[data-menu-xmlid$='products_menu']:visible, "
        ".o_navbar_apps_menu_section button:has-text('Products'):visible, "
        ".o_main_navbar button:has-text('Products'):visible"
    )
    if products_menu.count() > 0:
        products_menu.first.click()
        page.wait_for_timeout(500)
        sub = page.locator(
            ".o_menu_brand_dropdown_item:has-text('Products'), "
            ".dropdown-item:has-text('Products')"
        )
        # Click the deepest "Products" leaf.
        if sub.count() > 0:
            sub.last.click()
            page.wait_for_timeout(800)
    # Fallback: navigate via URL.
    if page.locator(".o_breadcrumb").locator("text=Products").count() == 0:
        navigate(page, "/odoo/inventory/products")
        _wait_no_loading(page)
        page.wait_for_timeout(800)

    _wait_for_ready(page)

    # Click New (top-left).
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel_main_buttons button:has-text('New'):visible"
    )
    new_btn.first.click()
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Fill product name (the form has a Char field "name" prominent at top).
    name_inp = page.locator(
        "input[id^='name'][type='text']:visible, "
        ".o_field_widget[name='name'] input:visible, "
        ".o_field_widget[name='name'] textarea:visible"
    )
    name_inp.first.click()
    name_inp.first.fill(PRODUCT_NAME)
    page.wait_for_timeout(300)

    # Set the product type to Service.
    _set_product_type_service(page)
    page.wait_for_timeout(400)

    # Set the service tracking to Event Registration ('event').
    _set_service_tracking_event(page)
    page.wait_for_timeout(400)

    # Set the sales price.
    list_price_inp = page.locator(
        ".o_field_widget[name='list_price'] input:visible"
    )
    list_price_inp.first.click()
    list_price_inp.first.fill("")
    list_price_inp.first.fill("100.00")
    list_price_inp.first.press("Tab")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ============================================================
    # STEP 2 — Add the ticket on the event
    # ============================================================
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    _clear_filters(page)
    _switch_to_list(page)
    page.wait_for_timeout(500)

    click_list_row(page, EVENT_NAME)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    click_tab(page, "Tickets")
    page.wait_for_timeout(500)

    _click_add_a_line(page)
    # New row in the event_ticket_ids one2many list.
    set_o2m_many2one(page, 0, "product_id", PRODUCT_NAME)
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "name", TICKET_NAME)
    set_o2m_field(page, 0, "price", "100")
    set_o2m_field(page, 0, "seats_max", "200")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
