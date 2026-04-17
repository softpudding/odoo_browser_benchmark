"""Oracle for contacts.add_bank_account_iban.

Open Ridgeway Commercial Services, switch to Invoicing tab, open the
Bank Accounts tag widget, create a new bank with the target IBAN,
save the dialog, save the form.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)

PARTNER_NAME = "Ridgeway Commercial Services"
IBAN = "DE89370400440532013000"


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Switch to list view for predictable navigation.
    list_btn = page.locator("button[data-tooltip='List']:visible")
    if list_btn.count() > 0:
        list_btn.first.click()
        page.wait_for_timeout(500)
        _wait_no_loading(page)

    click_list_row(page, PARTNER_NAME)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Open Invoicing tab.
    try:
        click_tab(page, "Invoicing")
    except Exception:
        # Fallback: search notebook tabs by text.
        tab = page.locator(
            ".o_notebook a.nav-link:has-text('Invoicing'):visible"
        ).first
        if tab.count() > 0:
            tab.click()
    page.wait_for_timeout(700)
    _wait_no_loading(page)

    # Focus the bank_ids tag widget and start typing the IBAN.
    bank_widget = page.locator(".o_field_widget[name='bank_ids']").first
    # Click inside to get focus then type.
    bank_widget.click()
    page.wait_for_timeout(300)
    # Find the autocomplete input inside.
    inp = bank_widget.locator("input").first
    inp.click()
    inp.fill(IBAN)
    page.wait_for_timeout(900)

    # Click "Create" or the "Create ..." suggestion in the dropdown.
    create_opt = page.locator(
        ".o-autocomplete--dropdown-item:has-text('Create'):visible, "
        "li.ui-menu-item:has-text('Create'):visible"
    )
    if create_opt.count() > 0:
        create_opt.first.click()
    else:
        # Some versions surface a distinct "Create and edit" link.
        alt = page.locator(
            ".o-autocomplete--dropdown-item.o_m2o_dropdown_option:visible"
        )
        if alt.count() > 0:
            alt.first.click()
        else:
            # Press Enter to trigger create from the typed value.
            inp.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # A dialog should open to finish creating the res.partner.bank.
    dialog = page.locator(".modal:visible")
    if dialog.count() > 0:
        acc_input = dialog.last.locator(
            "div[name='acc_number'] input"
        ).first
        if acc_input.count() > 0:
            val = acc_input.input_value() or ""
            if val.replace(" ", "") != IBAN:
                acc_input.click()
                acc_input.press("Control+A")
                acc_input.press("Meta+A")
                acc_input.fill(IBAN)
        # Save & close dialog.
        save_btn = dialog.last.locator(
            "button.btn-primary:has-text('Save'):visible, "
            "button.o_form_button_save:visible, "
            "button.btn-primary:visible"
        ).first
        save_btn.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    # Save the partner form.
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
