"""Oracle for contacts.add_bank_account_to_partner.

Open the partner, switch to the Invoicing tab, type the IBAN into the
many2many_tags_banks widget, pick the 'Create ...' suggestion, save the
dialog, then save the partner form.
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

PARTNER_NAME = "Benchmark IBAN Supplier Ltd"
IBAN = "GB82 WEST 1234 5698 7654 32"


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

    click_list_row(page, PARTNER_NAME)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    try:
        click_tab(page, "Invoicing")
    except Exception:
        tab = page.locator(
            ".o_notebook a.nav-link:has-text('Invoicing'):visible"
        ).first
        if tab.count() > 0:
            tab.click()
    page.wait_for_timeout(700)
    _wait_no_loading(page)

    bank_widget = page.locator(".o_field_widget[name='bank_ids']").first
    bank_widget.wait_for(state="visible", timeout=10000)
    bank_widget.click()
    page.wait_for_timeout(300)
    inp = bank_widget.locator("input").first
    inp.click()
    inp.fill(IBAN)
    page.wait_for_timeout(900)

    create_opt = page.locator(
        ".o-autocomplete--dropdown-item:has-text('Create'):visible, "
        "li.ui-menu-item:has-text('Create'):visible"
    )
    if create_opt.count() > 0:
        create_opt.first.click()
    else:
        alt = page.locator(
            ".o-autocomplete--dropdown-item.o_m2o_dropdown_option:visible"
        )
        if alt.count() > 0:
            alt.first.click()
        else:
            inp.press("Enter")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    dialog = page.locator(".modal:visible")
    if dialog.count() > 0:
        acc_input = dialog.last.locator("div[name='acc_number'] input").first
        if acc_input.count() > 0:
            val = acc_input.input_value() or ""
            if val.replace(" ", "") != IBAN.replace(" ", ""):
                acc_input.click()
                acc_input.press("Control+A")
                acc_input.press("Meta+A")
                acc_input.fill(IBAN)
        save_btn = dialog.last.locator(
            "button.btn-primary:has-text('Save'):visible, "
            "button.o_form_button_save:visible, "
            "button.btn-primary:visible"
        ).first
        save_btn.click()
        page.wait_for_timeout(1500)
        _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


run_oracle(oracle)
