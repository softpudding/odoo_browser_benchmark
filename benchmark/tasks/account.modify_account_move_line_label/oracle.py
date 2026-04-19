"""Oracle for account.modify_account_move_line_label.

Open the POSTED invoice BENCH-EDIT-001 (customer Bench Edit Co), click
'Reset to Draft' in the statusbar header, edit the single invoice line's
Label (the `name` field) from 'Service' to 'Corrected description', then
click 'Confirm' in the header to re-post.

Odoo 19 renders account.move.line.name via the
`product_label_section_and_note_field` widget, which merges the
product_id and name columns into a single cell under `td[name='product_id']`.
The description textarea lives inside
`.o_field_product_label_section_and_note_cell` and is hidden with
`d-none` when the label is empty (i.e. when name == product display
name). A toggler button (`.fa-bars`) reveals the textarea; we click
that first if present, then fill the textarea directly.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
    clear_search_filters,
    _wait_no_loading,
    _wait_for_ready,
)


TARGET_TEXT = "Corrected description"


def _edit_label_cell(page, text):
    """Overwrite the Label on the sole invoice line.

    Same mechanic as purchase.set_vendor_product_code_on_po_line —
    click into the merged product_id cell to activate row edit mode,
    click the fa-bars toggler if the description textarea is hidden,
    then fill the textarea.
    """
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row"
    ).first
    row.wait_for(state="visible", timeout=10000)

    product_cell = row.locator("td[name='product_id']").first
    product_cell.wait_for(state="visible", timeout=5000)
    product_cell.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    selected_row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row.o_selected_row"
    ).first
    selected_row.wait_for(state="visible", timeout=5000)

    # Click the label-visibility toggler if the textarea is hidden.
    toggler = selected_row.locator(
        "td[name='product_id'] button.o_external_button.fa-bars, "
        "td[name='product_id'] button.fa-bars, "
        "td[name='product_id'] button[data-tooltip*='description']"
    ).first
    if toggler.count() > 0 and toggler.is_visible():
        try:
            toggler.click()
            page.wait_for_timeout(300)
        except Exception:
            pass

    # Find the description textarea inside the merged cell.
    desc_area = selected_row.locator(
        "td[name='product_id'] .o_field_product_label_section_and_note_cell textarea"
    ).first
    if desc_area.count() == 0 or not desc_area.is_visible():
        # Unhide any `d-none` textareas in the cell, then retarget.
        page.evaluate(
            """() => {
                document.querySelectorAll(
                    '.o_form_view .o_list_renderer .o_data_row.o_selected_row '
                    + "td[name='product_id'] .o_field_product_label_section_and_note_cell textarea.d-none"
                ).forEach(el => el.classList.remove('d-none'));
            }"""
        )
        desc_area = selected_row.locator(
            "td[name='product_id'] .o_field_product_label_section_and_note_cell textarea"
        ).first

    desc_area.wait_for(state="visible", timeout=5000)
    desc_area.click()
    try:
        desc_area.fill(text)
    except Exception:
        desc_area.press("Control+a")
        desc_area.press("Delete")
        desc_area.type(text, delay=10)
    page.wait_for_timeout(300)
    desc_area.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(300)
    try:
        search_for(page, "BENCH-EDIT-001")
    except Exception:
        pass
    page.wait_for_timeout(600)

    click_list_row(page, "BENCH-EDIT-001")
    page.wait_for_timeout(1200)
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Click 'Reset to Draft' in the statusbar.
    reset_btn = page.locator(
        ".o_statusbar_buttons button[name='button_draft']:visible, "
        ".o_statusbar_buttons button:visible:has-text('Reset to Draft')"
    )
    if reset_btn.count() == 0:
        reset_btn = page.locator(
            ".o_statusbar_buttons button:visible:has-text('Reset')"
        )
    reset_btn.first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Handle possible confirmation dialog.
    try:
        modal = page.locator(".modal:visible").last
        if modal.count() > 0:
            ok_btn = modal.locator(
                "button.btn-primary:visible"
            ).filter(has_text="OK")
            if ok_btn.count() > 0:
                ok_btn.first.click()
                page.wait_for_timeout(1000)
                _wait_no_loading(page)
    except Exception:
        pass

    # Scroll the invoice lines list into view.
    try:
        page.locator(
            ".o_form_view .o_list_renderer"
        ).first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    except Exception:
        pass

    _edit_label_cell(page, TARGET_TEXT)

    # Click an inert area of the sheet before saving (blur-vs-save race).
    try:
        page.locator(".o_form_sheet_bg, .o_form_sheet").first.click(
            position={"x": 5, "y": 5}
        )
        page.wait_for_timeout(300)
    except Exception:
        pass

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Click Confirm in the statusbar to repost the draft.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
