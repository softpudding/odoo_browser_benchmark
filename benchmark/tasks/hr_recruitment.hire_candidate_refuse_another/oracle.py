"""Oracle for hr_recruitment.hire_candidate_refuse_another.

Executes both sub-flows in order:
 1. Open Bench Role -> open Top Candidate -> click Contract Signed in
    the form status bar (hired stage) -> click Create Employee ->
    save the pre-filled employee form.
 2. Go back to Bench Role applications -> open Runner Up -> click
    Refuse in the form header -> in the wizard pick the 'Not a fit'
    badge and ensure Send Email is off -> click the primary Refuse
    button.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_for_ready,
    _wait_no_loading,
)


JOB_NAME = "Bench Role"
TOP_NAME = "Top Candidate"
RUNNER_NAME = "Runner Up"
HIRED_STAGE = "Contract Signed"
REFUSE_REASON = "Not a fit"
EMPLOYEE_JOB_TITLE = "Bench Role (Hired)"


def _goto_job_applications(page):
    navigate(page, "/odoo/recruitment")
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Home kanban shows hr.job cards; click the Bench Role card body.
    page.wait_for_selector(
        f".o_kanban_record:has-text('{JOB_NAME}')", timeout=15000
    )
    card = page.locator(
        f".o_kanban_record:has-text('{JOB_NAME}')"
    ).first
    card.scroll_into_view_if_needed()
    # Click the visible label (card main body). The 3-dot menu lives in a
    # separate top-right corner so this click reliably fires
    # action_hr_job_applications.
    label = card.locator(
        "a, button, span, div"
    ).filter(has_text=JOB_NAME).first
    label.click()
    page.wait_for_timeout(1200)
    _wait_for_ready(page)
    _wait_no_loading(page)
    # Wait for either the kanban or list of applicants.
    page.wait_for_selector(
        ".o_kanban_view, .o_list_view", timeout=15000
    )
    page.wait_for_timeout(400)


def _open_applicant(page, name):
    # In kanban the applicants are grouped by stage; just find any card
    # with the applicant's name and click it.
    selector_kanban = (
        f".o_kanban_view .o_kanban_record:has-text('{name}')"
    )
    selector_list = (
        f".o_list_view .o_data_row:has-text('{name}')"
    )
    card = page.locator(selector_kanban).first
    if card.count() == 0:
        card = page.locator(selector_list).first
    card.wait_for(state="visible", timeout=10000)
    card.scroll_into_view_if_needed()
    card.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    _wait_no_loading(page)
    # Wait until the form has rendered the header buttons.
    page.wait_for_selector(
        ".o_form_view .o_statusbar_status, .o_form_view .o_form_statusbar",
        timeout=15000,
    )
    page.wait_for_timeout(400)


def _click_statusbar_stage(page, stage_name):
    # The status bar renders stage pills as buttons (rotting_statusbar_duration
    # with clickable=1). We click the first visible button containing the
    # stage label.
    btn = page.locator(
        ".o_statusbar_status button:visible, "
        ".o_arrow_button:visible, "
        ".o_statusbar_status .btn:visible"
    ).filter(has_text=stage_name).first
    btn.wait_for(state="visible", timeout=10000)
    btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _click_create_employee(page):
    # After hitting the hired stage, the header button becomes visible.
    btn = page.locator(
        "button[name='create_employee_from_applicant']:visible, "
        ".o_statusbar_buttons button:has-text('Create Employee'):visible, "
        ".o_control_panel button:has-text('Create Employee'):visible, "
        "button.o_create_employee:visible"
    ).first
    btn.wait_for(state="visible", timeout=10000)
    btn.click()
    # Wait for the employee form to render.
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    _wait_no_loading(page)
    # Employee form has breadcrumb containing TOP_NAME and name field.
    page.wait_for_selector(
        ".o_form_view .o_field_widget[name='name']", timeout=15000
    )
    page.wait_for_timeout(400)


def _set_employee_job_title(page, title):
    # On the pre-filled employee form the job_title field is under the
    # employee's name. Find the input, clear, re-type the target title.
    inp = page.locator(
        ".o_form_view .o_field_widget[name='job_title'] input:visible, "
        ".o_form_view input[name='job_title']:visible"
    ).first
    inp.wait_for(state="visible", timeout=10000)
    inp.click()
    inp.press("Control+a")
    try:
        inp.press("Meta+a")
    except Exception:
        pass
    inp.fill("")
    inp.type(title, delay=15)
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _save_form(page):
    # Cloud/save icon — or press Ctrl+S as fallback.
    save_btn = page.locator(
        ".o_control_panel button.o_form_button_save:visible, "
        ".o_form_button_save:visible, "
        "button.fa-cloud-upload:visible"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    else:
        page.keyboard.press("Control+s")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


def _click_refuse_and_apply(page):
    # Header Refuse button.
    refuse_btn = page.locator(
        "button[name='archive_applicant']:visible, "
        ".o_statusbar_buttons button:has-text('Refuse'):visible, "
        ".o_control_panel button:has-text('Refuse'):visible"
    ).first
    refuse_btn.wait_for(state="visible", timeout=10000)
    refuse_btn.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Wizard modal.
    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=10000)
    page.wait_for_timeout(400)

    # Pick the 'Not a fit' selection_badge — exact match via has_text.
    badge = modal.locator(
        ".o_field_selection_badge[name='refuse_reason_id'] .o_selection_badge, "
        ".o_field_widget[name='refuse_reason_id'] .o_selection_badge"
    ).filter(has_text=REFUSE_REASON).first
    badge.wait_for(state="visible", timeout=8000)
    badge.click()
    page.wait_for_timeout(400)

    # Ensure Send Email toggle is off (to avoid mail assertion surprises).
    send_mail_cb = modal.locator(
        ".o_field_widget[name='send_mail'] input[type='checkbox']"
    ).first
    try:
        if send_mail_cb.count() > 0 and send_mail_cb.is_checked():
            send_mail_cb.click()
            page.wait_for_timeout(300)
    except Exception:
        pass

    # Click the wizard primary Refuse button.
    apply_btn = modal.locator(
        "footer button.btn-primary:visible, "
        ".modal-footer button.btn-primary:visible, "
        "button[name='action_refuse_reason_apply']:visible"
    ).first
    apply_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


def oracle(page):
    login(page)

    # --- Hire Top Candidate ---
    _goto_job_applications(page)
    _open_applicant(page, TOP_NAME)
    _click_statusbar_stage(page, HIRED_STAGE)
    _click_create_employee(page)
    _set_employee_job_title(page, EMPLOYEE_JOB_TITLE)
    _save_form(page)

    # --- Refuse Runner Up ---
    _goto_job_applications(page)
    _open_applicant(page, RUNNER_NAME)
    _click_refuse_and_apply(page)

    page.wait_for_timeout(600)
    _wait_no_loading(page)


run_oracle(oracle)
