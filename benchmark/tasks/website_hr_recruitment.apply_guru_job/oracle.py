"""Oracle for website_hr_recruitment.apply_guru_job.

Public user (no login). Navigate to /jobs, click the "Guru" job,
fill out the application form, and submit.
"""

from benchmark.oracle_helpers import (
    full_url,
    run_oracle,
    _wait_no_loading,
    DB,
)


def oracle(page):
    # No login -- this is a public application.
    # However, we may need to ensure the right DB is selected for multi-DB setups.

    # Go to /jobs with db param if needed
    url = "/jobs"
    if DB:
        url = f"/jobs?db={DB}"
    page.goto(full_url(url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # If we hit a database selector page, select the DB
    db_select = page.locator("select[name='db']")
    if db_select.count() > 0 and db_select.is_visible():
        if DB:
            db_select.select_option(DB)
            page.wait_for_timeout(1000)
        # Re-navigate after DB selection
        page.goto(full_url(url))
        page.wait_for_load_state("load")
        page.wait_for_timeout(3000)

    # Click the "Guru" job posting link
    guru_link = page.locator("a:has-text('Guru')").first
    guru_link.wait_for(timeout=10000)
    guru_link.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click "Apply Now" or similar button to open the application form
    apply_btn = page.locator(
        "a:has-text('Apply'), "
        "button:has-text('Apply')"
    ).first
    apply_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Fill in the application form fields (public website form, standard HTML inputs)
    page.locator("input[name='partner_name']").first.fill("John Smith")
    page.locator("input[name='email_from']").first.fill("john@smith.com")
    page.locator("input[name='partner_phone']").first.fill("118.218")

    # LinkedIn profile -- may be named linkedin_profile or similar
    linkedin_input = page.locator(
        "input[name='linkedin_profile'], "
        "input[name='linkedin']"
    ).first
    linkedin_input.fill("linkedin.com/in/john-smith")

    # Short introduction / description (could be textarea)
    intro_field = page.locator(
        "textarea[name='description'], "
        "textarea[name='body']"
    ).first
    intro_field.fill("### [GURU] HR RECRUITMENT TEST DATA ###")

    # Submit the form
    submit_btn = page.locator(
        "button[type='submit'], "
        "a.btn:has-text('Submit'), "
        "button:has-text('Submit'), "
        ".s_website_form_send"
    ).first
    submit_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)

    # Verify confirmation -- look for a success message or thank-you text
    # The form shows a success message on the same page
    page.wait_for_selector(
        ".s_website_form_end_message:visible, "
        "span:has-text('Thank'):visible, "
        "div:has-text('submitted'):visible, "
        "div:has-text('Congratulations'):visible",
        timeout=15000,
    )


run_oracle(oracle)
