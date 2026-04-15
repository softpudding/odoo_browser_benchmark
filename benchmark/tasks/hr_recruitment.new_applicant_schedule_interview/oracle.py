"""Oracle for hr_recruitment.new_applicant_schedule_interview.

Open Recruitment app, click "Senior Backend Developer" job, create a new
applicant Elena Vasquez with contact details, recruiter, and expected salary.
Then schedule a Call activity for the first technical interview.
"""

from benchmark.oracle_helpers import (
    click_kanban_card,
    click_create,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    modal_set_many2one,
    modal_fill_field,
    _wait_no_loading,
    _wait_for_ready,
)


def _schedule_call_activity(page, activity_type, summary, due_date, assigned_to):
    """Schedule an activity via the chatter, handling Odoo 19 field names."""
    # Click the activity button in chatter
    activity_btn = page.locator(
        "button.o-mail-Chatter-activity, "
        ".o-mail-Chatter button:has-text('Activity'), "
        "button:has-text('Schedule Activity'), "
        "button.o_ChatterTopbar_activityBtn"
    ).first
    activity_btn.click()
    page.wait_for_timeout(1500)

    # If a dropdown appeared, click "Schedule an activity"
    schedule_link = page.locator(
        "button:has-text('Schedule an activity'), "
        "a:has-text('Schedule an activity')"
    )
    if schedule_link.count() > 0 and page.locator(".modal:visible").count() == 0:
        schedule_link.first.click()
        page.wait_for_timeout(500)

    # Wait for modal
    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    # Set activity type using the selection_badge_icons widget
    # In Odoo 19, activity types are shown as clickable badge buttons
    if activity_type:
        type_widget = modal.locator(".o_field_widget[name='activity_type_id']")
        if type_widget.count() > 0:
            # Click the badge/button that contains the activity type text
            badge = type_widget.locator(f"span:has-text('{activity_type}'), div:has-text('{activity_type}'), button:has-text('{activity_type}')")
            if badge.count() > 0:
                badge.first.click()
            else:
                # Try clicking any element with the text
                type_widget.locator(f":text('{activity_type}')").first.click()
        page.wait_for_timeout(500)

    # Set summary
    if summary:
        modal_fill_field(page, "summary", summary)
        page.wait_for_timeout(500)

    # Set due date
    if due_date:
        deadline_widget = modal.locator(".o_field_widget[name='date_deadline']").first
        inp = deadline_widget.locator("input:visible")
        if inp.count() == 0:
            btn = deadline_widget.locator("button")
            if btn.count() > 0:
                btn.first.click()
                page.wait_for_timeout(500)
            else:
                deadline_widget.click()
                page.wait_for_timeout(500)
            inp = deadline_widget.locator("input:visible")
        if inp.count() > 0:
            inp.first.click()
            inp.first.fill("")
            inp.first.type(due_date)
            inp.first.press("Tab")
        page.wait_for_timeout(500)
        try:
            page.press("body", "Escape")
        except Exception:
            pass
        page.wait_for_timeout(300)

    # Set assigned user - try multiple possible field names
    if assigned_to:
        for field_name in ["user_id", "activity_user_id"]:
            widget = modal.locator(f".o_field_widget[name='{field_name}'] input")
            if widget.count() > 0 and widget.first.is_visible():
                modal_set_many2one(page, field_name, assigned_to)
                break
        page.wait_for_timeout(500)

    # Click Schedule/Save
    save_btn = modal.locator(
        "button:has-text('Schedule'), "
        "button:has-text('Save')"
    )
    if save_btn.count() > 0:
        save_btn.first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    # Click the "Senior Backend Developer" job card to see its applicants
    click_kanban_card(page, "Senior Backend Developer")
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Click New to create a new applicant
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # Fill applicant fields
    fill_field(page, "partner_name", "Elena Vasquez")
    page.wait_for_timeout(500)

    fill_field(page, "email_from", "elena.vasquez@example.com")
    page.wait_for_timeout(500)

    fill_field(page, "partner_phone", "+1 555-0142")
    page.wait_for_timeout(500)

    # Set recruiter
    set_many2one(page, "user_id", "Marc Demo")
    page.wait_for_timeout(500)

    # Go to Details tab and set expected salary
    click_tab(page, "Details")
    page.wait_for_timeout(500)

    fill_field(page, "salary_expected", "85000")
    page.wait_for_timeout(500)

    # Save the applicant
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # Schedule Call activity using our local function
    _schedule_call_activity(
        page,
        activity_type="Call",
        summary="First technical interview",
        due_date="05/01/2026",
        assigned_to="Marc Demo",
    )


run_oracle(oracle)
