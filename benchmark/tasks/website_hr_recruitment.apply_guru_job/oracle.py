"""Oracle for website_hr_recruitment.apply_guru_job.

Public user (no login). Navigate to /jobs, click the "Guru" job,
fill out the application form, and submit.
"""

from benchmark.oracle_helpers import (
    full_url,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    # No login -- this is a public application

    # Go to /jobs
    page.goto(full_url("/jobs"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)

    # Click the "Guru" job posting link
    page.locator("a:has-text('Guru')").first.click()
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
    page.locator("input[name='partner_name']").fill("John Smith")
    page.locator("input[name='email_from']").fill("john@smith.com")
    page.locator("input[name='partner_phone']").fill("118.218")

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
    page.wait_for_timeout(3000)

    # Verify confirmation -- look for a success message or thank-you text
    page.wait_for_selector(
        ".s_website_form_end_message:visible, "
        ":has-text('Thank'):visible, "
        ":has-text('submitted'):visible, "
        ":has-text('Congratulations'):visible",
        timeout=10000,
    )


run_oracle(oracle)
