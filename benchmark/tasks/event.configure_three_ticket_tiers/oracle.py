"""Oracle for event.configure_three_ticket_tiers.

Open the Summer DevCon event, go to Tickets tab, add three tickets.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # Clear filters.
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

    click_list_row(page, "Summer DevCon 2026")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Open the Tickets tab.
    try:
        click_tab(page, "Tickets")
    except Exception:
        tab = page.locator("a.nav-link:has-text('Tickets'):visible")
        if tab.count() > 0:
            tab.first.click()
    page.wait_for_timeout(500)

    tiers = [
        ("Early Bird", "99.00", "80"),
        ("Regular", "149.00", "200"),
        ("VIP", "299.00", "40"),
    ]

    for idx, (name, price, seats) in enumerate(tiers):
        # Click "Add a line" — the exact DOM shape of this anchor changes
        # between list and kanban mode inside the x2many.
        add_line = page.locator(
            "div[name='event_ticket_ids'] a:has-text('Add a line'), "
            "div[name='event_ticket_ids'] button:has-text('Add a line'), "
            "div[name='event_ticket_ids'] a.o_field_x2many_list_row_add, "
            ".o_field_x2many[name='event_ticket_ids'] a:has-text('Add a line')"
        ).first
        add_line.wait_for(state="visible", timeout=15000)
        add_line.click()
        page.wait_for_timeout(500)
        set_o2m_field(page, idx, "name", name)
        set_o2m_field(page, idx, "price", price)
        set_o2m_field(page, idx, "seats_max", seats)
        page.wait_for_timeout(300)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
