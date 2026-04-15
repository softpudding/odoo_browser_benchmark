"""Oracle for sale.revise_target_quote_lines.

Find quotation with customer reference OPS-042 (Aurora Interiors).
Update order lines:
  - Standing Desk: description "Ergonomic standing desk bundle", discount 5%
  - Office Chair: description "Mesh chair support package", discount 10%
  - Whiteboard: description "Magnetic planning board", discount 0%
Set Payment Terms to "15 Days" in Other Info tab. Save.
"""

from benchmark.oracle_helpers import (
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
    clear_search_filters,
    search_for,
)


def _find_and_open_quotation(page, ref_text):
    """Find a quotation by customer reference and open it.

    Manually handles the search to avoid the click_list_row helper's
    infinite loop issue with facet removal.
    """
    # Remove default "My Quotations" filter if present
    for _ in range(5):
        facet = page.locator(".o_searchview_facet .o_facet_remove")
        if facet.count() == 0:
            break
        facet.first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    page.wait_for_timeout(500)

    # Search for the customer reference
    search_for(page, ref_text)
    page.wait_for_timeout(1000)

    # Click the first result
    row = page.locator(".o_list_view .o_data_row")
    if row.count() > 0:
        row.first.click()
        page.wait_for_load_state("load")
        _wait_for_ready(page)
    else:
        raise Exception(f"No quotation found for reference {ref_text}")


def _edit_line_description(page, row_index, new_description):
    """Edit the description (name field) of a sale order line.

    First click on the row to activate inline editing, then locate
    the editable name field.
    """
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")

    # Click the row to start editing
    row = rows.nth(row_index)
    row.click()
    page.wait_for_timeout(500)

    # In Odoo 19, after clicking a row in the one2many list, the row becomes
    # the "selected row". Look for the name field in the selected row.
    # The name field might be in td[name='name'] or as a cell without explicit name
    selected_row = page.locator(
        ".o_form_view .o_list_renderer .o_selected_row"
    )
    if selected_row.count() == 0:
        # Try clicking the first cell of the row
        row.locator("td").first.click()
        page.wait_for_timeout(500)
        selected_row = page.locator(
            ".o_form_view .o_list_renderer .o_selected_row"
        )

    # Look for the name cell and click it
    name_cell = selected_row.locator("td[name='name']")
    if name_cell.count() > 0:
        name_cell.first.click()
        page.wait_for_timeout(300)
    else:
        # The name field might not have a name attribute on the td.
        # Try to find it by looking for the text widget
        name_widget = selected_row.locator(".o_field_widget[name='name']")
        if name_widget.count() > 0:
            name_widget.first.click()
            page.wait_for_timeout(300)

    # Now find the textarea or input in the active editing area
    editable = selected_row.locator(
        "td[name='name'] textarea, "
        "td[name='name'] input, "
        ".o_field_widget[name='name'] textarea, "
        ".o_field_widget[name='name'] input"
    )
    if editable.count() == 0:
        # Broad search: any textarea in the selected row
        editable = selected_row.locator("textarea")
    if editable.count() == 0:
        editable = selected_row.locator("input.o_input")

    editable.first.fill(new_description)
    editable.first.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the quotation with ref OPS-042
    _find_and_open_quotation(page, "OPS-042")
    page.wait_for_timeout(1000)

    # Odoo auto-prepends the product name to the description on save.
    # So we only need to set the description part. The final stored value
    # will be "Product Name\nDescription text".
    _edit_line_description(page, 0, "Ergonomic standing desk bundle")
    set_o2m_field(page, 0, "discount", "5")
    page.wait_for_timeout(500)

    _edit_line_description(page, 1, "Mesh chair support package")
    set_o2m_field(page, 1, "discount", "10")
    page.wait_for_timeout(500)

    _edit_line_description(page, 2, "Magnetic planning board")
    page.wait_for_timeout(500)

    # Set Payment Terms to "15 Days" in Other Info tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)

    set_many2one(page, "payment_term_id", "15 Days")
    page.wait_for_timeout(500)

    # Save (don't confirm)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
