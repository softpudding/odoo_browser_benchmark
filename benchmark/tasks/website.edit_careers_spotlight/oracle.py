"""Oracle for website.edit_careers_spotlight.

Open /policy-studio in the website editor, edit the middle card's title,
text, and button label.  Then change the page title and URL via
Site > Properties (Page Properties dialog), and save.

Strategy: Change page properties first (before editing content), because
changing the URL triggers a page reload that would discard unsaved content
edits. After properties are saved, re-enter the editor on the new URL
path, make the content edits, and save.
"""

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
    _wait_no_loading,
)


def oracle(page):
    login(page)

    # Navigate to the website builder with the editor enabled.
    editor_url = "/odoo/action-website.website_preview?path=%2Fpolicy-studio&enable_editor=1"
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the editor save button (editor ready)
    page.wait_for_selector("[data-action='save']", timeout=30000)
    page.wait_for_timeout(3000)

    # -----------------------------------------------------------------
    # Step 1: Change page properties FIRST (before any content edits)
    # This avoids the "your changes will be lost" confirmation dialog
    # that appears when the URL change triggers a page reload.
    # -----------------------------------------------------------------
    # The main navbar is hidden (display:none) in the website builder.
    # Make it visible so we can access the Site menu.
    navbar = page.locator(".o_main_navbar").first
    navbar.evaluate("el => { el.style.display = 'flex'; }")
    page.wait_for_timeout(300)

    # Open the Site dropdown via dispatch_event (the button itself
    # isn't interactable via normal click since it's in a hidden navbar)
    page.locator("[data-menu-xmlid='website.menu_site']").first.dispatch_event(
        "click"
    )
    page.wait_for_timeout(1000)

    # Click "Properties"
    page.locator(".dropdown-item:has-text('Properties')").first.click()
    page.wait_for_timeout(2000)

    # The Page Properties dialog opens in the main frame
    modal = page.locator(".modal:visible").last

    # -- Page Title
    title_input = modal.locator(".o_field_widget[name='name'] input").first
    title_input.click()
    title_input.fill("")
    title_input.fill("Operations Playbooks")
    title_input.press("Tab")
    page.wait_for_timeout(500)

    # -- Page URL
    url_input = modal.locator(".o_field_widget[name='url'] input").first
    url_input.click()
    url_input.fill("")
    url_input.fill("/operations-playbooks")
    url_input.press("Tab")
    page.wait_for_timeout(500)

    # Save the properties dialog
    modal.locator(
        ".modal-footer button.o_form_button_save"
    ).first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # -----------------------------------------------------------------
    # Step 2: Re-enter editor on the new URL and edit the card content
    # -----------------------------------------------------------------
    # The page URL changed to /operations-playbooks; re-open editor there.
    editor_url_new = (
        "/odoo/action-website.website_preview"
        "?path=%2Foperations-playbooks&enable_editor=1"
    )
    page.goto(full_url(editor_url_new))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    page.wait_for_selector("[data-action='save']", timeout=30000)
    page.wait_for_timeout(3000)

    iframe_locator = page.frame_locator("iframe:not(.o_ignore_in_tour)")
    middle_card = iframe_locator.locator("#wrap .col-lg-4").nth(1)

    # -- Title: "Escalation Paths" -> "Approval Workflows"
    title_el = middle_card.locator("h3")
    title_el.click()
    page.wait_for_timeout(500)
    title_el.click(click_count=3)
    page.keyboard.type("Approval Workflows")
    page.wait_for_timeout(300)

    # -- Paragraph text
    text_el = middle_card.locator("p")
    text_el.click()
    page.wait_for_timeout(500)
    text_el.click(click_count=3)
    page.keyboard.type("Route sensitive changes through explicit review.")
    page.wait_for_timeout(300)

    # -- Button label
    btn_el = middle_card.locator("a.btn")
    btn_el.click()
    page.wait_for_timeout(500)
    btn_el.click(click_count=3)
    page.keyboard.type("Read Workflow Policy")
    page.wait_for_timeout(300)

    # Deselect
    iframe_locator.locator("#wrap h1").first.click()
    page.wait_for_timeout(500)

    # -----------------------------------------------------------------
    # Step 3: Save the editor
    # -----------------------------------------------------------------
    page.locator("[data-action='save']").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    _wait_no_loading(page)


run_oracle(oracle)
