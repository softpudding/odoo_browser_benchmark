"""Oracle for contacts.archive_duplicate_transfer_fields.

Navigate to Contacts, open the DUPLICATE (Ref=RGS-DUPLICATE) to note
its phone/email (already known from the seed). Open the PRIMARY
(Ref=RGS-PRIMARY), set phone + email, save. Go back to DUPLICATE and
archive it through the Actions menu.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)

PHONE = "+1 415 555 0188"
EMAIL = "contact@ridgeway-global.example"
PRIMARY_REF = "RGS-PRIMARY"
DUPLICATE_REF = "RGS-DUPLICATE"


def _goto_contacts_list(page):
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(600)
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(400)
        _wait_no_loading(page)


def _open_by_ref(page, ref):
    """Search the contacts list for a specific ref and open the row."""
    _goto_contacts_list(page)
    # Use the search box on "Reference" field.
    search_input = page.locator(".o_searchview input:visible").first
    search_input.click()
    search_input.fill(ref)
    page.wait_for_timeout(500)
    # Prefer searching by Reference rather than default Name.
    ref_opt = page.locator(
        ".o_searchview_autocomplete a:has-text('Search Reference'), "
        ".o_searchview_autocomplete li:has-text('Reference'), "
        ".dropdown-item:has-text('Search Reference')"
    )
    if ref_opt.count() > 0:
        ref_opt.first.click()
    else:
        search_input.press("Enter")
    page.wait_for_timeout(700)
    _wait_no_loading(page)

    rows = page.locator(".o_data_row:visible")
    if rows.count() > 0:
        rows.first.click()
    else:
        click_list_row(page, ref)
    page.wait_for_timeout(600)
    _wait_for_ready(page)


def _set_field(page, name, value):
    field = page.locator(f"div[name='{name}'] input:visible").first
    field.click()
    field.press("Control+A")
    field.press("Meta+A")
    field.fill(value)
    field.press("Tab")
    page.wait_for_timeout(200)


def oracle(page):
    login(page)

    # Update PRIMARY with phone + email.
    _open_by_ref(page, PRIMARY_REF)
    _set_field(page, "phone", PHONE)
    _set_field(page, "email", EMAIL)
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Go to DUPLICATE and archive it.
    _open_by_ref(page, DUPLICATE_REF)

    # Open the Actions gear menu and click Archive.
    gear = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        "button.o_form_dropdown_action:visible, "
        "button[aria-label='Actions']:visible"
    ).first
    gear.click()
    page.wait_for_timeout(400)
    archive_item = page.locator(
        ".o-dropdown--menu .dropdown-item:has-text('Archive'):visible, "
        "a.dropdown-item:has-text('Archive'):visible"
    ).first
    archive_item.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Some versions show a confirmation dialog.
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        confirm = modal.last.locator(
            "button:has-text('Archive'):visible, "
            "button.btn-primary:visible"
        ).first
        if confirm.count() > 0:
            confirm.click()
            page.wait_for_timeout(800)
            _wait_no_loading(page)


run_oracle(oracle)
