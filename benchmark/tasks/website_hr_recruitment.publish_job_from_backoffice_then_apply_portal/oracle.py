"""Oracle for website_hr_recruitment.publish_job_from_backoffice_then_apply_portal.

Two phases:
  1. Back-office: create + publish "Senior Widget Engineer".
  2. Public portal: navigate to /jobs and submit the application form.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
    DB,
)


JOB_NAME = "Senior Widget Engineer"
APPLICANT_NAME = "Alex Portal"
APPLICANT_EMAIL = "alex.portal@example.com"
APPLICANT_PHONE = "+1 555 0199"
APPLICANT_LINKEDIN = "linkedin.com/in/alex-portal"
APPLICANT_INTRO = "Excited to apply for this role."
JOB_DESCRIPTION = "Design and build widgets. Remote-friendly."


def _activate_details_tab(page):
    """Activate the Details / Recruitment tab so the standard fields are visible."""
    details_tab = page.locator(
        ".o_notebook .nav-link:has-text('Details'), "
        ".o_notebook .nav-link:has-text('Recruitment')"
    ).first
    if details_tab.count() > 0 and details_tab.is_visible():
        try:
            details_tab.click()
            page.wait_for_timeout(500)
        except Exception:
            pass


def oracle(page):
    # =======================================================================
    # Phase 1 — Back-office: create the job
    # =======================================================================
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Click "New" on the recruitment kanban — this opens a simple modal
    # asking for just the name + alias.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # If a modal opens (simple form), fill the name and click Create.
    modal = page.locator(".modal:visible")
    opened_modal = modal.count() > 0
    if opened_modal:
        modal_name = modal.locator(
            "input.o_job_name, "
            ".o_field_widget[name='name'] input, "
            ".o_field_widget[name='name'] textarea"
        ).first
        modal_name.click()
        modal_name.fill(JOB_NAME)
        page.wait_for_timeout(500)
        # Click "Create" in the modal footer
        create_btn = modal.locator(
            "button:has-text('Create'):visible, "
            "button.o_create_job:visible"
        ).first
        create_btn.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(2500)
        _wait_no_loading(page)

        # We're now on the applications kanban. Go back to the recruitment
        # main and click Configure on the new job card.
        navigate(page, "/odoo/recruitment")
        _wait_no_loading(page)
        page.wait_for_timeout(1500)

        job_card = page.locator(
            f".o_kanban_record:has-text('{JOB_NAME}')"
        ).first
        job_card.wait_for(timeout=10000)
        configure_btn = job_card.locator("button:has-text('Configure')").first
        configure_btn.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(2000)
        _wait_no_loading(page)
    else:
        # If no modal, the "New" button took us directly to a form view.
        name_input = page.locator(
            ".o_field_widget[name='name'] textarea, "
            ".o_field_widget[name='name'] input"
        ).first
        name_input.click()
        name_input.fill(JOB_NAME)
        page.wait_for_timeout(500)

    # Now we're on the full job form view. Activate Details tab so we can
    # see department_id, no_of_recruitment, website_published toggle.
    _activate_details_tab(page)

    # Set Department to Administration.
    set_many2one(page, "department_id", "Administration")
    page.wait_for_timeout(500)

    # Set Target (no_of_recruitment) to 2.
    target_input = page.locator(
        ".o_field_widget[name='no_of_recruitment'] input"
    ).first
    target_input.click()
    target_input.fill("")
    target_input.fill("2")
    target_input.press("Tab")
    page.wait_for_timeout(500)

    # Toggle website_published while we're still on the Details tab.
    publish_cb = page.locator(
        ".o_field_boolean_toggle[name='website_published'] input, "
        ".o_field_widget[name='website_published'] input[type='checkbox']"
    )
    if publish_cb.count() > 0:
        try:
            checked = publish_cb.first.is_checked()
        except Exception:
            checked = False
        if not checked:
            try:
                publish_cb.first.click()
            except Exception:
                # Fallback: click the visible toggle container/label.
                page.locator(
                    ".o_field_boolean_toggle[name='website_published'], "
                    ".o_field_widget[name='website_published'] .form-check, "
                    ".o_field_widget[name='website_published'] label"
                ).first.click()
            page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Fill the Job Description on the "Job Description" / "Summary" tab.
    desc_tab = page.locator(
        ".o_notebook .nav-link:has-text('Job Description'), "
        ".o_notebook .nav-link:has-text('Summary')"
    ).first
    if desc_tab.count() > 0 and desc_tab.is_visible():
        desc_tab.click()
        page.wait_for_timeout(500)

    desc_field = page.locator(
        ".o_field_widget[name='description'] .note-editable, "
        ".o_field_widget[name='description'] .odoo-editor-editable, "
        ".o_field_widget[name='description'] [contenteditable='true']"
    ).first
    desc_field.click()
    page.wait_for_timeout(300)
    page.keyboard.type(JOB_DESCRIPTION)
    page.wait_for_timeout(500)

    # Save the job
    save_form(page)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # =======================================================================
    # Phase 2 — Portal: navigate to /jobs and apply.
    # =======================================================================
    portal_url = "/jobs"
    if DB:
        portal_url = f"/jobs?db={DB}"
    page.goto(full_url(portal_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2500)

    # Click the "Senior Widget Engineer" link.
    job_link = page.locator(
        f"a:has-text('{JOB_NAME}')"
    ).first
    job_link.wait_for(timeout=15000)
    job_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2500)

    # Click the "Apply Now" / "Apply" button. Filter to only links/buttons
    # whose text actually starts with Apply (not "Apply" elsewhere on page).
    apply_btn = page.locator(
        "a.btn:has-text('Apply'), "
        "a:has-text('Apply Now'), "
        "button:has-text('Apply Now'), "
        "a:has-text('Apply'), button:has-text('Apply')"
    ).first
    apply_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    apply_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the application form to be present.
    page.wait_for_selector(
        "input[name='partner_name'], form#hr_recruitment_form",
        timeout=15000,
    )

    # Fill the public application form.
    page.locator("input[name='partner_name']").first.fill(APPLICANT_NAME)
    page.locator("input[name='email_from']").first.fill(APPLICANT_EMAIL)
    page.locator("input[name='partner_phone']").first.fill(APPLICANT_PHONE)
    page.locator("input[name='linkedin_profile']").first.fill(APPLICANT_LINKEDIN)
    page.locator("textarea[name='short_introduction']").first.fill(APPLICANT_INTRO)
    page.wait_for_timeout(500)

    # Submit — the button is .s_website_form_send. Scroll it into view first.
    send_btn = page.locator(
        ".s_website_form_send:visible, "
        "form#hr_recruitment_form button[type='submit']:visible, "
        "button.s_website_form_send"
    ).first
    try:
        send_btn.scroll_into_view_if_needed()
    except Exception:
        pass
    page.wait_for_timeout(300)
    send_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(6000)

    # Verify confirmation (flexible — either thank-you page redirect or
    # end-message on same page).
    try:
        page.wait_for_selector(
            ".s_website_form_end_message:visible, "
            "span:has-text('Thank'):visible, "
            "h1:has-text('Congratulations'):visible, "
            "div:has-text('application has been'):visible",
            timeout=10000,
        )
    except Exception:
        # If no confirmation element, we assume submission went through
        # and move on — the postconditions will validate the applicant row.
        pass


run_oracle(oracle)
