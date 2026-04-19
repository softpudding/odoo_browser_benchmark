"""Oracle for purchase.add_product_to_rfq_with_taxes.

Open the seeded draft RFQ BENCH-ADD-TAX for vendor Bench Tax Vendor.
Click 'Add a product' in the Products tab to create a new inline o2m
row. Pick 'Bench Taxable Item' in the Product cell. Set product_qty to
3. Then click into the Taxes cell on the new row and pick
'Bench Tax 5%' from the many2many_tax_tags autocomplete dropdown.
Save (do NOT confirm).

Key selectors:
- `td.o_field_x2many_list_row_add a` for 'Add a product'.
- `td[name='product_id']` for the Product cell (merged with description
  via product_label_section_and_note_field widget, but the m2o
  autocomplete is still the first input in the cell).
- `td[name='product_qty']` for Quantity.
- `td[name='tax_ids']` for the Taxes cell (widget=many2many_tax_tags,
  behaves like many2many_tags: type + pick from dropdown to add a
  pill).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


PO_NAME = "BENCH-ADD-TAX"
PRODUCT_NEW = "Bench Taxable Item"
TAX_NAME = "Bench Tax 5%"
NEW_QTY = "3"


def _open_po(page):
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
                        args: [[['name', '=', 'BENCH-ADD-TAX']], ['id']],
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
        raise RuntimeError("Seeded BENCH-ADD-TAX purchase.order not found")
    navigate(page, f"/odoo/purchase/{po_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(600)


def _click_add_a_product(page):
    """Click the 'Add a product' link in the o2m list."""
    add_link = page.locator(
        ".o_form_view .o_list_renderer td.o_field_x2many_list_row_add a, "
        ".o_form_view .o_list_renderer a.o_field_x2many_list_row_add"
    )
    # Prefer 'Add a product' label over 'Add a section' / 'Add a note'.
    product_link = add_link.filter(has_text="Add a product")
    if product_link.count() > 0:
        product_link.first.click()
    else:
        add_link.first.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _selected_row(page):
    return page.locator(
        ".o_form_view .o_list_renderer .o_data_row.o_selected_row"
    ).first


def _pick_product_in_new_row(page, product_name):
    """Set the Product many2one on the newly-added (selected) row."""
    row = _selected_row(page)
    row.wait_for(state="visible", timeout=10000)

    cell = row.locator("td[name='product_id']").first
    cell.click()
    page.wait_for_timeout(400)

    # The product cell uses product_label_section_and_note_field; the
    # first input inside the cell is the m2o autocomplete.
    inp = cell.locator("input").first
    inp.wait_for(state="visible", timeout=5000)
    inp.click()
    inp.fill("")
    inp.fill(product_name)
    page.wait_for_timeout(900)

    # Click matching option from the dropdown.
    dropdown = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete:visible .ui-menu-item"
    )
    option = dropdown.filter(has_text=product_name).first
    option.wait_for(state="visible", timeout=5000)
    option.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)


def _set_qty_in_new_row(page, qty):
    """Set product_qty on the selected row."""
    row = _selected_row(page)
    cell = row.locator("td[name='product_qty']").first
    cell.click()
    page.wait_for_timeout(300)

    inp = cell.locator("input").first
    inp.wait_for(state="visible", timeout=5000)
    inp.click()
    # Triple-click-select then overwrite (qty default is 1.00).
    try:
        inp.press("Control+a")
    except Exception:
        pass
    inp.fill("")
    inp.fill(qty)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _add_tax_tag_in_new_row(page, tax_name):
    """Add a tax to the many2many_tax_tags pill cell on the selected row."""
    row = _selected_row(page)
    # Make sure we're still editing the new row.
    if row.count() == 0:
        # The save may have blurred; re-click the product cell to re-enter.
        any_row = page.locator(
            ".o_form_view .o_list_renderer .o_data_row"
        ).last
        any_row.locator("td[name='product_id']").first.click()
        page.wait_for_timeout(400)
        row = _selected_row(page)

    tax_cell = row.locator("td[name='tax_ids']").first
    if tax_cell.count() == 0 or not tax_cell.is_visible():
        # The Taxes column is `optional="show"` and enabled by default,
        # but just in case, try enabling it via the optional columns
        # dropdown.
        opt_toggle = page.locator(
            ".o_form_view .o_list_renderer .o_optional_columns_dropdown_toggle"
        ).first
        if opt_toggle.count() > 0:
            opt_toggle.click()
            page.wait_for_timeout(300)
            items = page.locator(".dropdown-menu:visible .dropdown-item")
            for i in range(items.count()):
                txt = items.nth(i).inner_text().strip().lower()
                if txt.startswith("taxes") or txt == "taxes":
                    cb = items.nth(i).locator("input[type='checkbox']")
                    if cb.count() > 0 and not cb.first.is_checked():
                        items.nth(i).click()
                        page.wait_for_timeout(300)
                    break
            try:
                page.press("body", "Escape")
            except Exception:
                pass
            page.wait_for_timeout(300)
            tax_cell = row.locator("td[name='tax_ids']").first

    tax_cell.scroll_into_view_if_needed()
    tax_cell.click()
    page.wait_for_timeout(400)

    # The m2m_tags cell renders an autocomplete input on edit.
    inp = tax_cell.locator("input").first
    inp.wait_for(state="visible", timeout=5000)
    inp.click()
    inp.fill("")
    inp.fill(tax_name)
    page.wait_for_timeout(900)

    dropdown = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete:visible .ui-menu-item"
    )
    option = dropdown.filter(has_text=tax_name).first
    option.wait_for(state="visible", timeout=5000)
    option.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)
    _open_po(page)

    # Click Products tab defensively (default-open on PO form).
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

    try:
        page.locator(
            ".o_form_view .o_list_renderer"
        ).first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    except Exception:
        pass

    # Add a new line.
    _click_add_a_product(page)

    # Fill product, quantity, taxes on the new (selected) row.
    _pick_product_in_new_row(page, PRODUCT_NEW)
    _set_qty_in_new_row(page, NEW_QTY)
    _add_tax_tag_in_new_row(page, TAX_NAME)

    # Blur the row so the save picks up all field edits.
    try:
        page.locator(".o_form_sheet_bg, .o_form_sheet").first.click(
            position={"x": 5, "y": 5}
        )
        page.wait_for_timeout(400)
    except Exception:
        pass

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
