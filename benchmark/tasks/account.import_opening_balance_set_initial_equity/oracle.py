"""Oracle for account.import_opening_balance_set_initial_equity.

Create a new move_type='entry' opening balance journal entry in
Accounting -> Journal Entries, fill two balanced lines
(Stock Valuation 10000 debit, Opening Balance 10000 credit), then post.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def _set_accounting_date(page, date_str):
    """Set the top-level `date` (Accounting Date) field on the entry form."""
    widget = page.locator(".o_field_widget[name='date']").first
    widget.scroll_into_view_if_needed()

    control = widget.locator("button, input, span").first
    control.click()
    page.wait_for_timeout(500)

    inp = widget.locator("input:visible").first
    if inp.count() == 0:
        inp = page.locator(
            ".o_datetime_picker:visible input, "
            ".o_datetime_picker_container:visible input"
        ).first

    inp.click(click_count=3)
    inp.press("Delete")
    inp.type(date_str, delay=40)
    page.wait_for_timeout(300)
    inp.press("Escape")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _click_add_line(page):
    add = page.locator(
        ".o_field_one2many[name='line_ids'] a.o_field_x2many_list_row_add, "
        ".o_field_one2many[name='line_ids'] td.o_field_x2many_list_row_add a"
    )
    if add.count() == 0:
        add = page.locator("td.o_field_x2many_list_row_add:visible a, a.o_field_x2many_list_row_add:visible")
    add.first.click()
    page.wait_for_timeout(700)


def _row(page, idx):
    return (
        page.locator(".o_field_one2many[name='line_ids']").first
        .locator(".o_data_row").nth(idx)
    )


def _fill_cell(page, row_idx, field_name, value, *, is_many2one=False):
    row = _row(page, row_idx)
    cell = row.locator(
        f"td[name='{field_name}'], .o_field_widget[name='{field_name}']"
    ).first
    cell.click()
    page.wait_for_timeout(300)
    editable = cell.locator("input, textarea").first
    editable.fill("")
    editable.press("Delete")
    page.wait_for_timeout(200)
    if is_many2one:
        editable.click()
        editable.type(value, delay=50)
        page.wait_for_timeout(1200)
        dropdown_items = page.locator(
            ".o-autocomplete--dropdown-menu .o-autocomplete--dropdown-item, "
            ".dropdown-menu .dropdown-item, "
            ".ui-autocomplete .ui-menu-item"
        )
        # Account dropdown items are formatted as "<code> <name>", e.g.
        # "140000 Stock Valuation". Exact-match on the name part to avoid
        # substring collisions (e.g., "Stock Valuation" vs "Stock Interim
        # (Received)").
        target = None
        count = dropdown_items.count()
        for i in range(min(count, 25)):
            try:
                txt = dropdown_items.nth(i).inner_text().strip()
            except Exception:
                continue
            if txt.lower() == value.lower():
                target = dropdown_items.nth(i)
                break
            parts = txt.split(None, 1)
            if len(parts) == 2 and parts[1].strip().lower() == value.lower():
                target = dropdown_items.nth(i)
                break
            if txt.lower().endswith(" " + value.lower()):
                target = dropdown_items.nth(i)
                break
        if target is not None:
            target.click()
        else:
            create_opt = dropdown_items.filter(has_text=f'Create "{value}"').first
            if create_opt.count() > 0:
                create_opt.click()
            else:
                editable.press("Enter")
    else:
        editable.fill(value)
        page.wait_for_timeout(200)
        editable.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _add_entry_line(page, row_idx, account, label, debit, credit):
    existing = (
        page.locator(".o_field_one2many[name='line_ids']").first
        .locator(".o_data_row").count()
    )
    if existing <= row_idx:
        _click_add_line(page)

    _fill_cell(page, row_idx, "account_id", account, is_many2one=True)
    _fill_cell(page, row_idx, "name", label)
    _fill_cell(page, row_idx, "debit", debit)
    _fill_cell(page, row_idx, "credit", credit)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/entries")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    fill_field(page, "ref", "OPEN-BAL-001")
    page.wait_for_timeout(400)

    _set_accounting_date(page, "01/01/2026")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    _add_entry_line(page, 0, "Stock Valuation", "Opening stock valuation", "10000.00", "0.00")
    _add_entry_line(page, 1, "Opening Balance", "Initial equity contribution", "0.00", "10000.00")

    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    click_status_button(page, "Post")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
