"""Oracle for sale.add_line_with_optional_template_apply_discount.

Open the seeded Bench Optional Co quotation (S-BENCH-OPT-001), add a new
order line for "Bench Service Bundle" with qty 2 and per-line discount 10%,
then save without confirming.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    clear_search_filters(page)
    ensure_list_view(page)

    # Find the seeded quotation by customer reference.
    search_for(page, "S-BENCH-OPT-001")
    page.wait_for_timeout(1000)
    row = page.locator(".o_list_view .o_data_row").first
    row.click(force=True)
    page.wait_for_timeout(1500)
    if page.locator(".o_form_view").count() == 0:
        # Fall back to searching by partner name if the reference search
        # returned nothing.
        clear_search_filters(page)
        search_for(page, "Bench Optional Co")
        page.wait_for_timeout(1000)
        page.locator(".o_list_view .o_data_row").first.click(force=True)
        page.wait_for_timeout(1500)
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view", timeout=15000)

    # Add a new line.
    click_add_a_line(page)
    page.wait_for_timeout(800)

    # The newly added (empty) row is the LAST data row in the o2m list.
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    new_index = rows.count() - 1
    if new_index < 0:
        new_index = 0

    # Pick the product via the autocomplete on product_template_id.
    set_o2m_many2one(page, new_index, "product_template_id", "Bench Service Bundle")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Set quantity 2 on this line.
    set_o2m_field(page, new_index, "product_uom_qty", "2")
    page.wait_for_timeout(500)

    # Set per-line discount 10 on this line.
    set_o2m_field(page, new_index, "discount", "10")
    page.wait_for_timeout(500)

    # Save (do not confirm).
    save_form(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
