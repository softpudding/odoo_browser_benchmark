"""Oracle for website_hr_recruitment.set_kanban_state_assign_recruiter.

Open Recruitment, click the 'Senior QA Engineer' job kanban card, open
applicant 'Diana Recruit', flip the kanban_state status ball to
'Ready for Next Stage', set the recruiter to 'Recruiter Bob', post an
internal Log note 'Phone screen done.', save.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


JOB_NAME = "Senior QA Engineer"
APPLICANT_NAME = "Diana Recruit"
RECRUITER_NAME = "Recruiter Bob"
NOTE_TEXT = "Phone screen done."


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # Open the job's applicant kanban.
    click_kanban_card(page, JOB_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Open Diana's applicant card.
    click_kanban_card(page, APPLICANT_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(700)

    # ------------------------------------------------------------------
    # 1. Click the kanban_state ball, then "Ready for Next Stage"
    # ------------------------------------------------------------------
    state_widget = page.locator(
        ".o_field_widget[name='kanban_state']"
    ).first
    state_widget.scroll_into_view_if_needed()
    page.wait_for_timeout(200)

    # The widget renders as a small button containing an o_status span.
    state_btn = state_widget.locator("button").first
    state_btn.click()
    page.wait_for_timeout(500)

    # Dropdown menu is appended to the body (not the widget) — locate by
    # the .state_selection_field_menu class set on the dropdown.
    menu_item = page.locator(
        ".state_selection_field_menu .dropdown-item:has-text('Ready for Next Stage'), "
        ".o-dropdown--menu .dropdown-item:has-text('Ready for Next Stage'), "
        ".o-dropdown--menu :text('Ready for Next Stage')"
    ).first
    menu_item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # 2. Recruiter many2one
    # ------------------------------------------------------------------
    set_many2one(page, "user_id", RECRUITER_NAME)
    page.wait_for_timeout(500)

    # ------------------------------------------------------------------
    # 3. Save the field changes BEFORE posting the note.  Some chatter
    #    composers refuse to post on an unsaved record; saving first is
    #    the cleanest path.
    # ------------------------------------------------------------------
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # 4. Post an internal Log note 'Phone screen done.'
    # ------------------------------------------------------------------
    log_note_btn = page.locator(
        "button.o-mail-Chatter-logNote:visible, "
        "button:has-text('Log note'):visible, "
        ".o-mail-Chatter button:has-text('Log note'):visible"
    ).first
    log_note_btn.scroll_into_view_if_needed()
    log_note_btn.click()
    page.wait_for_timeout(800)

    note_input = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-Composer [contenteditable='true'], "
        "div[contenteditable='true'].odoo-editor-editable"
    ).last
    note_input.click()
    page.wait_for_timeout(200)
    note_input.fill(NOTE_TEXT)
    page.wait_for_timeout(300)

    add_btn = page.locator(
        "button.o-mail-Composer-send:visible, "
        ".o-mail-Composer button:has-text('Log'):visible, "
        ".o-mail-Composer button:has-text('Send'):visible"
    ).first
    add_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
