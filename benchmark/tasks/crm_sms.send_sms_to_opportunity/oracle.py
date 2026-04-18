"""Oracle for crm_sms.send_sms_to_opportunity.

Open the CRM pipeline, click the 'Bench Hot Lead' opportunity card,
open the cog Actions menu, click 'Send SMS', fill the body, and click
Send in the dialog footer.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


SMS_BODY = "Following up on your inquiry. - Bench team"


def _open_cog_menu(page):
    cog = page.locator(
        ".o_cp_action_menus button:visible, "
        ".o_control_panel button.dropdown-toggle:has-text('Actions'):visible, "
        ".o_control_panel .fa-cog:visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)


def _click_send_sms_menu_item(page):
    item = page.locator(
        ".dropdown-menu:visible .dropdown-item:has-text('Send SMS'), "
        ".o-dropdown--menu:visible .dropdown-item:has-text('Send SMS')"
    ).first
    item.click()
    page.wait_for_timeout(800)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(500)


def _fill_sms_body(page, body: str):
    modal = page.locator(".modal:visible").last
    # The body field uses widget="sms_widget" — an auto-resizing <textarea>
    body_field = modal.locator(
        ".o_field_widget[name='body'] textarea:visible"
    ).first
    body_field.click()
    body_field.fill("")
    body_field.type(body)
    page.wait_for_timeout(400)


def _click_send(page):
    modal = page.locator(".modal:visible").last
    # The Send button has name="action_send_sms" and label "Send"
    send_btn = modal.locator(
        ".modal-footer button[name='action_send_sms']:not([disabled]):visible"
    ).first
    send_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # Click the opportunity kanban card
    click_kanban_card(page, "Bench Hot Lead")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Open cog Actions menu → Send SMS
    _open_cog_menu(page)
    _click_send_sms_menu_item(page)

    # Fill SMS body
    _fill_sms_body(page, SMS_BODY)

    # Click Send
    _click_send(page)


run_oracle(oracle)
