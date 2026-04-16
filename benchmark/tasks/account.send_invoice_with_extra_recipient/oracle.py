"""Oracle for account.send_invoice_with_extra_recipient.

Open the posted invoice SEND-APR-17, add the controller as an extra recipient
in the Send wizard, overwrite subject and body, and send the email.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


TARGET_BODY = (
    "Please review the April service invoice and reply with any approval notes by Friday."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    click_list_row(page, "SEND-APR-17")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_status_button(page, "Send")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last

    # Add the extra recipient without removing the default finance recipient.
    recipient_input = modal.locator(
        ".o_field_widget[name='mail_partner_ids'] input"
    ).last
    recipient_input.click()
    recipient_input.fill("controller@beacon-offshore.example.com")
    page.wait_for_timeout(1000)
    recipient_item = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    ).filter(has_text="controller@beacon-offshore.example.com").first
    recipient_item.click()
    page.wait_for_timeout(500)

    subject = modal.locator(".o_field_widget[name='subject'] input").first
    subject.click()
    subject.fill("")
    subject.fill("Beacon Offshore invoice review")
    subject.press("Tab")
    page.wait_for_timeout(500)

    body = modal.locator(
        ".o_field_widget[name='body'] .odoo-editor-editable, "
        ".o_field_widget[name='body'] [contenteditable='true']"
    ).first
    body.click()
    page.wait_for_timeout(300)
    page.keyboard.press("Control+A")
    page.wait_for_timeout(200)
    page.keyboard.press("Backspace")
    page.wait_for_timeout(200)
    page.keyboard.insert_text(TARGET_BODY)
    page.wait_for_timeout(500)
    body.press("Tab")
    page.wait_for_timeout(300)

    modal.locator("button:has-text('Send')").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
