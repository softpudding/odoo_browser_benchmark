"""Oracle for website_hr_recruitment.apply_public_then_schedule_interview.

Pure Playwright UI oracle — proves the task is solvable via the browser:

  Phase 1 — Public website (no login):
    1. Navigate to /jobs.
    2. Open the "Senior Backend Engineer" posting.
    3. Click Apply and fill the public application form.
    4. Submit via the .s_website_form_send button.

  Phase 2 — Back-office (admin login):
    5. Log in as admin and open /odoo/recruitment.
    6. Open the "Senior Backend Engineer" job pipeline.
    7. Open Bench Candidate's kanban card.
    8. Open the Activities button in the chatter, click the "Meeting" badge,
       click Schedule to land on the calendar, then create a new
       calendar.event named "Interview" on 2026-05-04. Saving the event
       creates a linked mail.activity with
           summary="Interview", activity_type_id=Meeting,
           date_deadline=2026-05-04, res_model=hr.applicant.

In Odoo 19, picking "Meeting" hides the summary / date_deadline inputs on
the schedule-activity wizard and routes the user through the calendar so
the activity's summary/date are derived from the calendar event.
"""

from benchmark.oracle_helpers import (
    DB,
    click_kanban_card,
    full_url,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


JOB_NAME = "Senior Backend Engineer"
APPLICANT_NAME = "Bench Candidate"
APPLICANT_EMAIL = "bench.candidate@example.com"
APPLICANT_PHONE = "+1 555 0143"
APPLICANT_LINKEDIN = "linkedin.com/in/bench-candidate"
APPLICANT_INTRO = "Excited to interview for the Senior Backend Engineer role."
ACTIVITY_SUMMARY = "Interview"
TARGET_MONTH_LABEL = "May 2026"
TARGET_DAY = "4"


def _submit_public_application(page):
    portal_url = "/jobs"
    if DB:
        portal_url = f"/jobs?db={DB}"
    page.goto(full_url(portal_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click the job link.
    job_link = page.locator(f"a:has-text('{JOB_NAME}')").first
    job_link.wait_for(timeout=15000)
    job_link.scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    job_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2500)

    # Click Apply / Apply Now.
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

    page.wait_for_selector(
        "input[name='partner_name'], form#hr_recruitment_form",
        timeout=15000,
    )

    page.locator("input[name='partner_name']").first.fill(APPLICANT_NAME)
    page.locator("input[name='email_from']").first.fill(APPLICANT_EMAIL)
    page.locator("input[name='partner_phone']").first.fill(APPLICANT_PHONE)

    linkedin_input = page.locator("input[name='linkedin_profile']")
    if linkedin_input.count() > 0:
        linkedin_input.first.fill(APPLICANT_LINKEDIN)

    intro_textarea = page.locator("textarea[name='short_introduction']")
    if intro_textarea.count() > 0:
        intro_textarea.first.fill(APPLICANT_INTRO)
    page.wait_for_timeout(500)

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

    # Soft-wait for a confirmation signal.
    try:
        page.wait_for_selector(
            ".s_website_form_end_message:visible, "
            "span:has-text('Thank'):visible, "
            "h1:has-text('Congratulations'):visible, "
            "div:has-text('application has been'):visible",
            timeout=10000,
        )
    except Exception:
        pass


def _open_applicant(page):
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Open the job's applicant pipeline, then the applicant card.
    click_kanban_card(page, JOB_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    click_kanban_card(page, APPLICANT_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(1500)


def _open_schedule_activity_modal(page):
    chatter = page.locator(".o-mail-Chatter, .o_chatter")
    if chatter.count() > 0:
        chatter.first.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

    activity_btn = page.locator(
        "button.o-mail-Chatter-activity:visible, "
        ".o-mail-Chatter button:has-text('Activities'):visible, "
        ".o-mail-Chatter button:has-text('Activity'):visible"
    )
    if activity_btn.count() == 0:
        activity_btn = page.locator("button.o-mail-Chatter-activity")
    activity_btn.first.click()
    page.wait_for_timeout(2000)

    page.wait_for_selector(".modal:visible", timeout=15000)


def _pick_meeting_type_and_schedule(page):
    modal = page.locator(".modal:visible").last
    # In Odoo 19 the activity_type is a row of selection badges.
    meeting_badge = modal.locator(
        ".o_field_widget[name='activity_type_id'] "
        ".o_selection_badge:has-text('Meeting')"
    )
    meeting_badge.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # After picking Meeting, the only visible action is "Schedule".
    modal = page.locator(".modal:visible").last
    schedule_btn = modal.locator(
        "button[name='action_create_calendar_event']:visible, "
        ".modal-footer button.btn-primary:visible"
    ).first
    schedule_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(4000)
    _wait_no_loading(page)


def _create_calendar_event(page):
    # We are now on the applicant's calendar for the meeting activity.
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # Event title.
    name_inp = page.locator(
        ".o_field_widget[name='name'] input, "
        ".o_field_widget[name='name'] textarea"
    ).first
    name_inp.click()
    name_inp.fill(ACTIVITY_SUMMARY)
    page.wait_for_timeout(500)

    # Toggle "All day" so we only pick a date (no time component).
    allday = page.locator(
        ".o_field_widget[name='allday'] input[type='checkbox']"
    ).first
    if not allday.is_checked():
        allday.click()
        page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Open the start_date picker (button-based date range widget).
    start_btn = page.locator("button[data-field='start_date']").first
    start_btn.click()
    page.wait_for_timeout(1200)

    # Navigate the popover calendar to the target month.
    for _ in range(36):
        header = page.locator(
            ".o_datetime_picker_header .o_header_part"
        ).first
        current = header.inner_text().strip() if header.count() > 0 else ""
        if current == TARGET_MONTH_LABEL:
            break
        page.locator(".o_datetime_picker .o_next:visible").first.click()
        page.wait_for_timeout(350)

    # Click the target day cell (must match exactly to avoid 14/24/etc.).
    day_cells = page.locator(".o_date_picker .o_date_item_cell")
    clicked = False
    for i in range(day_cells.count()):
        cell = day_cells.nth(i)
        if cell.inner_text().strip() == TARGET_DAY:
            cls = cell.get_attribute("class") or ""
            if "o_out_of_range" in cls:
                continue
            cell.click()
            clicked = True
            break
    if not clicked:
        raise RuntimeError(
            f"Could not find day '{TARGET_DAY}' in month '{TARGET_MONTH_LABEL}'"
        )
    page.wait_for_timeout(800)

    save_form(page)
    page.wait_for_timeout(2500)
    _wait_no_loading(page)


def oracle(page):
    # Phase 1 — Public website (no login).
    _submit_public_application(page)

    # Phase 2 — Back-office: log in then schedule the Meeting activity.
    login(page)
    _open_applicant(page)
    _open_schedule_activity_modal(page)
    _pick_meeting_type_and_schedule(page)
    _create_calendar_event(page)


run_oracle(oracle)
