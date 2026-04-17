"""Oracle for hr_recruitment.create_applicant_add_skills_refuse.

Open Recruitment app, click "Senior Data Engineer" job, create a new applicant
Cameron Blake with contact details and responsible. Add a Python/Advanced skill
via the Skills tab. Save, then refuse the applicant with reason and no email.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_kanban_card,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    # Open the Senior Data Engineer job position
    click_kanban_card(page, "Senior Data Engineer")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Create a new applicant
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Fill applicant fields
    fill_field(page, "partner_name", "Cameron Blake")
    page.wait_for_timeout(500)

    fill_field(page, "email_from", "cameron.blake@techmail.example.com")
    page.wait_for_timeout(500)

    fill_field(page, "partner_phone", "+1 555 0147")
    page.wait_for_timeout(500)

    set_many2one(page, "user_id", "Administrator")
    page.wait_for_timeout(500)

    # Go to Skills tab and add a skill
    click_tab(page, "Skills")
    page.wait_for_timeout(800)

    # Click "Pick a skill from the list" button to open the skill picker modal
    page.get_by_role("button", name="Pick a skill from the list").click()
    page.wait_for_timeout(1000)

    modal = page.locator(".modal:visible").last
    if modal.count() > 0:
        # Select skill type: Languages
        modal.locator(
            ".o_field_widget[name='skill_type_id'] .o_selection_badge:has-text('Languages')"
        ).first.click()
        page.wait_for_timeout(400)

        # Select skill: Python
        modal.locator(
            ".o_field_widget[name='skill_id'] .o_selection_badge:has-text('Python')"
        ).first.click()
        page.wait_for_timeout(400)

        # Select skill level: Advanced
        modal.locator(
            ".o_field_widget[name='skill_level_id'] .o_selection_badge:has-text('Advanced')"
        ).first.click()
        page.wait_for_timeout(400)

        # Save the skill modal
        modal.locator(
            ".modal-footer button.o_form_button_save, .modal-footer button.btn-primary"
        ).first.click()
        page.wait_for_timeout(1200)
        _wait_no_loading(page)

    # Save the applicant form
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Refuse button in the status bar
    refuse_btn = page.locator(
        ".o_statusbar_buttons button:visible:has-text('Refuse'), "
        ".o_control_panel button:visible:has-text('Refuse'), "
        "button[name='archive_applicant']:visible"
    ).first
    refuse_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Handle the Refuse Reason wizard modal
    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10_000)
    page.wait_for_timeout(500)

    # Set refuse reason via selection badge
    modal.locator(
        ".o_field_selection_badge[name='refuse_reason_id'] .o_selection_badge, "
        ".o_field_widget[name='refuse_reason_id'] .o_selection_badge"
    ).filter(has_text="Does not fit the job requirements").first.click()
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

    # Click the Refuse button in the wizard footer
    apply_btn = modal.locator(
        "footer button.btn-primary:visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    apply_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
