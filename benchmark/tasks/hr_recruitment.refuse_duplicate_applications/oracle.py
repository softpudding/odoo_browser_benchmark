"""Oracle for hr_recruitment.refuse_duplicate_applications.

Open the Priya Nair applicant, use the Refuse dialog, enable duplicate
handling, and send the customized refusal email after creating the exact
refuse reason in Recruitment configuration.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_kanban_card,
    click_button_name,
    fill_field,
    login,
    modal_fill_field,
    set_many2one,
    navigate,
    run_oracle,
    _wait_no_loading,
)


EXPECTED_REASON = "Candidate withdrew after final review"
EXPECTED_TEMPLATE = "Benchmark Applicant Withdrawal Template"
EXPECTED_BODY = (
    "We are closing your Operations Analyst applications after your withdrawal request."
)


def _open_refuse_reasons(page):
    navigate(page, "/odoo/action-hr_recruitment.hr_applicant_refuse_reason_action")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _create_refuse_reason(page):
    click_create(page)
    page.wait_for_timeout(800)
    fill_field(page, "name", EXPECTED_REASON)
    page.wait_for_timeout(300)
    set_many2one(page, "template_id", EXPECTED_TEMPLATE)
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    row = page.locator(f".o_list_view .o_data_row:has-text('{EXPECTED_REASON}')")
    if row.count() == 0:
        raise RuntimeError(f"Failed to create refuse reason {EXPECTED_REASON!r}")


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    _open_refuse_reasons(page)
    _create_refuse_reason(page)

    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    click_kanban_card(page, "Operations Analyst")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    page.locator(
        ".o_kanban_record:has-text('Priya Nair'), "
        ".o_data_row:has-text('Priya Nair')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    click_button_name(page, "archive_applicant")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    modal.locator(
        ".o_field_selection_badge[name='refuse_reason_id'] .o_selection_badge, "
        ".o_field_widget[name='refuse_reason_id'] .o_selection_badge"
    ).filter(has_text=EXPECTED_REASON).first.click()
    page.wait_for_timeout(500)

    duplicates = modal.locator(
        ".o_field_boolean_toggle[name='duplicates'] input, "
        ".o_field_widget[name='duplicates'] input"
    )
    if duplicates.count() > 0 and not duplicates.first.is_checked():
        duplicates.first.click()
    else:
        toggle = modal.locator(
            ".o_field_boolean_toggle[name='duplicates'], "
            ".o_field_widget[name='duplicates'] button, "
            ".o_field_widget[name='duplicates'] .form-check"
        )
        if toggle.count() > 0:
            toggle.first.click()
    page.wait_for_timeout(800)

    modal_fill_field(page, "subject", "Operations Analyst application update")
    page.wait_for_timeout(500)

    body = modal.locator(
        ".o_field_widget[name='body'] .odoo-editor-editable, "
        ".o_field_widget[name='body'] [contenteditable='true']"
    ).first
    body.click()
    page.wait_for_timeout(300)
    body.press("Control+A")
    body.press("Backspace")
    body.press_sequentially(EXPECTED_BODY)
    body.dispatch_event("input")
    body.dispatch_event("change")
    page.wait_for_timeout(500)

    modal.locator("button[name='action_refuse_reason_apply']").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
