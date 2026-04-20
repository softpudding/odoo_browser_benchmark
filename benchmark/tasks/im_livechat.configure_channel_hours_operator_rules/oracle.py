"""Oracle for im_livechat.configure_channel_hours_operator_rules."""
from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    click_tab,
    fill_field,
    login,
    modal_click_button,
    modal_fill_field,
    navigate,
    run_oracle,
    save_form,
)

def oracle(page):
    login(page)
    navigate(page, "/odoo/livechat")
    click_create(page)
    fill_field(page, "name", "Support Routing")
    click_tab(page, "Options")
    fill_field(page, "button_text", "Talk to support now")
    page.locator(
        ".o_field_widget[name='max_sessions_mode'] input[data-value='limited']"
    ).first.click()
    page.wait_for_selector(".o_field_widget[name='max_sessions'] input", timeout=15000)
    fill_field(page, "max_sessions", "1")
    click_tab(page, "Agents")
    click_add_a_line(page)
    page.locator(
        ".modal .o_data_row:has-text('Demo User') .o_list_record_selector input"
    ).first.check()
    modal_click_button(page, "Select")
    click_tab(page, "Rules")
    click_add_a_line(page)
    page.locator(".modal .o_field_widget[name='action'] label").filter(
        has_text="Show"
    ).first.click()
    modal_fill_field(page, "regex_url", "/support")
    modal_click_button(page, "Save & Close")
    save_form(page)

run_oracle(oracle)
