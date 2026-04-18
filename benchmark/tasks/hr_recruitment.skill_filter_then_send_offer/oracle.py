"""Oracle for hr_recruitment.skill_filter_then_send_offer.

Opens the Applications list, types "Python" in the search bar and
picks the Skills autocomplete entry (filters by
applicant_skill_ids). Four applicants match. Ticks ONLY Alice Senior's
row checkbox, opens the Actions menu and clicks Send Email. In the
applicant.send.mail wizard, clears the Subject, types the exact offer
string, fills the body with the required 2026-06-01 date, and clicks
Send.
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


OFFER_SUBJECT = "Job Offer - QA Lead"
OFFER_BODY = "Welcome aboard. Your expected start date is 2026-06-01."
ALICE = "Alice Senior"


def oracle(page):
    login(page)

    navigate(page, "/odoo/recruitment-applications")
    _wait_for_ready(page)
    _wait_no_loading(page)

    ensure_list_view(page)
    _wait_no_loading(page)

    # Type "Python" in search and pick the "Skills" autocomplete entry
    searchbox = page.locator(".o_searchview_input").first
    searchbox.click()
    searchbox.fill("Python")
    page.wait_for_timeout(900)

    ac_items = page.locator(
        ".o_searchview_autocomplete:visible .o-dropdown-item, "
        ".o_searchview_autocomplete:visible .o_menu_item"
    )
    picked = False
    for i in range(ac_items.count()):
        label = ac_items.nth(i).inner_text().strip()
        if "Skills" in label and "Python" in label:
            ac_items.nth(i).click()
            picked = True
            break
    if not picked:
        skill_link = page.locator(
            ".o_searchview_autocomplete:visible .o_menu_item:has-text('Skills')"
        )
        if skill_link.count() > 0:
            skill_link.first.click()
            picked = True
    if not picked:
        searchbox.press("Enter")

    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Tick ONLY Alice Senior's row checkbox
    page.wait_for_selector(".o_list_view .o_data_row", timeout=8000)
    alice_row = page.locator(
        f".o_list_view .o_data_row:has-text('{ALICE}')"
    ).first
    cb = alice_row.locator(".o_list_record_selector input[type='checkbox']")
    cb.first.check()
    page.wait_for_timeout(400)

    # Open Actions menu and click Send Email
    actions_btn = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_cp_action_menus button:has-text('Actions'):visible, "
        "button[aria-label='Actions']:visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(500)

    send_item = page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Send Email'):visible, "
        "a.dropdown-item:has-text('Send Email'):visible"
    ).first
    send_item.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # In the wizard, clear subject and type the exact offer subject
    modal = page.locator(".modal:visible").last
    subject_input = modal.locator(
        ".o_field_widget[name='subject'] input:visible"
    ).first
    subject_input.click()
    subject_input.press("Control+a")
    try:
        subject_input.press("Meta+a")
    except Exception:
        pass
    subject_input.fill(OFFER_SUBJECT)
    page.wait_for_timeout(300)

    # Fill body (html_mail widget — contenteditable)
    body_widget = modal.locator(
        ".o_field_widget[name='body'] .note-editable, "
        ".o_field_widget[name='body'] .odoo-editor-editable, "
        ".o_field_widget[name='body'] [contenteditable='true']"
    ).first
    body_widget.click()
    page.keyboard.type(OFFER_BODY)
    page.wait_for_timeout(400)

    # Click Send
    send_btn = modal.locator("button:has-text('Send')").first
    send_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
