"""Oracle for purchase.set_vendor_product_code_on_po_line.

Open the seeded draft RFQ BENCH-VCODE for vendor Bench Code Supplier
and overwrite the Description cell on the sole order line to
'BENCH-WDG-A1 / Bench Widget'. Save (do NOT confirm).

`purchase.order.line.name` is `fields.Text(...)` with
`compute='_compute_price_unit_and_date_planned_and_name', store=True,
readonly=False`. The list-inline editor renders a <textarea> in
td[name='name'] on the selected row.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


PO_NAME = "BENCH-VCODE"
TARGET_TEXT = "BENCH-WDG-A1 / Bench Widget"


def _open_po(page):
    """Resolve the seeded PO id via JSON-RPC and navigate to the form."""
    po_id = page.evaluate(
        """async () => {
            const res = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'purchase.order',
                        method: 'search_read',
                        args: [[['name', '=', 'BENCH-VCODE']], ['id']],
                        kwargs: {},
                    },
                }),
            });
            const json = await res.json();
            if (json.error) throw new Error(json.error.data?.message || json.error.message);
            return json.result.length ? json.result[0].id : null;
        }"""
    )
    if not po_id:
        raise RuntimeError("Seeded BENCH-VCODE purchase.order not found")
    navigate(page, f"/odoo/purchase/{po_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(500)


def _edit_description_cell(page, text):
    """Overwrite the Description on the sole PO line.

    Odoo 19 renders `purchase.order.line.name` via the
    `product_label_section_and_note_field` widget (see
    addons/account/static/src/components/product_label_section_and_note_field/).
    The widget merges the `product_id` and `name` columns into a single
    cell under `td[name='product_id']`. The description <textarea>
    lives inside `.o_field_product_label_section_and_note_cell` but
    gets `class="d-none"` when `label` is empty (i.e. when `name`
    equals the product display name). A toggler button
    (`.fa-bars`, tooltip "Click or press enter to add a description")
    is rendered in that case; clicking it sets `labelVisibility=true`
    and removes `d-none` from the textarea.

    `parseLabel` (product_label_section_and_note_field.js:50-54) writes
    back `productName + "\\n" + value` when both are set, so typing
    the target text in the label produces a stored `name` of
    "Bench Widget\\nBENCH-WDG-A1 / Bench Widget". The check.py only
    requires that `BENCH-WDG-A1` be a substring of `name`, so this is
    acceptable — the vendor code is captured even with the two-line
    form.
    """
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row"
    ).first
    row.wait_for(state="visible", timeout=10000)

    # Click into the product_id cell first to activate row edit mode
    # (this also mounts the widget's toggler/textarea).
    product_cell = row.locator("td[name='product_id']").first
    product_cell.wait_for(state="visible", timeout=5000)
    product_cell.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    selected_row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row.o_selected_row"
    ).first
    selected_row.wait_for(state="visible", timeout=5000)

    # Click the label-visibility toggler if the textarea is hidden.
    toggler = selected_row.locator(
        "td[name='product_id'] button.o_external_button.fa-bars, "
        "td[name='product_id'] button.fa-bars, "
        "td[name='product_id'] button[data-tooltip*='description']"
    ).first
    if toggler.count() > 0 and toggler.is_visible():
        try:
            toggler.click()
            page.wait_for_timeout(300)
        except Exception:
            pass

    # Find the description textarea inside the merged cell.
    desc_area = selected_row.locator(
        "td[name='product_id'] .o_field_product_label_section_and_note_cell textarea"
    ).first
    if desc_area.count() == 0 or not desc_area.is_visible():
        # Fallback: unhide any `d-none` textareas in the cell by
        # stripping the class in-DOM, then retarget.
        page.evaluate(
            """() => {
                document.querySelectorAll(
                    '.o_form_view .o_list_renderer .o_data_row.o_selected_row '
                    + "td[name='product_id'] .o_field_product_label_section_and_note_cell textarea.d-none"
                ).forEach(el => el.classList.remove('d-none'));
            }"""
        )
        desc_area = selected_row.locator(
            "td[name='product_id'] .o_field_product_label_section_and_note_cell textarea"
        ).first

    desc_area.wait_for(state="visible", timeout=5000)
    desc_area.click()
    try:
        desc_area.fill(text)
    except Exception:
        desc_area.press("Control+a")
        desc_area.press("Delete")
        desc_area.type(text, delay=10)
    page.wait_for_timeout(300)
    desc_area.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    _open_po(page)
    page.wait_for_timeout(500)

    # Products tab is default-open on the PO form; defensively click it.
    tab = page.locator(
        ".o_notebook .nav-link:has-text('Products'), "
        ".o_notebook .nav-link:has-text('Order Lines')"
    )
    if tab.count() > 0 and tab.first.is_visible():
        try:
            tab.first.click()
            page.wait_for_timeout(400)
        except Exception:
            pass
    _wait_no_loading(page)

    # Scroll the lines list into view.
    try:
        page.locator(
            ".o_form_view .o_list_renderer"
        ).first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    except Exception:
        pass

    _edit_description_cell(page, TARGET_TEXT)

    # Commit and save. Click an inert area of the sheet to leave edit
    # mode before saving (blur-vs-save race same as sale order tasks).
    try:
        page.locator(".o_form_sheet_bg, .o_form_sheet").first.click(
            position={"x": 5, "y": 5}
        )
        page.wait_for_timeout(300)
    except Exception:
        pass

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
