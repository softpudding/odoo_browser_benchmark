"""Oracle for website_hr_recruitment.edit_job_form_publish_preview.

Back-office-only UI path:
  1. Open /odoo/recruitment → Configure on Bench QA Engineer.
  2. Summary tab → type the description phrase into the HTML editor.
  3. Flip the "Published" boolean_toggle.
  4. Save.
  5. Click the Go to Website smart button (widget=website_redirect_button).
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


JOB_NAME = "Bench QA Engineer"
EXPECTED_DESC_PHRASE = "Write automated tests for Bench Products."


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Find the Bench QA Engineer kanban card and click Configure.
    job_card = page.locator(
        f".o_kanban_record:has-text('{JOB_NAME}')"
    ).first
    job_card.wait_for(timeout=15000)
    configure_btn = job_card.locator("button:has-text('Configure')").first
    configure_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Activate Details/Recruitment tab so the Published toggle is visible.
    details_tab = page.locator(
        ".o_notebook .nav-link:has-text('Recruitment'), "
        ".o_notebook .nav-link:has-text('Details')"
    ).first
    if details_tab.count() > 0 and details_tab.is_visible():
        try:
            details_tab.click()
            page.wait_for_timeout(500)
        except Exception:
            pass

    # Toggle Published (website_published boolean_toggle).
    publish_cb = page.locator(
        ".o_field_boolean_toggle[name='website_published'] input, "
        ".o_field_widget[name='website_published'] input[type='checkbox']"
    )
    if publish_cb.count() > 0:
        try:
            checked = publish_cb.first.is_checked()
        except Exception:
            checked = False
        if not checked:
            try:
                publish_cb.first.click()
            except Exception:
                page.locator(
                    ".o_field_boolean_toggle[name='website_published'], "
                    ".o_field_widget[name='website_published'] .form-check, "
                    ".o_field_widget[name='website_published'] label"
                ).first.click()
            page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Open the Summary / Job Description tab and type the description.
    desc_tab = page.locator(
        ".o_notebook .nav-link:has-text('Job Description'), "
        ".o_notebook .nav-link:has-text('Summary')"
    ).first
    if desc_tab.count() > 0 and desc_tab.is_visible():
        desc_tab.click()
        page.wait_for_timeout(500)

    desc_field = page.locator(
        ".o_field_widget[name='description'] .note-editable, "
        ".o_field_widget[name='description'] .odoo-editor-editable, "
        ".o_field_widget[name='description'] [contenteditable='true']"
    ).first
    desc_field.wait_for(timeout=10000)
    desc_field.click()
    page.wait_for_timeout(300)
    # Clear and type. The editor might already be empty; still select-all-delete.
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.type(EXPECTED_DESC_PHRASE)
    page.wait_for_timeout(500)

    # Save
    save_form(page)
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Click Go to Website smart button (widget website_redirect_button renders
    # an <a>/<button> inside the button box).
    go_website = page.locator(
        ".oe_button_box a:has-text('Go to Website'), "
        ".oe_button_box button:has-text('Go to Website'), "
        ".oe_stat_button:has-text('Go to Website'), "
        "a[name='is_published']:has-text('Go to Website'), "
        "button[name='is_published']:has-text('Go to Website')"
    ).first
    try:
        go_website.wait_for(timeout=10000)
        go_website.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(3000)
    except Exception:
        # Fallback: navigate via full_url pattern /jobs/<slug>.
        # We don't know the slug here — but /jobs page will list it.
        page.goto(page.url.split("/odoo")[0] + "/jobs")
        page.wait_for_load_state("load")
        page.wait_for_timeout(2500)
        page.locator(f"a:has-text('{JOB_NAME}')").first.click()
        page.wait_for_load_state("load")
        page.wait_for_timeout(2500)


run_oracle(oracle)
