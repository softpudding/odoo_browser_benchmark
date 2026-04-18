"""Oracle for contacts.merge_three_duplicates_keep_email.

Navigate to Contacts, switch to list view, filter to "John Doe"
records, tick the three duplicate rows whose Company column is empty
(skipping the Acme Corp decoy), launch the Merge wizard from the
Actions menu, pick the partner with email=john@x.com as the master
via the dst_partner_id m2o (using partner_show_db_id context), and
click 'Merge Contacts'.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


DUP_NAME = "John Doe"
MASTER_EMAIL = "john@x.com"
DECOY_COMPANY = "Acme Corp"


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Switch to list view
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    # Search by name
    search_input = page.locator(".o_searchview input:visible").first
    search_input.click()
    search_input.fill(DUP_NAME)
    page.wait_for_timeout(400)
    name_opt = page.locator(
        ".o_searchview_autocomplete a:has-text('Search Name'), "
        ".o_searchview_autocomplete li:has-text('Name'), "
        ".dropdown-item:has-text('Search Name')"
    )
    if name_opt.count() > 0:
        name_opt.first.click()
    else:
        search_input.press("Enter")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Select all rows with name John Doe AND company NOT "Acme Corp"
    rows = page.locator(".o_data_row:visible")
    selected = 0
    for i in range(rows.count()):
        row = rows.nth(i)
        text = row.inner_text()
        if DUP_NAME not in text:
            continue
        # Decoy row's Company column contains "Acme Corp"
        if DECOY_COMPANY in text:
            continue
        cb = row.locator(".o_list_record_selector input[type='checkbox']")
        if cb.count() > 0:
            cb.first.check()
            selected += 1
    assert selected == 3, (
        f"Expected to select 3 duplicate rows, selected {selected}"
    )
    page.wait_for_timeout(400)

    # Open Actions menu
    actions_btn = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        "button[aria-label='Actions']:visible, "
        ".o_control_panel button:has-text('Actions'):visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(400)

    # Click Merge
    merge_item = page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Merge'):visible, "
        "a.dropdown-item:has-text('Merge'):visible"
    ).first
    merge_item.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Wait for modal to appear
    page.wait_for_selector(".modal:visible, .o_dialog:visible", timeout=10000)

    # Identify master partner id by locating its email in the wizard rows
    wizard_rows = page.locator(
        ".modal .o_list_view .o_data_row:visible, "
        ".o_dialog .o_list_view .o_data_row:visible"
    )
    master_id = None
    for i in range(wizard_rows.count()):
        row = wizard_rows.nth(i)
        row_text = row.inner_text()
        if MASTER_EMAIL in row_text:
            cells = row.locator("td.o_data_cell")
            if cells.count() > 0:
                id_text = cells.first.inner_text().strip()
                try:
                    master_id = int(id_text)
                except ValueError:
                    master_id = None
            break
    assert master_id is not None, (
        f"Could not locate master partner by email {MASTER_EMAIL} in wizard"
    )

    # Set dst_partner_id. The m2o uses partner_show_db_id so the dropdown
    # options have a trailing id token. Type 'John Doe' and pick the one
    # whose trailing id matches master_id.
    dst_input = page.locator(
        ".modal div[name='dst_partner_id'] input:visible, "
        ".o_dialog div[name='dst_partner_id'] input:visible"
    ).first
    dst_input.click()
    page.wait_for_timeout(300)
    # Clear default value thoroughly: triple-click selects all, then delete
    dst_input.click(click_count=3)
    page.wait_for_timeout(150)
    page.keyboard.press("Delete")
    page.wait_for_timeout(200)
    # Also try fill to be safe
    dst_input.fill("")
    page.wait_for_timeout(200)
    dst_input.type(DUP_NAME, delay=40)
    page.wait_for_timeout(1200)

    options = page.locator(".o-autocomplete--dropdown-item:visible")
    picked = False
    num_opts = options.count()
    for i in range(num_opts):
        opt = options.nth(i)
        opt_text = opt.inner_text().strip()
        tokens = opt_text.split()
        # Partner_show_db_id puts id at the end (may be wrapped in parens)
        tail = tokens[-1].strip("()") if tokens else ""
        if tail == str(master_id):
            opt.click()
            picked = True
            break
    if not picked:
        opt_texts = [
            options.nth(i).inner_text() for i in range(num_opts)
        ]
        raise AssertionError(
            f"Could not find dropdown option for master id {master_id} "
            f"among {opt_texts}"
        )

    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Click 'Merge Contacts' button in modal footer
    merge_btn = page.locator(
        ".modal footer button[name='action_merge'], "
        ".modal-footer button[name='action_merge'], "
        ".o_dialog footer button[name='action_merge']"
    ).first
    # Ensure visibility — may need scrolling
    merge_btn.wait_for(state="visible", timeout=10000)
    merge_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Close any trailing confirmation / finished dialogs
    for _ in range(3):
        modal = page.locator(".modal:visible")
        if modal.count() == 0:
            break
        close_btn = modal.last.locator(
            "button:has-text('Ok'):visible, "
            "button:has-text('Close'):visible, "
            "button:has-text('Confirm'):visible"
        ).first
        if close_btn.count() > 0:
            close_btn.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)
        else:
            break


run_oracle(oracle)
