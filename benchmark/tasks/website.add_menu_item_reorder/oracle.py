"""Oracle for website.add_menu_item_reorder."""

from benchmark.oracle_helpers import full_url, login, run_oracle, _wait_no_loading


def oracle(page):
    login(page)
    page.goto(full_url("/odoo/action-website.website_preview?path=%2F&enable_editor=1"))
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)
    page.wait_for_selector("[data-action='save']", timeout=30000)

    # Show navbar (may be hidden during editing)
    navbar = page.locator(".o_main_navbar").first
    navbar.evaluate("el => { el.style.display = 'flex'; }")
    page.wait_for_timeout(500)

    # Open Site > Menu Editor
    page.locator("[data-menu-xmlid='website.menu_site']").first.dispatch_event("click")
    page.wait_for_timeout(800)
    page.locator(".dropdown-item:has-text('Menu Editor')").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    menu_modal = page.locator(".modal:visible").last

    # Click "Add Menu Item"
    menu_modal.locator('a:has-text("Add Menu Item"), button:has-text("Add Menu Item")').first.click()
    page.wait_for_timeout(1500)

    # The add-item sub-dialog is a nested modal
    add_modal = page.locator(".modal:visible").last
    title_input = add_modal.locator("input").first
    url_input = add_modal.locator("#url_input, input").nth(1)

    title_input.click()
    title_input.fill("Resources")
    page.wait_for_timeout(300)

    url_input.click()
    url_input.fill("/resources")
    page.wait_for_timeout(300)

    # Click Continue
    add_modal.locator("button:has-text('Continue'), button.btn-primary").first.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Verify Resources was added in the menu editor
    menu_modal = page.locator(".modal:visible").last

    # Read current order and find indices
    top_ul = menu_modal.locator(".oe_menu_editor > ul, .o_menu_editor_content > ul").first
    if top_ul.count() == 0:
        top_ul = menu_modal.locator("ul").first
    lis = top_ul.locator("> li")

    item_names = []
    for i in range(lis.count()):
        name = lis.nth(i).inner_text().strip().split("\n")[0].strip()
        item_names.append(name)

    print(f"Menu before reorder: {item_names}")

    # Find Resources and the position after Consulting
    resources_idx = None
    consulting_idx = None
    for i, name in enumerate(item_names):
        if "Resources" in name:
            resources_idx = i
        if "Consulting" in name:
            consulting_idx = i

    if resources_idx is not None and consulting_idx is not None and resources_idx != consulting_idx + 1:
        # Need to drag Resources to after Consulting
        source_li = lis.nth(resources_idx)
        # Target: drop just after Consulting item
        target_li = lis.nth(consulting_idx)

        source_box = source_li.bounding_box()
        target_box = target_li.bounding_box()

        if source_box and target_box:
            sx = source_box["x"] + 20
            sy = source_box["y"] + source_box["height"] / 2
            # Drop position: just below Consulting
            tx = target_box["x"] + 20
            ty = target_box["y"] + target_box["height"] + 2

            page.mouse.move(sx, sy)
            page.mouse.down()
            page.wait_for_timeout(300)
            # Move in steps for drag to register
            page.mouse.move(tx, ty, steps=10)
            page.wait_for_timeout(300)
            page.mouse.up()
            page.wait_for_timeout(500)

    # Save the menu editor
    menu_modal.locator("button:has-text('Save')").first.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)

    # Save the website editor (may already be auto-saved)
    save_btn = page.locator("[data-action='save']:visible")
    if save_btn.count() > 0:
        save_btn.first.click()
        page.wait_for_timeout(3000)
        _wait_no_loading(page)


run_oracle(oracle)
