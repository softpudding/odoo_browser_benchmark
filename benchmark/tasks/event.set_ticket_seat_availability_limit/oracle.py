"""Oracle for event.set_ticket_seat_availability_limit."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters + list view.
    for _ in range(5):
        facets = page.locator(".o_searchview .o_facet_remove:visible")
        if facets.count() == 0:
            break
        try:
            facets.first.click()
            page.wait_for_timeout(300)
        except Exception:
            break
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)

    click_list_row(page, "Autumn AI Summit")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    try:
        click_tab(page, "Tickets")
    except Exception:
        tab = page.locator("a.nav-link:has-text('Tickets'):visible")
        if tab.count() > 0:
            tab.first.click()
    page.wait_for_timeout(500)

    # Double-click seats_max cell of General Admission row.
    row = page.locator(
        "tr.o_data_row:has-text('General Admission')"
    ).first
    row.wait_for(state="visible", timeout=15000)
    cell = row.locator("td[name='seats_max']").first
    cell.dblclick()
    page.wait_for_timeout(300)
    inp = page.locator(
        "tr.o_selected_row td[name='seats_max'] input, "
        "td[name='seats_max'] input:visible"
    ).first
    inp.fill("250")
    page.keyboard.press("Tab")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
