"""Oracle for crm.create_lead_priority_schedule_call."""

from benchmark.oracle_helpers import (
    click_create,
    clear_search_filters,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    _wait_no_loading,
    _wait_for_ready,
)


def _fill_name_widget(page, value: str) -> None:
    widget = page.locator(".o_field_widget[name='name']").first
    widget.click()
    page.wait_for_timeout(300)
    editor = widget.locator(
        "input:visible, textarea:visible, .odoo-editor-editable:visible, [contenteditable='true']:visible"
    ).first
    editor.click()
    tag_name = editor.evaluate("el => el.tagName.toLowerCase()")
    if tag_name in {"input", "textarea"}:
        editor.fill("")
        editor.fill(value)
        editor.press("Tab")
    else:
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        page.keyboard.insert_text(value)
        editor.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/web#action=crm.crm_lead_all_leads")
    _wait_no_loading(page)
    ensure_list_view(page)
    clear_search_filters(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    _fill_name_widget(page, "Apex Warehouse Expansion")
    page.wait_for_timeout(300)
    fill_field(page, "contact_name", "Jordan Pike")
    page.wait_for_timeout(300)
    fill_field(page, "email_from", "jordan.pike@apexwarehouse.com")
    page.wait_for_timeout(300)

    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star, .o_field_widget[name='priority'] .fa-star-o, .o_field_widget[name='priority'] .fa-star")
    if stars.count() >= 2:
        stars.nth(1).click()
        page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(800)
    schedule_activity(
        page,
        activity_type="Call",
        summary="Qualify warehouse rollout",
        due_date="06/15/2026",
    )
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
