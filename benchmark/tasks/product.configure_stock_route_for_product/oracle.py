"""Oracle for product.configure_stock_route_for_product.

Flow:
    1. Navigate to Inventory > Products.
    2. Search for 'Bench MTO Item', open it.
    3. Click the Inventory notebook tab on the product form.
    4. Locate the Routes many2many_checkboxes field in the Operations group
       and tick the checkbox labelled 'Replenish on Order (MTO)'.
    5. Save.

Selector notes (Odoo 19):
    * Routes field is ``<field name="route_ids" widget="many2many_checkboxes">``
      rendered inside ``<group name="operations">`` on the Inventory tab.
      Each route renders as a label/checkbox pair — we locate the
      checkbox by scoping to the widget wrapper and filtering by the
      adjacent label text.
    * The MTO route's stored name is exactly
      'Replenish on Order (MTO)'.
    * Saving via the top breadcrumb save button (``.o_form_button_save``).
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    ensure_list_view,
    full_url,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
    _wait_for_ready,
    _wait_no_loading,
)


PRODUCT_NAME = "Bench MTO Item"
ROUTE_LABEL = "Replenish on Order (MTO)"


def _open_products_list(page):
    page.goto(
        full_url("/odoo/action-stock.product_template_action_product"),
        timeout=60000,
    )
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _open_product(page, name):
    try:
        ensure_list_view(page)
    except Exception:
        pass
    page.wait_for_timeout(300)
    # Try clicking directly in a list/kanban first; fall back to search.
    rec = page.locator(
        f".o_list_view .o_data_row:has-text('{name}'), "
        f".o_kanban_record:has-text('{name}')"
    ).first
    if rec.count() == 0 or not rec.is_visible():
        search_for(page, name)
        page.wait_for_timeout(500)
        _wait_no_loading(page)
        rec = page.locator(
            f".o_list_view .o_data_row:has-text('{name}'), "
            f".o_kanban_record:has-text('{name}')"
        ).first
    rec.wait_for(state="visible", timeout=15000)
    rec.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(700)
    _wait_no_loading(page)


def _switch_to_inventory_tab(page):
    # Robust tab selection — name='inventory' is the notebook page name.
    tab = page.locator(
        ".o_notebook a.nav-link[name='inventory']:visible, "
        ".o_notebook .nav-link[name='inventory']:visible"
    ).first
    if tab.count() > 0 and tab.is_visible():
        tab.click()
    else:
        # Fallback: click by visible text 'Inventory'.
        click_tab(page, "Inventory")
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _tick_route_checkbox(page, label):
    # Scope to the m2m_checkboxes widget named route_ids.
    widget = page.locator(
        ".o_field_widget[name='route_ids']"
    ).first
    widget.wait_for(state="visible", timeout=10000)
    widget.scroll_into_view_if_needed()
    page.wait_for_timeout(200)

    # m2m_checkboxes renders one <div class="form-check"> per available
    # route with a <label> whose text is the route name.  Find the
    # matching row by label text and click its input[type=checkbox].
    row = widget.locator(
        f".form-check:has(label:has-text('{label}')), "
        f".o_checkbox_optional_field:has(label:has-text('{label}'))"
    ).first
    if row.count() == 0:
        # Fallback: try the generic structure — a label immediately
        # preceded by the input checkbox.
        row = widget.locator(f"label:has-text('{label}')").first.locator(
            "xpath=.."
        )
    row.wait_for(state="visible", timeout=5000)

    cb = row.locator("input[type='checkbox']").first
    cb.wait_for(state="attached", timeout=5000)
    if not cb.is_checked():
        # Clicking the input is the most reliable — some themes put
        # pointer-events on the label.
        try:
            cb.check()
        except Exception:
            label_el = row.locator(f"label:has-text('{label}')").first
            label_el.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)

    _open_products_list(page)
    _open_product(page, PRODUCT_NAME)

    _switch_to_inventory_tab(page)
    _tick_route_checkbox(page, ROUTE_LABEL)

    save_form(page)
    page.wait_for_timeout(600)
    _wait_no_loading(page)


run_oracle(oracle)
