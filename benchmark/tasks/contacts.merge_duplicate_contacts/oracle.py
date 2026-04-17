"""Oracle for contacts.merge_duplicate_contacts.

Navigate to Contacts, switch to list view, filter to the two
'Globex Corporation' duplicates, tick their checkboxes, launch the
Merge wizard from the Actions menu, identify the master by VAT from
the wizard's partner_ids list, pick it in the dst_partner_id m2o by
matching the ' (<id>)' suffix (partner_show_db_id context), and click
'Merge Contacts'.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


DUP_NAME = "Globex Corporation"
MASTER_VAT = "BE0477472701"


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

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

    rows = page.locator(".o_data_row:visible")
    row_count = rows.count()
    for i in range(row_count):
        row = rows.nth(i)
        text = row.inner_text()
        if DUP_NAME in text and "Globex plc" not in text and \
                "Globex Labs" not in text:
            cb = row.locator(".o_list_record_selector input[type='checkbox']")
            if cb.count() > 0:
                cb.first.check()
    page.wait_for_timeout(400)

    actions_btn = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        "button[aria-label='Actions']:visible, "
        ".o_control_panel button:has-text('Actions'):visible"
    ).first
    actions_btn.click()
    page.wait_for_timeout(400)

    merge_item = page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Merge'):visible, "
        "a.dropdown-item:has-text('Merge'):visible"
    ).first
    merge_item.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Find the master row in the wizard's partner_ids list by its VAT
    wizard_rows = page.locator(
        ".modal .o_data_row:visible, .o_dialog .o_data_row:visible"
    )
    master_id = None
    for i in range(wizard_rows.count()):
        row = wizard_rows.nth(i)
        row_text = row.inner_text()
        if MASTER_VAT in row_text:
            cells = row.locator("td.o_data_cell")
            if cells.count() > 0:
                id_text = cells.first.inner_text().strip()
                try:
                    master_id = int(id_text)
                except ValueError:
                    master_id = None
            break

    assert master_id is not None, (
        f"Could not locate master partner by VAT {MASTER_VAT} in wizard"
    )

    # Focus the dst_partner_id input and type to trigger autocomplete
    dst_input = page.locator(
        ".modal div[name='dst_partner_id'] input:visible, "
        ".o_dialog div[name='dst_partner_id'] input:visible"
    ).first
    dst_input.click()
    page.wait_for_timeout(300)
    dst_input.fill("")
    page.wait_for_timeout(200)
    dst_input.type(DUP_NAME)
    page.wait_for_timeout(900)

    # Pick the option whose text ends with "(master_id)"
    options = page.locator(".o-autocomplete--dropdown-item:visible")
    picked = False
    for i in range(options.count()):
        opt = options.nth(i)
        opt_text = opt.inner_text().strip()
        # Options from m2o with partner_show_db_id show the ID appended:
        # 'Globex Corporation 9' or 'Globex Corporation (9)' (renderer may
        # drop parens). Match by the trailing numeric token.
        tokens = opt_text.split()
        tail_digits = tokens[-1].strip("()") if tokens else ""
        if tail_digits == str(master_id):
            opt.click()
            picked = True
            break
    if not picked:
        opt_texts = [options.nth(i).inner_text() for i in range(options.count())]
        raise AssertionError(
            f"Could not find dropdown option for master id {master_id} "
            f"among {opt_texts}"
        )

    # Close any lingering dropdown overlay before clicking footer button
    page.wait_for_timeout(400)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    # Click 'Merge Contacts'
    merge_btn = page.locator(
        ".modal button[name='action_merge']:visible, "
        ".o_dialog button:has-text('Merge Contacts'):visible"
    ).first
    merge_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    for _ in range(2):
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
