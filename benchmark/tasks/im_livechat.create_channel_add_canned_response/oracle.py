"""Oracle for im_livechat.create_channel_add_canned_response."""

from benchmark.oracle_helpers import (
    click_create,
    click_tab,
    fill_field,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/livechat")
    _wait_no_loading(page)

    click_create(page)
    _wait_for_ready(page)

    fill_field(page, "name", "Checkout Support")
    click_tab(page, "Options")
    fill_field(page, "button_text", "Need help with your order?")
    save_form(page)
    _wait_no_loading(page)

    navigate(page, "/odoo/action-mail.mail_canned_response_action")
    _wait_no_loading(page)

    click_create(page)
    _wait_for_ready(page)
    fill_field(page, "source", "checkout_help")
    fill_text_field(page, "substitution", "Hello, thanks for contacting checkout support.")
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
