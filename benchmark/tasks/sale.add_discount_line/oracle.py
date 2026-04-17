"""Oracle for sale.add_discount_line.

Open the seeded Azure Interior quotation, set the Desk Organizer line discount
to 10%, and save without confirming the quotation.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    clear_search_filters(page)
    ensure_list_view(page)

    # The task's "reference" lives in a non-visible field, so use the visible
    # customer name to surface the seeded quotation and open the newest match.
    search_for(page, "Azure Interior")
    page.wait_for_timeout(1000)
    result_row = page.locator(".o_list_view .o_data_row").first
    result_row.click(force=True)
    page.wait_for_timeout(1500)
    if page.locator(".o_form_view").count() == 0:
        result_row.dblclick(force=True)
        page.wait_for_timeout(1500)
    if page.locator(".o_form_view").count() == 0:
        result_row.press("Enter")
        page.wait_for_timeout(1500)
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view", timeout=15000)

    page.locator(".o_form_view td[name='discount']").first.click(force=True)
    page.wait_for_timeout(300)

    # Odoo renders the active inline editor as the last visible numeric input.
    discount_input = page.locator("input.o_input").last
    discount_input.fill("10")
    discount_input.press("Tab")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    page.locator(".o_form_button_save:visible").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
