"""Oracle for survey.publish_share_via_link_get_url.

Open the seeded 'Customer Pulse Q2' survey, click the Share button in the
form header, verify the share dialog displays the public Survey Link, and
close the dialog without sending an email.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


SURVEY_TITLE = "Customer Pulse Q2"


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-survey.action_survey_form")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Survey root view defaults to kanban; open the target card.
    card_selector = (
        f".o_kanban_view .o_kanban_record:has-text('{SURVEY_TITLE}'), "
        f".o_list_view .o_data_row:has-text('{SURVEY_TITLE}')"
    )
    page.wait_for_selector(card_selector, state="visible", timeout=15000)
    page.locator(card_selector).first.click()
    page.wait_for_selector(".o_form_view", state="visible", timeout=15000)
    _wait_for_ready(page)
    page.wait_for_timeout(600)

    # Click the form-header "Share" button (name=action_send_survey).
    share_btn = page.locator(
        ".o_form_view .o_form_statusbar button[name='action_send_survey']:visible, "
        ".o_form_view header button[name='action_send_survey']:visible"
    ).first
    share_btn.wait_for(state="visible", timeout=10000)
    share_btn.click()

    # The Share a Survey wizard opens as a modal with the Survey Link field.
    page.wait_for_selector(
        ".modal:visible .o_field_widget[name='survey_start_url']",
        state="visible",
        timeout=15000,
    )
    page.wait_for_timeout(500)

    # Sanity: the Survey Link widget displays a non-empty /survey/start/ URL.
    # CopyClipboardChar renders the readonly value either as a <span> (text)
    # or via an <input> (display) depending on the active widget mode. Try
    # both to be robust.
    link_widget = page.locator(
        ".modal:visible .o_field_widget[name='survey_start_url']"
    ).first
    text_value = (link_widget.text_content() or "").strip()
    if "/survey/start/" not in text_value:
        # Fallback: maybe the value is in an inner input.
        inputs = link_widget.locator("input")
        if inputs.count() > 0:
            text_value = (inputs.first.input_value() or "").strip()
    if "/survey/start/" not in text_value:
        raise RuntimeError(
            f"Share dialog did not expose a /survey/start/ URL (got: {text_value!r})"
        )

    # Close the dialog using the footer Close button (cancel) — do NOT click Send.
    close_btn = page.locator(
        ".modal:visible .modal-footer button:has-text('Close')"
    ).first
    close_btn.wait_for(state="visible", timeout=5000)
    close_btn.click()
    _wait_no_loading(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
