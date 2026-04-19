"""Oracle for stock.run_manual_replenishment_for_product.

Flow:
  1. Login, navigate to /odoo/replenishment (the server action's
     path is `replenishment`; `ir.actions.server` id
     `stock.action_replenishment` injects
     `search_default_filter_to_reorder=True,
      search_default_filter_not_snoozed=True,
      default_trigger='manual',
      searchpanel_default_trigger='manual'`).
  2. Filter / search for "Bench Replenish Item".
  3. Click the per-row Order button (`button[name='action_replenish']`
     with class `o_replenish_buttons`, icon `fa-truck`). This fires
     `stock.warehouse.orderpoint.action_replenish` on that single
     record, which generates a draft `purchase.order` for the vendor
     through `stock.rule._run_buy`.
  4. Handle any confirmation modal that may appear (none in default
     flow — action_replenish returns a client notification action, not
     a wizard, unless the product has no vendor price which won't
     happen here).

UI quirks:
  * The Replenishment dashboard is distinct from Reordering Rules: the
    editable list view `view_warehouse_orderpoint_tree_editable` is
    loaded by action `stock.action_orderpoint_replenish`. Only this
    view renders the `.o_replenish_buttons` column (Order / Automate
    icons), and only when `qty_to_order > 0.0`. The Reordering Rules
    menu loads `view_warehouse_orderpoint_tree_editable_show_trigger`
    which hides those buttons.
  * Default filter "To Reorder" (qty_to_order > 0) keeps only actionable
    rows. Since our seed yields qty_to_order = 20 > 0, the row appears.
  * The list default context trigger filter is `manual` via
    `searchpanel_default_trigger='manual'` — with seed trigger='manual'
    the row is in the expected facet.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)

PRODUCT_NAME = "Bench Replenish Item"


def _search_for_product(page):
    sb = page.locator(".o_searchview_input").first
    sb.click()
    sb.fill(PRODUCT_NAME)
    page.wait_for_timeout(600)
    # Press Enter — the Product column is visible and the searchview
    # autocomplete resolves to product_id (the standard field on the
    # `stock_reorder_report_search` search view).
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    _wait_no_loading(page)


def _click_order_on_row(page):
    # Wait for the list row to materialise.
    row = page.locator(
        f".o_list_view .o_data_row:has-text('{PRODUCT_NAME}')"
    ).first
    row.wait_for(state="visible", timeout=15000)

    # Find the fa-truck "Order" button on that row. It's a <button> with
    # name=action_replenish and class `o_replenish_buttons`. Prefer the
    # more specific locator.
    btn = row.locator(
        "button[name='action_replenish'].o_replenish_buttons, "
        "button[name='action_replenish']"
    ).first
    btn.wait_for(state="visible", timeout=15000)
    btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # If any confirmation/wizard modal appears, accept the primary
    # button (default flow issues only a client notification, but guard
    # against future stock_buy_alternative wizards etc.).
    for _ in range(2):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        m = modal.last
        pbtn = m.locator("button.btn-primary:visible").first
        if pbtn.count() == 0:
            break
        try:
            pbtn.click()
            page.wait_for_timeout(1000)
            _wait_no_loading(page)
        except Exception:
            break


def oracle(page):
    login(page)
    # Go directly to the Replenishment dashboard (server action path).
    page.goto(full_url("/odoo/replenishment"), timeout=60000)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    _search_for_product(page)
    _click_order_on_row(page)


run_oracle(oracle)
