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


def oracle(page):
    login(page)

    # =====================================================================
    # Phase 1: Add custom fields to Platform Support Specialist form
    # =====================================================================

    # First, go to /jobs to find Platform Support Specialist
    page.goto(full_url("/jobs"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Platform Support Specialist" (the one mentioning pager rotation)
    page.locator("a:has-text('Platform Support Specialist')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Apply Now" to reach the application form
    apply_btn = page.locator("a:has-text('Apply'), button:has-text('Apply')").first
    apply_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Now we're on the public application form page.
    # We need to enter edit mode. The URL is something like /jobs/.../apply
    # We need to go through the backend editor to edit this page.
    # Get the current path for the editor
    current_url = page.url
    from urllib.parse import urlparse, quote
    parsed = urlparse(current_url)
    path = parsed.path  # e.g., /jobs/platform-support-specialist-0/apply

    # Navigate to the backend website editor for this page
    editor_url = f"/odoo/action-website.website_preview?path={quote(path, safe='')}&enable_editor=1"
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the builder sidebar to appear
    page.wait_for_selector(
        ".o-website-builder_sidebar, .o-snippets-menu, "
        "[data-action='save']",
        timeout=30000,
    )
    page.wait_for_timeout(3000)

    # The website form is inside the iframe. Click on the form to select it.
    iframe = page.frame_locator("iframe:not(.o_ignore_in_tour)")

    # Click on a form field to trigger the form builder options
    form_field = iframe.locator(
        ".s_website_form_field, "
        ".s_website_form form .form-group, "
        "form.s_website_form .form-group"
    ).first
    form_field.click()
    page.wait_for_timeout(1000)

    # Now the builder sidebar should show the form field options.
    # Click "+ Field" button in the sidebar to add a new field
    add_field_btn = page.locator(
        ".o-website-builder_sidebar button:has-text('+ Field'), "
        ".o-snippets-menu button:has-text('+ Field'), "
        "button.btn-success:has-text('+ Field')"
    ).first
    add_field_btn.click()
    page.wait_for_timeout(1000)

    # A new field is added. We need to set its label.
    # The field options should now show in the sidebar.
    # Look for the "Label" input in the builder sidebar.
    # The label is set via BuilderTextInput with action "setLabelText"
    label_input = page.locator(
        ".o-website-builder_sidebar input, "
        ".o-snippets-menu input"
    )
    # Find the Label input - it should be near the "Label" text
    # In the builder, there are multiple inputs. We need the Label field.
    # Try to find by looking for the row with "Label" heading
    label_row = page.locator(
        ".o-website-builder_sidebar .hb-row:has-text('Label'), "
        ".o-snippets-menu .hb-row:has-text('Label')"
    ).first
    label_inp = label_row.locator("input").first
    label_inp.click()
    label_inp.fill("")
    label_inp.fill("Referral Code")
    label_inp.press("Enter")
    page.wait_for_timeout(1000)

    # Click the form again to add another field
    form_field = iframe.locator(
        ".s_website_form_field, "
        ".s_website_form form .form-group, "
        "form.s_website_form .form-group"
    ).first
    form_field.click()
    page.wait_for_timeout(1000)

    # Add second field
    add_field_btn = page.locator(
        ".o-website-builder_sidebar button:has-text('+ Field'), "
        ".o-snippets-menu button:has-text('+ Field'), "
        "button.btn-success:has-text('+ Field')"
    ).first
    add_field_btn.click()
    page.wait_for_timeout(1000)

    # Set label to "Implementation Notes"
    label_row = page.locator(
        ".o-website-builder_sidebar .hb-row:has-text('Label'), "
        ".o-snippets-menu .hb-row:has-text('Label')"
    ).first
    label_inp = label_row.locator("input").first
    label_inp.click()
    label_inp.fill("")
    label_inp.fill("Implementation Notes")
    label_inp.press("Enter")
    page.wait_for_timeout(1000)

    # Save the website editor changes
    save_btn = page.locator(
        "button[data-action='save']:visible, "
        ".o-snippets-top-actions button:has-text('Save'):visible, "
        "button.btn-success:has-text('Save'):visible"
    ).first
    save_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    _wait_no_loading(page)

    # =====================================================================
    # Phase 2: Submit application for Customer Success Specialist
    # =====================================================================

    # Go to /jobs as a logged-in user viewing the public page
    page.goto(full_url("/jobs"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Customer Success Specialist" (mentions renewals)
    page.locator("a:has-text('Customer Success Specialist')").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Apply Now"
    apply_btn = page.locator("a:has-text('Apply'), button:has-text('Apply')").first
    apply_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Fill in the application form (public website form, HTML inputs)
    page.locator("input[name='partner_name']").fill("Jack Doe")
    page.locator("input[name='email_from']").fill("jack@doe.com")
    page.locator("input[name='partner_phone']").fill("118.712")

    linkedin_input = page.locator(
        "input[name='linkedin_profile'], "
        "input[name='linkedin']"
    ).first
    linkedin_input.fill("linkedin.com/in/jack-doe")

    # Short introduction
    intro_field = page.locator(
        "textarea[name='description'], "
        "textarea[name='body']"
    ).first
    intro_field.fill("### [CS-SPECIALIST] HR TEST ###")

    # Custom fields added in Phase 1
    # They appear as custom fields with label-based containers
    referral_input = page.locator(
        "input[name='Referral Code'], "
        "input[name='referral_code'], "
        ".s_website_form_field:has-text('Referral Code') input, "
        ".s_website_form_field:has-text('Referral Code') textarea"
    ).first
    referral_input.fill("CUST-REF-27")

    impl_input = page.locator(
        "input[name='Implementation Notes'], "
        "input[name='implementation_notes'], "
        ".s_website_form_field:has-text('Implementation Notes') input, "
        ".s_website_form_field:has-text('Implementation Notes') textarea"
    ).first
    impl_input.fill("Escalate onboarding blockers")

    # Submit
    submit_btn = page.locator(
        "button[type='submit'], "
        "a.btn:has-text('Submit'), "
        "button:has-text('Submit'), "
        ".s_website_form_send"
    ).first
    submit_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

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
    qual_btn = page.locator(
        ".o_statusbar_status button:has-text('Qualification'), "
        ".o_statusbar_status .o_arrow_button:has-text('Qualification')"
    ).first
    qual_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Set Evaluation to "Excellent" (priority field = 3 stars).
    # Click the 3rd star in the priority widget.
    stars = page.locator(
        ".o_field_widget[name='priority'] .o_priority_star, "
        ".o_field_widget[name='priority'] a"
    )
    # Click the 3rd star (index 2) for "Excellent"
    if stars.count() >= 3:
        stars.nth(2).click()
    else:
        # Fallback: click the last star
        stars.last.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save
    save_form(page)
    page.wait_for_timeout(1000)


run_oracle(oracle)
