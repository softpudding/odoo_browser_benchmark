"""Oracle for website.edit_careers_spotlight.

Open /policy-studio in the website editor, edit the middle card's title,
text, and button label.  Then change the page title and URL via
Site > Properties, and save.
"""

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
    _wait_no_loading,
)


def oracle(page):
    login(page)

    # Navigate to the page with the editor enabled
    page.goto(full_url("/policy-studio?enable_editor=1"))
    page.wait_for_load_state("load")

    # Wait for the website editor to be ready (the editor toolbar / save btn)
    page.wait_for_selector("#oe_snippets, .o_we_website_top_actions", timeout=20000)
    page.wait_for_timeout(3000)  # let the editor fully initialize

    # -----------------------------------------------------------------
    # Edit the MIDDLE card (2nd .col-lg-4)
    # -----------------------------------------------------------------
    middle_card = page.locator("#wrap .col-lg-4").nth(1)

    # -- Title: "Escalation Paths" -> "Approval Workflows"
    title_el = middle_card.locator("h3")
    title_el.click()
    page.wait_for_timeout(300)
    # Triple-click to select all text, then type replacement
    title_el.click(click_count=3)
    page.keyboard.type("Approval Workflows")
    page.wait_for_timeout(300)

    # -- Card text: "Route urgent issues quickly." -> "Route sensitive changes through explicit review."
    text_el = middle_card.locator("p")
    text_el.click()
    page.wait_for_timeout(300)
    text_el.click(click_count=3)
    page.keyboard.type("Route sensitive changes through explicit review.")
    page.wait_for_timeout(300)

    # -- Button text: "Open Escalation Map" -> "Read Workflow Policy"
    btn_el = middle_card.locator("a.btn")
    btn_el.click()
    page.wait_for_timeout(300)
    btn_el.click(click_count=3)
    page.keyboard.type("Read Workflow Policy")
    page.wait_for_timeout(300)

    # -----------------------------------------------------------------
    # Open page properties: Site > Properties
    # -----------------------------------------------------------------
    # Click "Site" in the top menu bar of the website editor
    site_menu = page.locator(
        ".o_we_website_top_actions .dropdown-toggle:has-text('Site'), "
        "button.dropdown-toggle:has-text('Site'), "
        "a.dropdown-toggle:has-text('Site')"
    ).first
    site_menu.click()
    page.wait_for_timeout(500)

    # Click "Properties" in the dropdown
    page.locator(
        ".dropdown-menu a:has-text('Properties'), "
        ".dropdown-item:has-text('Properties')"
    ).first.click()
    page.wait_for_timeout(1000)

    # -- Page Title: "Operations Playbooks"
    title_input = page.locator(
        ".modal:visible input[name='name'], "
        ".modal:visible .o_field_widget[name='name'] input"
    ).first
    title_input.click()
    title_input.fill("")
    title_input.fill("Operations Playbooks")
    page.wait_for_timeout(300)

    # -- Page URL: "/operations-playbooks"
    url_input = page.locator(
        ".modal:visible input[name='url'], "
        ".modal:visible .o_field_widget[name='url'] input"
    ).first
    url_input.click()
    url_input.fill("")
    url_input.fill("/operations-playbooks")
    page.wait_for_timeout(300)

    # Close the properties dialog (Save / OK / Close)
    modal = page.locator(".modal:visible").last
    save_btn = modal.locator(
        "button.btn-primary:has-text('Save'), "
        "button.btn-primary:has-text('OK'), "
        "button.btn-primary:has-text('Close'), "
        "footer button.btn-primary"
    ).first
    save_btn.click()
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # -----------------------------------------------------------------
    # Save the page (website editor save button)
    # -----------------------------------------------------------------
    save_page = page.locator(
        "button[data-action='save']:visible, "
        ".o_we_website_top_actions button:has-text('Save'):visible, "
        "button.btn-primary:has-text('Save'):visible"
    ).first
    save_page.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    _wait_no_loading(page)


run_oracle(oracle)
