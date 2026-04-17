"""Oracle for website.edit_page_update_text_set_properties.

Open /about-us in the website editor, change the h2 heading and the
paragraph below it, then update the page title and URL via
Site > Properties.

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
    editor_url = "/odoo/action-website.website_preview?path=%2Fabout-us&enable_editor=1"
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)

    # Wait for the editor save button (editor ready)
    page.wait_for_selector("[data-action='save']", timeout=30000)
    page.wait_for_timeout(3000)

    # -----------------------------------------------------------------
    # Step 1: Change page properties FIRST (before any content edits)
    # -----------------------------------------------------------------
    navbar = page.locator(".o_main_navbar").first
    navbar.evaluate("el => { el.style.display = 'flex'; }")
    page.wait_for_timeout(300)

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
    title_input.fill("About Benchmark Industries | Our Story")
    title_input.press("Tab")
    page.wait_for_timeout(500)

    # -- Page URL
    url_input = modal.locator(".o_field_widget[name='url'] input").first
    url_input.click()
    url_input.fill("")
    url_input.fill("/about-benchmark-industries")
    url_input.press("Tab")
    page.wait_for_timeout(500)

    # Save the properties dialog
    modal.locator(
        ".modal-footer button.o_form_button_save"
    ).first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # -----------------------------------------------------------------
    # Step 2: Re-enter editor on the new URL and edit content
    # -----------------------------------------------------------------
    editor_url_new = (
        "/odoo/action-website.website_preview"
        "?path=%2Fabout-benchmark-industries&enable_editor=1"
    )
    page.goto(full_url(editor_url_new))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    page.wait_for_selector("[data-action='save']", timeout=30000)
    page.wait_for_timeout(3000)

    iframe_locator = page.frame_locator("iframe:not(.o_ignore_in_tour)")

    # -- Change h2 heading: "About Our Company" -> "About Benchmark Industries"
    heading = iframe_locator.locator("h2:has-text('About Our Company')").first
    heading.click()
    page.wait_for_timeout(500)
    heading.click(click_count=3)
    page.keyboard.type("About Benchmark Industries")
    page.wait_for_timeout(300)

    # -- Change paragraph below the heading
    paragraph = iframe_locator.locator("p.lead").first
    paragraph.click()
    page.wait_for_timeout(500)
    paragraph.click(click_count=3)
    page.keyboard.type(
        "Benchmark Industries is a leading provider of industrial automation "
        "solutions, serving clients worldwide since 2015."
    )
    page.wait_for_timeout(300)

    # Deselect by clicking elsewhere in the iframe
    iframe_locator.locator("#wrap").first.click(position={"x": 10, "y": 10})
    page.wait_for_timeout(500)

    # -----------------------------------------------------------------
    # Step 3: Save the editor
    # -----------------------------------------------------------------
    page.locator("[data-action='save']").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    _wait_no_loading(page)


run_oracle(oracle)
