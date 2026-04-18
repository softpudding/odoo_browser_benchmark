"""Oracle for survey.invite_attendees_send_email.

Open the seeded 'Bench Onboarding Quiz' survey, click the form-header Send
button (survey.survey.action_send_survey), add the three seeded partners
(Alice/Bob/Carol Invitee) into the Recipients many2many_tags_email field,
overwrite the Subject, and click the dialog-footer Send button
(survey.invite.action_invite).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


SURVEY_TITLE = "Bench Onboarding Quiz"
RECIPIENT_EMAILS = ["alice@x.com", "bob@y.com", "carol@z.com"]
SUBJECT = "Please complete onboarding"


def _add_recipient(page, modal, email):
    """Type email in the Recipients many2many_tags_email input and pick the
    matching partner from autocomplete.
    """
    partner_widget = modal.locator(".o_field_widget[name='partner_ids']").first
    partner_widget.wait_for(state="visible", timeout=10000)
    # The visible input inside many2many_tags is an autocomplete input.
    rec_input = partner_widget.locator("input[type='text'], .o-autocomplete input").first
    rec_input.click()
    rec_input.fill(email)
    # Wait for the dropdown suggestions to render.
    page.wait_for_selector(
        ".o-autocomplete--dropdown-menu .o-autocomplete--dropdown-item:visible",
        state="visible",
        timeout=5000,
    )
    page.wait_for_timeout(400)
    # Click the first suggestion that contains the email.
    suggestion = page.locator(
        ".o-autocomplete--dropdown-menu .o-autocomplete--dropdown-item:visible"
    ).filter(has_text=email).first
    if suggestion.count() == 0:
        # Fallback: click the first suggestion anyway (it should be the
        # seeded partner).
        suggestion = page.locator(
            ".o-autocomplete--dropdown-menu .o-autocomplete--dropdown-item:visible"
        ).first
    suggestion.click()
    page.wait_for_timeout(500)


def oracle(page):
    login(page)
    navigate(page, "/odoo/action-survey.action_survey_form")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Open the survey form (kanban or list).
    card_selector = (
        f".o_kanban_view .o_kanban_record:has-text('{SURVEY_TITLE}'), "
        f".o_list_view .o_data_row:has-text('{SURVEY_TITLE}')"
    )
    page.wait_for_selector(card_selector, state="visible", timeout=15000)
    page.locator(card_selector).first.click()
    page.wait_for_selector(".o_form_view", state="visible", timeout=15000)
    _wait_for_ready(page)
    page.wait_for_timeout(600)

    # Form-header "Send" (name=action_send_survey).
    send_btn = page.locator(
        ".o_form_view .o_form_statusbar button[name='action_send_survey']:visible, "
        ".o_form_view header button[name='action_send_survey']:visible"
    ).first
    send_btn.wait_for(state="visible", timeout=10000)
    send_btn.click()

    # Wait for the invite wizard modal to open.
    page.wait_for_selector(".modal:visible .o_form_view", state="visible", timeout=15000)
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last

    # Add the three seeded Recipients via autocomplete.
    for email in RECIPIENT_EMAILS:
        _add_recipient(page, modal, email)

    # Overwrite the Subject field.
    subject_widget = modal.locator(".o_field_widget[name='subject']").first
    subject_widget.wait_for(state="visible", timeout=10000)
    subject_input = subject_widget.locator("input, textarea").first
    subject_input.click()
    subject_input.press("Control+a")
    subject_input.press("Delete")
    subject_input.fill(SUBJECT)
    page.keyboard.press("Tab")
    page.wait_for_timeout(400)

    # Click footer Send (name=action_invite).
    send_dialog_btn = modal.locator(
        ".modal-footer button[name='action_invite']:visible, "
        ".modal-footer button.btn-primary:has-text('Send'):visible"
    ).first
    send_dialog_btn.wait_for(state="visible", timeout=10000)
    send_dialog_btn.click()

    # Wait for the wizard to close and the form view to return.
    try:
        page.wait_for_selector(".modal:visible", state="hidden", timeout=20000)
    except Exception:
        pass
    _wait_no_loading(page)
    page.wait_for_timeout(1500)


run_oracle(oracle)
