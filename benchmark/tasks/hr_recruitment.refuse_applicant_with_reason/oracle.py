"""Oracle for hr_recruitment.refuse_applicant_with_reason.

Open the Senior Platform Engineer kanban, click the target applicant,
click Refuse, choose the refuse reason in the wizard, untick Send Email,
and apply.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    modal_set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


JOB_NAME = "Senior Platform Engineer"
TARGET = "Marcus Whitfield"
EXPECTED_REASON = "Does not fit the job requirements"


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Open the job's applicant kanban by clicking its kanban card
    click_kanban_card(page, JOB_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Open the target applicant
    click_kanban_card(page, TARGET)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Click Refuse button (status bar / header)
    refuse_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Refuse'), "
        ".o_control_panel button:visible:has-text('Refuse'), "
        "button[name='archive_applicant']:visible"
    ).first
    refuse_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Wait for the Refuse Reason wizard modal
    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10_000)
    page.wait_for_timeout(500)

    # Set refuse_reason_id on the wizard
    modal_set_many2one(page, "refuse_reason_id", EXPECTED_REASON)
    page.wait_for_timeout(400)

    # Untick Send Email if checked
    send_mail_cb = modal.locator(
        ".o_field_widget[name='send_mail'] input[type='checkbox']"
    ).first
    if send_mail_cb.count() > 0:
        try:
            if send_mail_cb.is_checked():
                send_mail_cb.click()
                page.wait_for_timeout(300)
        except Exception:
            pass

    # Click the wizard primary button — label varies across versions
    apply_btn = modal.locator(
        "footer button.btn-primary:visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    apply_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
