"""Oracle for stock.update_delivery_scheduled_date_validate."""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    cards = page.locator(".o_kanban_record:visible")
    opened = False
    for i in range(cards.count()):
        card = cards.nth(i)
        if "Delivery Orders" in card.inner_text() or "Delivery Order" in card.inner_text():
            card.click(); opened = True; break
    if not opened:
        page.locator(".o_kanban_record:has-text('Delivery'):visible").first.click()
    _wait_no_loading(page)
    page.wait_for_timeout(1000)
    clear_search_filters(page)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, "BENCH-DEL-DATE-01")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    sched_btn = page.locator(".o_field_widget[name='scheduled_date'] button").first
    sched_btn.click()
    page.wait_for_timeout(800)
    picker = page.locator(".o_datetime_picker:visible").first
    picker.locator(".o_next").first.click()
    page.wait_for_timeout(400)
    day = picker.locator(
        ".o_date_item_cell:not(.text-muted):has-text('27')"
    ).first
    day.click()
    page.wait_for_timeout(400)
    time_input = picker.locator("input").first
    if time_input.count() > 0:
        time_input.click(click_count=3)
        time_input.fill("11:30:00am")
        time_input.press("Tab")
        page.wait_for_timeout(300)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        row_text = rows.nth(i).inner_text()
        if "Steel Bracket" in row_text:
            set_o2m_field(page, i, "quantity", "20")
            page.wait_for_timeout(300)
        elif "Copper Wire" in row_text:
            set_o2m_field(page, i, "quantity", "8")
            page.wait_for_timeout(300)
    page.wait_for_timeout(500)
    click_status_button(page, "Validate")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        no_bo = modal.last.locator("button:has-text('No Backorder')")
        if no_bo.count() > 0:
            no_bo.first.click()
        else:
            modal.last.locator("button:has-text('Apply'), button:has-text('Validate'), button:has-text('Ok'), button.btn-primary").first.click()
        page.wait_for_timeout(1000)
        _wait_no_loading(page)


run_oracle(oracle)
