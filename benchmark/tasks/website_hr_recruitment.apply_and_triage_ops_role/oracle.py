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

    # Enter edit mode on the form page
    # Look for the "Edit" pencil/button in the website top bar
    edit_btn = page.locator(
        "a[data-action='edit']:visible, "
        "button[data-action='edit']:visible, "
        ".o_edit_website_container a:visible, "
        "a.btn:has-text('Edit'):visible"
    ).first
    edit_btn.click()
    page.wait_for_timeout(3000)
    # Wait for editor to load
    page.wait_for_selector("#oe_snippets, .o_we_website_top_actions", timeout=20000)
    page.wait_for_timeout(2000)

    # -----------------------------------------------------------------
    # Add custom fields via the form builder
    # In the Odoo website form editor, we need to add fields.
    # Click on the form to select it, then use the "Add a field" option
    # from the right-side snippet options panel.
    # -----------------------------------------------------------------

    # Click on the form element to select it in the editor
    form_el = page.locator(
        ".s_website_form form, "
        "form.o_mark_required, "
        ".s_website_form"
    ).first
    form_el.click()
    page.wait_for_timeout(1000)

    # Look for "Add a field" or the field addition mechanism in the editor panel
    # The website form builder has a "+" or "Add a field" button in the
    # customize panel on the right side
    add_field_btn = page.locator(
        "we-button:has-text('Add a field'), "
        ".o_we_customize_panel button:has-text('Add'), "
        "we-button[data-add-field], "
        ".snippet-option-WebsiteFormEditor we-button:has-text('Field'), "
        "we-button:has-text('+ Field')"
    ).first
    add_field_btn.click()
    page.wait_for_timeout(1000)

    # A modal or panel should appear to configure the new field
    # Set the field label to "Referral Code"
    # The exact UI depends on Odoo version -- typically a modal with label input
    label_input = page.locator(
        ".modal:visible input[name='label'], "
        ".modal:visible input.o_we_field_label, "
        ".o_we_customize_panel input[data-set-label], "
        ".modal:visible input"
    ).first
    label_input.fill("")
    label_input.fill("Referral Code")
    page.wait_for_timeout(500)

    # Confirm the field addition
    confirm_btn = page.locator(
        ".modal:visible button.btn-primary, "
        ".modal:visible button:has-text('Save'), "
        ".modal:visible button:has-text('Add'), "
        ".modal:visible button:has-text('Confirm')"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
        page.wait_for_timeout(1000)

    # Now add the second field: "Implementation Notes"
    # Re-click form and add another field
    form_el = page.locator(
        ".s_website_form form, "
        "form.o_mark_required, "
        ".s_website_form"
    ).first
    form_el.click()
    page.wait_for_timeout(500)

    add_field_btn = page.locator(
        "we-button:has-text('Add a field'), "
        ".o_we_customize_panel button:has-text('Add'), "
        "we-button[data-add-field], "
        ".snippet-option-WebsiteFormEditor we-button:has-text('Field'), "
        "we-button:has-text('+ Field')"
    ).first
    add_field_btn.click()
    page.wait_for_timeout(1000)

    label_input = page.locator(
        ".modal:visible input[name='label'], "
        ".modal:visible input.o_we_field_label, "
        ".o_we_customize_panel input[data-set-label], "
        ".modal:visible input"
    ).first
    label_input.fill("")
    label_input.fill("Implementation Notes")
    page.wait_for_timeout(500)

    confirm_btn = page.locator(
        ".modal:visible button.btn-primary, "
        ".modal:visible button:has-text('Save'), "
        ".modal:visible button:has-text('Add'), "
        ".modal:visible button:has-text('Confirm')"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
        page.wait_for_timeout(1000)

    # Save the website editor changes
    save_page = page.locator(
        "button[data-action='save']:visible, "
        ".o_we_website_top_actions button:has-text('Save'):visible, "
        "button.btn-primary:has-text('Save'):visible"
    ).first
    save_page.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # =====================================================================
    # Phase 2: Submit application for Customer Success Specialist
    # =====================================================================

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
    # They may appear as inputs with the label text or a slugified name
    referral_input = page.locator(
        "input[name='Referral Code'], "
        "input[name='referral_code'], "
        "input[name='Referral code'], "
        ".s_website_form_field:has-text('Referral Code') input, "
        ".s_website_form_field:has-text('Referral Code') textarea"
    ).first
    referral_input.fill("CUST-REF-27")

    impl_input = page.locator(
        "input[name='Implementation Notes'], "
        "input[name='implementation_notes'], "
        "input[name='Implementation notes'], "
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

    # Set Evaluation to "Excellent" (priority field = 3 stars)
    # In Odoo, the priority widget uses star icons. "Excellent" = 3 stars.
    # Click the 3rd star in the priority widget.
    stars = page.locator(
        ".o_field_widget[name='priority'] .o_priority_star, "
        ".o_field_widget[name='priority'] a"
    )
    # Click the 3rd star (index 2) for "Excellent"
    stars.nth(2).click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Save
    save_form(page)
    page.wait_for_timeout(1000)


run_oracle(oracle)
