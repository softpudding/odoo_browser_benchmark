"""Oracle for website_hr_recruitment.apply_and_triage_ops_role.

Complex multi-phase task:
1. Navigate /jobs, find "Platform Support Specialist" (mentions pager rotation)
2. Open its application form in edit mode, add custom fields
   "Referral Code" and "Implementation Notes"
3. Save and leave edit mode
4. Navigate /jobs, find "Customer Success Specialist" (mentions renewals)
5. Submit application with specified data
6. Open Recruitment backend, find Jack Doe, set stage + evaluation
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_selection,
    full_url,
    _wait_no_loading,
    _wait_for_ready,
)


def _add_custom_field(page, iframe, label_text):
    """Click a form field, press '+ Field', and set its label."""
    # Click an existing form field to ensure the form snippet is selected
    field = iframe.locator(".s_website_form_field").first
    field.click()
    page.wait_for_timeout(1500)

    # Click "+ Field" button in the builder sidebar
    page.locator("button:has-text('+ Field')").first.click()
    page.wait_for_timeout(2000)

    # Find the Label row in the sidebar (shows "Custom Text" for new fields)
    hb_rows = page.locator(".o-website-builder_sidebar .hb-row")
    for i in range(hb_rows.count()):
        text = hb_rows.nth(i).inner_text().strip()
        inp = hb_rows.nth(i).locator("input")
        if text.startswith("Label") and inp.count() > 0:
            val = inp.first.input_value()
            if val == "Custom Text":
                inp.first.click()
                inp.first.fill("")
                inp.first.fill(label_text)
                inp.first.press("Enter")
                page.wait_for_timeout(1000)
                return
    raise RuntimeError(f"Could not find Label row to set '{label_text}'")


def oracle(page):
    login(page)

    # =====================================================================
    # Phase 1: Add custom fields to Platform Support Specialist form
    # =====================================================================

    # Go to /jobs to find Platform Support Specialist
    page.goto(full_url("/jobs"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Platform Support Specialist" (the one mentioning pager rotation)
    page.locator("a:has-text('Platform Support Specialist')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Apply Now" to reach the application form
    page.locator("a:has-text('Apply'), button:has-text('Apply')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Get the current path for the editor
    from urllib.parse import urlparse, quote
    parsed = urlparse(page.url)
    path = parsed.path  # e.g., /jobs/platform-support-specialist-0/apply

    # Navigate to the backend website editor for this page
    editor_url = (
        f"/odoo/action-website.website_preview"
        f"?path={quote(path, safe='')}&enable_editor=1"
    )
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the editor save button to appear
    page.wait_for_selector("[data-action='save']", timeout=30000)
    page.wait_for_timeout(3000)

    iframe = page.frame_locator("iframe:not(.o_ignore_in_tour)")

    # Add "Referral Code" custom field
    _add_custom_field(page, iframe, "Referral Code")

    # Add "Implementation Notes" custom field
    _add_custom_field(page, iframe, "Implementation Notes")

    # Save the website editor changes
    page.locator("[data-action='save']").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    _wait_no_loading(page)

    # =====================================================================
    # Phase 2: Submit application for Customer Success Specialist
    # =====================================================================

    # Go to /jobs
    page.goto(full_url("/jobs"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Customer Success Specialist" (mentions renewals)
    page.locator("a:has-text('Customer Success Specialist')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Apply Now"
    page.locator("a:has-text('Apply'), button:has-text('Apply')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Fill in the application form (public website form, HTML inputs)
    page.locator("input[name='partner_name']").first.fill("Jack Doe")
    page.locator("input[name='email_from']").first.fill("jack@doe.com")
    page.locator("input[name='partner_phone']").first.fill("118.712")
    page.locator("input[name='linkedin_profile']").first.fill(
        "linkedin.com/in/jack-doe"
    )

    # Short introduction
    page.locator("textarea[name='short_introduction']").first.fill(
        "### [CS-SPECIALIST] HR TEST ###"
    )

    # Custom fields added in Phase 1 (name attribute matches the label)
    page.locator("input[name='Referral Code']").first.fill("CUST-REF-27")
    page.locator("input[name='Implementation Notes']").first.fill(
        "Escalate onboarding blockers"
    )

    # Submit (button text is "I'm feeling lucky", class s_website_form_send)
    page.locator(".s_website_form_send").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)

    # =====================================================================
    # Phase 3: Backend -- triage Jack Doe's application
    # =====================================================================

    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Find "Customer Success Specialist" job and open it
    click_kanban_card(page, "Customer Success Specialist")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Find Jack Doe's application card and open it
    jack_card = page.locator(
        ".o_kanban_record:has-text('Jack Doe'), "
        ".o_data_row:has-text('Jack Doe')"
    ).first
    jack_card.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Set Stage to "Qualification" via the status bar
    page.locator(
        ".o_statusbar_status button:has-text('Qualification'), "
        ".o_statusbar_status .o_arrow_button:has-text('Qualification')"
    ).first.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Set Evaluation to "Excellent" (priority field = 3 stars).
    # Click the 3rd star in the priority widget.
    stars = page.locator(
        ".o_field_widget[name='priority'] .o_priority_star, "
        ".o_field_widget[name='priority'] a"
    )
    if stars.count() >= 3:
        stars.nth(2).click()
    else:
        stars.last.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save
    save_form(page)
    page.wait_for_timeout(1000)


run_oracle(oracle)
