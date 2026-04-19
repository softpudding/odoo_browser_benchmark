"""Oracle for sale.duplicate_confirmed_order_edit_customer.

Open the confirmed sale.order with client_order_ref BENCH-DUP for
Bench Orig Co, duplicate it via the cog/Actions menu, on the new draft
copy change the Customer m2o to Bench Clone Co, then Save (no Confirm).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def _open_source_order(page):
    """Resolve the source SO id via JSON-RPC and navigate to its form.

    The /odoo/sales list applies "My Quotations" filter by default, and
    `BENCH-DUP` lives in `client_order_ref` rather than the default-shown
    list columns. Short-circuit via a single JSON-RPC search_read so the
    oracle lands deterministically on the record regardless of the list
    view's default filter/view mode.
    """
    so_id = page.evaluate(
        """async () => {
            const res = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'sale.order',
                        method: 'search_read',
                        args: [[['client_order_ref', '=', 'BENCH-DUP']], ['id']],
                        kwargs: {},
                    },
                }),
            });
            const json = await res.json();
            if (json.error) throw new Error(json.error.data?.message || json.error.message);
            return json.result.length ? json.result[0].id : null;
        }"""
    )
    if not so_id:
        raise RuntimeError("Seeded BENCH-DUP sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(500)


def _set_partner_on_current_form(page, partner_name: str):
    """Click the partner_id m2o, clear it, type the new name, and
    select from the autocomplete dropdown."""
    widget = page.locator(".o_field_widget[name='partner_id']").first
    widget.wait_for(state="visible", timeout=8000)
    inp = widget.locator("input").first
    inp.click()
    # Select all + delete (more reliable than .fill('') when there's
    # already a value + a dropdown portal attached).
    inp.press("Control+a")
    inp.press("Delete")
    page.wait_for_timeout(200)
    inp.fill(partner_name)
    page.wait_for_timeout(900)
    # The autocomplete dropdown may render at the page root (portal).
    dropdown = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".o-autocomplete--dropdown-menu:visible li, "
        ".dropdown-menu:visible .dropdown-item"
    )
    # Prefer an exact match on the partner name, avoid 'Create "X"' quick-create
    # entries (we already seeded Bench Clone Co, so it exists).
    items = dropdown.filter(has_text=partner_name)
    chosen = None
    for i in range(items.count()):
        txt = items.nth(i).inner_text()
        if txt.strip().startswith("Create"):
            continue
        chosen = items.nth(i)
        break
    if chosen is None and items.count() > 0:
        chosen = items.first
    if chosen is None:
        raise RuntimeError(
            f"No autocomplete option found for partner '{partner_name}'"
        )
    chosen.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_source_order(page)
    page.wait_for_timeout(500)

    # --- cog/Actions -> Duplicate ---
    cog = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_cp_action_menus button:has(.fa-cog):visible, "
        ".o_control_panel_actions button.dropdown-toggle:visible, "
        ".o_control_panel button:has(.fa-cog):visible"
    ).first
    cog.click()
    page.wait_for_timeout(600)
    dup_item = page.locator(
        ".o-dropdown--menu:visible .dropdown-item:has-text('Duplicate'), "
        ".dropdown-menu:visible .dropdown-item:has-text('Duplicate')"
    ).first
    dup_item.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Duplicate lands on a new draft SO. The partner_id field is always
    # visible on the main tab.
    _set_partner_on_current_form(page, "Bench Clone Co")

    # Click outside to commit the m2o selection
    page.locator(".o_form_sheet").first.click(position={"x": 10, "y": 10})
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # --- Save the duplicate (do NOT confirm) ---
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
