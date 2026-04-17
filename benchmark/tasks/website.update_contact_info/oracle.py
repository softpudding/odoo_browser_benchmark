"""Oracle for website.update_contact_info.

Navigate to the About Us page, open the website editor, change the phone
number to +1 555 987 6543, and save.
"""

from benchmark.oracle_helpers import (
    full_url,
    run_oracle,
    _wait_no_loading,
)


def oracle(page):
    page.goto(full_url("/web/login"))
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector("input[name='login']", timeout=30000)
    page.fill("input[name='login']", "admin")
    page.fill("input[name='password']", "admin")
    page.click(
        ".oe_login_form button[type='submit'], "
        "form[action='/web/login'] button[type='submit']:has-text('Log')"
    )
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector(".o_action_manager, .o_home_menu", timeout=120000)

    editor_url = "/odoo/action-website.website_preview?path=%2Fabout-us&enable_editor=1"
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    page.wait_for_selector("[data-action='save']", timeout=30000)

    iframe = page.frame_locator("iframe:not(.o_ignore_in_tour)")
    phone_line = iframe.locator("p").filter(has_text="+1 555 123 4567").first
    phone_line.click()
    page.wait_for_timeout(500)
    phone_line.click(click_count=3)
    page.keyboard.type("Phone: +1 555 987 6543")
    page.wait_for_timeout(500)

    page.locator("[data-action='save']").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    _wait_no_loading(page)


run_oracle(oracle)
