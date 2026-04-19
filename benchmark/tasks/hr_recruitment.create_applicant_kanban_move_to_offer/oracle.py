"""Oracle for hr_recruitment.create_applicant_kanban_move_to_offer.

Opens the Recruitment kanban, clicks 'Bench Senior Dev' to enter its
Applications kanban (grouped by stage), creates a new applicant in the
'Initial Qualification' column via the kanban quick-create, opens the
resulting card's full form to fill email_from + partner_phone, saves,
then advances the applicant's stage via the form status bar:
Initial Qualification -> Qualified -> Contract Proposal.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


JOB_NAME = "Bench Senior Dev"
APPLICANT_NAME = "Alice Applicant"
EMAIL = "alice@bench.test"
PHONE = "+15555555555"
FIRST_STAGE = "Initial Qualification"
TARGET_STAGES_ORDER = ["Qualified", "Contract Proposal"]


def _open_job_applications(page):
    navigate(page, "/odoo/recruitment")
    _wait_for_ready(page)
    _wait_no_loading(page)

    # The recruitment home is a kanban of hr.job cards. Each card is a
    # clickable action that opens the Applications kanban. Clicking the
    # card title / job-name anywhere on the card navigates there.
    page.wait_for_selector(
        f".o_kanban_record:has-text('{JOB_NAME}')", timeout=15000
    )
    card = page.locator(
        f".o_kanban_record:has-text('{JOB_NAME}')"
    ).first
    card.scroll_into_view_if_needed()

    # Click the applicants-count label (it's the only consistently
    # navigable click target; the card root has the same action but may
    # be intercepted by the 3-dot menu overlay).
    app_label = card.locator(
        "a, button, span, div"
    ).filter(has_text=JOB_NAME).first
    app_label.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Confirm we're in the applicant kanban (grouped by stage).
    page.wait_for_selector(
        ".o_kanban_view .o_kanban_group", timeout=15000
    )
    page.wait_for_timeout(500)


def _quick_create_applicant(page):
    """Click '+' on the first stage column and enter partner_name."""
    first_col = page.locator(
        f".o_kanban_group:has(.o_column_title:has-text('{FIRST_STAGE}'))"
    ).first
    first_col.wait_for(state="visible", timeout=10000)
    first_col.scroll_into_view_if_needed()

    # The per-column quick-create button is `.o_kanban_quick_add i.fa-plus`
    # or `button.o_kanban_quick_add` in the column header.
    add_btn = first_col.locator(
        ".o_kanban_quick_add, "
        "button.o_kanban_quick_add, "
        ".o_kanban_header button:has(i.fa-plus), "
        ".o_column_title ~ * button:has(i.fa-plus)"
    ).first
    add_btn.click()
    page.wait_for_timeout(700)
    _wait_no_loading(page)

    # The quick-create form renders at the top of the column with a
    # partner_name input.
    name_input = page.locator(
        ".o_kanban_quick_create .o_field_widget[name='partner_name'] input:visible"
    ).first
    name_input.wait_for(state="visible", timeout=5000)
    name_input.click()
    name_input.fill(APPLICANT_NAME)
    page.wait_for_timeout(300)

    # Click the green check / 'Add' button inside the quick-create to save.
    add_save_btn = page.locator(
        ".o_kanban_quick_create button.o_kanban_add, "
        ".o_kanban_quick_create button:has-text('Add'):visible"
    ).first
    add_save_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def _open_new_applicant_form(page):
    """Click on the newly-created Alice Applicant card to open the form."""
    card = page.locator(
        f".o_kanban_view .o_kanban_record:has-text('{APPLICANT_NAME}')"
    ).first
    card.wait_for(state="visible", timeout=10000)
    card.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    _wait_no_loading(page)
    # Wait until the form is clearly rendered
    page.wait_for_selector(".o_form_view .o_field_widget[name='email_from']", timeout=10000)


def _fill_contact_details(page):
    email_inp = page.locator(
        ".o_form_view .o_field_widget[name='email_from'] input:visible"
    ).first
    email_inp.click()
    email_inp.fill(EMAIL)
    email_inp.press("Tab")
    page.wait_for_timeout(400)

    phone_inp = page.locator(
        ".o_form_view .o_field_widget[name='partner_phone'] input:visible"
    ).first
    phone_inp.click()
    phone_inp.fill(PHONE)
    phone_inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _save_form(page):
    # Click the save button in the control panel (cloud icon)
    save_btn = page.locator(
        ".o_control_panel button.o_form_button_save:visible, "
        ".o_form_button_save:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
        page.wait_for_timeout(800)
    else:
        # Fallback: press Ctrl+S
        page.keyboard.press("Control+s")
        page.wait_for_timeout(800)
    _wait_no_loading(page)


def _advance_stage(page, stage_name):
    """Click the given stage button on the form status bar."""
    # status bar buttons in Odoo 19 for stage_id with clickable=True render
    # as `.o_statusbar_status button[data-value=...]` with the stage name.
    btn = page.locator(
        ".o_statusbar_status button:visible, "
        ".o_arrow_button:visible, "
        ".o_statusbar_status .btn:visible"
    ).filter(has_text=stage_name).first
    btn.wait_for(state="visible", timeout=10000)
    btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    _open_job_applications(page)
    _quick_create_applicant(page)
    _open_new_applicant_form(page)
    _fill_contact_details(page)
    _save_form(page)

    for stage in TARGET_STAGES_ORDER:
        _advance_stage(page, stage)

    _save_form(page)
    page.wait_for_timeout(600)
    _wait_no_loading(page)


run_oracle(oracle)
