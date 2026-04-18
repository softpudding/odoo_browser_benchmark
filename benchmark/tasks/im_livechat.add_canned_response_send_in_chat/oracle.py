"""Oracle for im_livechat.add_canned_response_send_in_chat."""

from benchmark.oracle_helpers import (
    click_create,
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

    navigate(page, "/odoo/action-mail.mail_canned_response_action")
    _wait_no_loading(page)

    click_create(page)
    _wait_for_ready(page)
    fill_field(page, "source", ":greet")
    fill_text_field(
        page,
        "substitution",
        "Hello! How can I help you today? \u2014 Bench Support",
    )
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
