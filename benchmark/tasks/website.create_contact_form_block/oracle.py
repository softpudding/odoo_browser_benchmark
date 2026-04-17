"""Oracle for website.create_contact_form_block."""

import sys

from benchmark.oracle_helpers import full_url, login, run_oracle, _wait_no_loading


def oracle(page):
    login(page)
    page.goto(full_url("/odoo/action-website.website_preview?path=%2Ftalk-to-sales&enable_editor=1"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    page.wait_for_selector("[data-action='save']", timeout=30000)

    main_iframe = page.frame_locator('iframe[src*="force"]')

    # First, click at the bottom of the page content to position cursor
    # Click after the last section to set the insert position
    wrap = main_iframe.locator("#wrap")
    sections = main_iframe.locator("#wrap > section, #wrap > div")
    print(f"DBG: sections: {sections.count()}", file=sys.stderr, flush=True)

    # Click below the hero section
    if sections.count() > 0:
        last = sections.last
        last.click()
        page.wait_for_timeout(1000)

    # Open Blocks panel
    page.locator('button:has-text("Blocks")').first.click()
    page.wait_for_timeout(2000)

    # Find and click the "Form" inner element (s_website_form)
    form_thumb = page.locator('.o_snippet_thumbnail[data-snippet="s_website_form"]')
    print(f"DBG: form thumb: {form_thumb.count()}", file=sys.stderr, flush=True)

    if form_thumb.count() > 0:
        # Scroll it into view
        form_thumb.first.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        # Get coordinates for drag
        thumb_box = form_thumb.first.bounding_box()
        iframe_el = page.locator('iframe[src*="force"]')
        iframe_box = iframe_el.first.bounding_box()

        print(f"DBG: thumb_box={thumb_box}", file=sys.stderr, flush=True)
        print(f"DBG: iframe_box={iframe_box}", file=sys.stderr, flush=True)

        if thumb_box and iframe_box:
            sx = thumb_box["x"] + thumb_box["width"] / 2
            sy = thumb_box["y"] + thumb_box["height"] / 2
            # Target: middle of the iframe content (below hero, above footer)
            tx = iframe_box["x"] + iframe_box["width"] / 2
            ty = iframe_box["y"] + iframe_box["height"] * 0.5

            # Drag the snippet into the iframe
            page.mouse.move(sx, sy)
            page.wait_for_timeout(200)
            page.mouse.down()
            page.wait_for_timeout(500)
            page.mouse.move(tx, ty, steps=10)
            page.wait_for_timeout(500)
            page.mouse.up()
            page.wait_for_timeout(3000)
            _wait_no_loading(page)

    # Check if form was inserted
    forms = main_iframe.locator('.s_website_form')
    print(f"DBG: forms after drag: {forms.count()}", file=sys.stderr, flush=True)

    if forms.count() == 0:
        # Alternative: try the "Contact & Forms" group approach
        page.locator('[data-snippet="s_snippet_group"]:has-text("Contact")').first.click()
        page.wait_for_timeout(3000)

        # Check for the tab panel iframe
        tab_frame_el = page.locator('iframe[id*="contact"]')
        if tab_frame_el.count() > 0:
            tab_id = tab_frame_el.first.get_attribute('id')
            tab_frame = page.frame_locator(f'#{tab_id}')
            for sid in ["s_website_form_info", "s_title_form", "s_form_aside"]:
                w = tab_frame.locator(f'.o_snippet_preview_wrap[data-snippet-id="{sid}"]')
                try:
                    if w.count() > 0:
                        w.first.click(timeout=5000)
                        page.wait_for_timeout(3000)
                        _wait_no_loading(page)
                        break
                except Exception:
                    continue

    forms = main_iframe.locator('.s_website_form')
    print(f"DBG: final forms: {forms.count()}", file=sys.stderr, flush=True)

    if forms.count() == 0:
        raise RuntimeError("Could not insert form block")

    # Edit submit button text to "Request Callback"
    submit = main_iframe.locator('.s_website_form button[type="submit"], .s_website_form .s_website_form_send, .s_website_form a.btn')
    if submit.count() > 0:
        submit.first.click(click_count=3)
        page.wait_for_timeout(300)
        page.keyboard.type("Request Callback")
        page.wait_for_timeout(500)

    # Save
    save = page.locator("[data-action='save']:visible")
    if save.count() > 0:
        save.first.click()
    else:
        page.keyboard.press("Meta+s")
    page.wait_for_timeout(3000)
    _wait_no_loading(page)


run_oracle(oracle)
