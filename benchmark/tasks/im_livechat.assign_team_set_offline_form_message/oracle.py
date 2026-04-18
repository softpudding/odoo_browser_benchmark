"""Oracle for im_livechat.assign_team_set_offline_form_message.

The Live Chat kanban opens the discuss-channel session view by default; to reach
the configuration form (with the Options tab) we open the kanban card menu and
click "Configure Channel" (per the Odoo 19 Live Chat cookbook quirk).
"""

from benchmark.oracle_helpers import (
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


BUTTON_TEXT = "Leave us a message and we will follow up by Monday."
DEFAULT_MESSAGE = (
    "Hello \u2014 we are offline. "
    "Email support@bench.test and we will reply by Monday."
)


def _open_website_support_form(page):
    """Open the Website Support channel form via the kanban dropdown."""
    card = page.locator(
        ".o_kanban_view .o_kanban_record:has-text('Website Support')"
    ).first
    card.scroll_into_view_if_needed()
    card.hover()
    page.wait_for_timeout(300)

    # Click the per-card menu toggle (3-dots).
    menu_btn = card.locator(
        ".o_dropdown_kanban button, "
        "button[title='Dropdown menu'], "
        "button:has(.oi-ellipsis-v)"
    )
    menu_btn.first.click(force=True)
    page.wait_for_timeout(400)

    # Click "Configure Channel" dropdown item.
    page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Configure Channel'), "
        ".dropdown-menu .dropdown-item:has-text('Configure Channel')"
    ).first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/livechat")
    _wait_no_loading(page)

    _open_website_support_form(page)

    # Switch to the "Options" tab.
    click_tab(page, "Options")
    page.wait_for_timeout(500)

    # Update the two text fields. Both are Char fields rendered as plain inputs.
    fill_field(page, "button_text", BUTTON_TEXT)
    fill_field(page, "default_message", DEFAULT_MESSAGE)

    # Save the parent channel form so the new values are persisted.
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
