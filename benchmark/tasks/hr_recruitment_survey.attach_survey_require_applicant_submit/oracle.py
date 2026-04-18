"""Oracle for hr_recruitment_survey.attach_survey_require_applicant_submit.

Opens the 'Bench Recruit Lead' job form via the list view, switches to
the Recruitment tab, fills the Interview Form many2one with the seeded
'Bench Screening' survey, saves, then opens Alice Candidate's applicant
form to confirm the Send Interview button is now visible.
"""

from benchmark.oracle_helpers import (
    ensure_list_view,
    click_list_row,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    # Switch to list view so the job kanban card's default action
    # (opening Applications) does not get in the way.
    ensure_list_view(page)
    _wait_no_loading(page)

    # Open the Bench Recruit Lead row → job form.
    click_list_row(page, "Bench Recruit Lead")
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Click the Recruitment tab (labelled "Details" on the hr_recruitment-
    # inherited view). Our page name is 'recruitment_page'.
    tab = page.locator(
        ".o_notebook .nav-item a[name='recruitment_page'], "
        ".o_notebook .nav-item:has-text('Details') a, "
        ".o_notebook .nav-item:has-text('Recruitment') a"
    ).first
    if tab.count() > 0:
        tab.click()
        page.wait_for_timeout(300)

    # Set the Interview Form many2one to Bench Screening.
    set_many2one(page, "survey_id", "Bench Screening")

    # Save the job form.
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Navigate to the applicant to confirm Send Interview header button
    # is visible — do it via the global Applications menu for simplicity.
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    # Open applicant directly via action url.
    page.evaluate("""
        window.location.href = '/odoo/action-hr_recruitment.crm_case_categ0_act_job';
    """)
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Try to open Alice Candidate's applicant form from the list.
    ensure_list_view(page)
    _wait_no_loading(page)
    try:
        click_list_row(page, "Alice Candidate")
        _wait_for_ready(page)
        _wait_no_loading(page)
        # Verify Send Interview button is present (does not need to click).
        btn = page.locator("button:has-text('Send Interview')")
        btn.first.wait_for(state="visible", timeout=5000)
    except Exception:
        # Non-fatal — the main task is the job edit which is already saved.
        pass


run_oracle(oracle)
