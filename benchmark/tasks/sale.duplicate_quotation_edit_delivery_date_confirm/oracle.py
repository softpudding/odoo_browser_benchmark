"""Oracle for sale.duplicate_quotation_edit_delivery_date_confirm.

Open draft quotation S-BENCH-COPY-001 for Bench Copy Co, duplicate it via
the cog/Actions menu, set the copy's Delivery Date (commitment_date on the
Other Info tab) to 08/15/2026, save, then click Confirm in the status bar.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    click_tab,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)


def _open_source_quotation(page):
    """Navigate to Sales and open the seeded S-BENCH-COPY-001 quotation.

    Resolves the SO id via JSON-RPC (the oracle is allowed to short-circuit
    UI navigation for record lookup; the actual Duplicate/Confirm flow is
    still driven through the form UI), then navigates directly to that
    record. Bypasses flakiness in the default /odoo/sales search + list
    rendering.
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
                        args: [[['name', '=', 'S-BENCH-COPY-001']], ['id']],
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
        raise RuntimeError("Seeded S-BENCH-COPY-001 sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(500)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_source_quotation(page)
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
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # --- Set commitment_date on the Other Info tab ---
    click_tab(page, "Other Info")
    page.wait_for_timeout(400)

    # `commitment_date` is a Datetime field. It may render as a bare <input>
    # (empty default) or the dual button/input DateTimeField when a value
    # is already present. Seed leaves it empty, so a plain fill should work;
    # we inline the button->input flip defensively (see ODOO19_PATTERNS.md
    # § DateTimeField widget: button vs input dual rendering).
    widget = page.locator(".o_field_widget[name='commitment_date']").first
    widget.wait_for(state="visible", timeout=8000)
    # Flip button (if any) to input
    clickable = widget.locator("button, input").first
    clickable.click()
    page.wait_for_timeout(300)
    inp = widget.locator("input").first
    inp.wait_for(state="visible", timeout=5000)
    inp.fill("")
    inp.type("08/15/2026 00:00:00", delay=20)
    page.keyboard.press("Escape")  # close date picker popover if it opened
    page.wait_for_timeout(300)
    # Click outside the field to commit the value
    page.locator(".o_form_sheet").first.click(position={"x": 10, "y": 10})
    page.wait_for_timeout(300)
    _wait_no_loading(page)

    # --- Save the duplicate ---
    save_form(page)
    page.wait_for_timeout(900)
    _wait_no_loading(page)

    # --- Confirm the duplicate via the status-bar Confirm button ---
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
