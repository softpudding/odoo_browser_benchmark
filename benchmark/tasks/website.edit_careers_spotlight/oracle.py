"""Oracle for website.edit_careers_spotlight.

Open /policy-studio in the website editor, edit the middle card's title,
text, and button label.  Then change the page title and URL via
Site > Properties (Page Properties dialog), and save.
"""

from benchmark.oracle_helpers import (
    login,
    run_oracle,
    full_url,
    _wait_no_loading,
)


def oracle(page):
    login(page)

    # Navigate to the website builder action with the editor enabled.
    # In Odoo 19, the website editor is a backend client action that embeds
    # the website in an iframe. The URL pattern is:
    #   /odoo/action-website.website_preview?path=<url>&enable_editor=1
    editor_url = "/odoo/action-website.website_preview?path=%2Fpolicy-studio&enable_editor=1"
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the iframe to be present and loaded
    iframe_locator = page.frame_locator("iframe:not(.o_ignore_in_tour)")
    # Wait for the builder sidebar to appear (editor is ready)
    page.wait_for_selector(
        ".o-website-builder_sidebar, .o-snippets-menu, "
        "[data-action='save']",
        timeout=30000,
    )
    page.wait_for_timeout(3000)  # Let the editor fully initialize

    # The website content is inside the iframe. Use frame_locator.
    # -----------------------------------------------------------------
    # Edit the MIDDLE card (2nd .col-lg-4)
    # -----------------------------------------------------------------
    middle_card = iframe_locator.locator("#wrap .col-lg-4").nth(1)

    # -- Title: "Escalation Paths" -> "Approval Workflows"
    title_el = middle_card.locator("h3")
    title_el.click()
    page.wait_for_timeout(500)
    # Triple-click to select all text, then type replacement
    title_el.click(click_count=3)
    page.keyboard.type("Approval Workflows")
    page.wait_for_timeout(300)

    # -- Card text: "Route urgent issues quickly." -> "Route sensitive changes through explicit review."
    text_el = middle_card.locator("p")
    text_el.click()
    page.wait_for_timeout(500)
    text_el.click(click_count=3)
    page.keyboard.type("Route sensitive changes through explicit review.")
    page.wait_for_timeout(300)

    # -- Button text: "Open Escalation Map" -> "Read Workflow Policy"
    btn_el = middle_card.locator("a.btn")
    btn_el.click()
    page.wait_for_timeout(500)
    btn_el.click(click_count=3)
    page.keyboard.type("Read Workflow Policy")
    page.wait_for_timeout(300)

    # Click somewhere neutral to deselect
    iframe_locator.locator("#wrap h1, #wrap .container > h1").first.click()
    page.wait_for_timeout(500)

    # -----------------------------------------------------------------
    # Open page properties dialog.
    # In Odoo 19, the "Site" menu might not be visible when the builder
    # is active. We use Odoo's menu system by scrolling to make it visible
    # or clicking the menu button programmatically.
    # -----------------------------------------------------------------
    # Try to find and click the "Site" menu - it might be in the
    # backend top navbar which could be scrolled out of view
    site_btn = page.locator(
        "button[data-menu-xmlid='website.menu_site'], "
        ".o_main_navbar .dropdown-toggle:has-text('Site'), "
        "button.dropdown-toggle:has-text('Site')"
    ).first

    # Make the button visible by scrolling or forcing display
    site_btn.evaluate("el => { el.style.display = 'block'; el.style.visibility = 'visible'; }")
    page.wait_for_timeout(300)
    site_btn.click(force=True)
    page.wait_for_timeout(500)

    # Click "This page" submenu
    this_page = page.locator(
        ".dropdown-menu a:has-text('This page'), "
        ".dropdown-item:has-text('This page'), "
        ".o-dropdown-item:has-text('This page')"
    )
    if this_page.count() > 0:
        this_page.first.click()
        page.wait_for_timeout(500)

    # Click "Properties"
    properties_link = page.locator(
        ".dropdown-menu a:has-text('Properties'), "
        ".dropdown-item:has-text('Properties'), "
        ".o-dropdown-item:has-text('Properties')"
    ).first
    properties_link.click()
    page.wait_for_timeout(1500)

    # The Page Properties dialog opens in the main frame (not iframe)
    modal = page.locator(".modal:visible").last

    # -- Page Title: "Operations Playbooks"
    title_input = modal.locator(
        ".o_field_widget[name='name'] input, "
        "input[name='name']"
    ).first
    title_input.click()
    title_input.fill("")
    title_input.fill("Operations Playbooks")
    title_input.press("Tab")
    page.wait_for_timeout(500)

    # -- Page URL: "/operations-playbooks"
    # The URL field uses widget="page_url" which may be a custom input
    url_widget = modal.locator(".o_field_widget[name='url']").first
    url_input = url_widget.locator("input").first
    url_input.click()
    url_input.fill("")
    url_input.fill("/operations-playbooks")
    url_input.press("Tab")
    page.wait_for_timeout(500)

    # Close the properties dialog (Save button in footer)
    save_dialog_btn = modal.locator(
        "footer button.btn-primary, "
        "footer button:has-text('Save'), "
        ".modal-footer button.btn-primary"
    ).first
    save_dialog_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # -----------------------------------------------------------------
    # Save the page (website editor save button in builder sidebar)
    # -----------------------------------------------------------------
    save_btn = page.locator(
        "button[data-action='save']:visible, "
        ".o-snippets-top-actions button:has-text('Save'):visible, "
        ".o-website-builder_sidebar button[data-action='save']:visible, "
        "button.btn-success:has-text('Save'):visible"
    ).first
    save_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    _wait_no_loading(page)


run_oracle(oracle)
