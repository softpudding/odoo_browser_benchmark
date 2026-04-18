"""Oracle for account.create_recurring_journal_entry.

Create a new move_type='entry' journal entry in Accounting -> Journal Entries,
fill two balanced lines (Rent 1000 debit, Bank 1000 credit), schedule a
chatter activity for next month, then post.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_status_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    schedule_activity,
    _wait_for_ready,
    _wait_no_loading,
)


def _set_accounting_date(page, date_str):
    """Set the top-level `date` (Accounting Date) field.

    In Odoo 19 the `date` field on account.move renders as a DateTimeInput
    which may show as a <button>/span with today's default. We click it to
    focus, clear, then type the MM/DD/YYYY value.
    """
    widget = page.locator(".o_field_widget[name='date']").first
    widget.scroll_into_view_if_needed()

    # Click whatever is inside (button/span/input) to activate editing
    # Prefer the inner control element.
    control = widget.locator("button, input, span").first
    control.click()
    page.wait_for_timeout(500)

    inp = widget.locator("input:visible").first
    # Fall back to picker popup input
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
    # section_and_note_text renders a textarea for non-section rows
    editable = cell.locator("input, textarea").first
    # Clear whatever autocomplete may have pre-filled
    editable.fill("")
    editable.press("Delete")
    page.wait_for_timeout(200)
    if is_many2one:
        editable.click()
        # .type() dispatches real keystrokes so autocomplete fires
        editable.type(value, delay=50)
        page.wait_for_timeout(1200)
        dropdown_items = page.locator(
            ".o-autocomplete--dropdown-menu .o-autocomplete--dropdown-item, "
            ".dropdown-menu .dropdown-item, "
            ".ui-autocomplete .ui-menu-item"
        )
        # Account dropdown items are formatted as "<code> <name>", e.g.
        # "612000 Rent". We need to match the name part exactly, not any
        # item whose display contains the value as a substring (otherwise
        # "Rent" matches "Current Assets" via "cur**rent**").
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
            # Pattern "<digits> <name>"
            parts = txt.split(None, 1)
            if len(parts) == 2 and parts[1].strip().lower() == value.lower():
                target = dropdown_items.nth(i)
                break
            # Also allow "name (something)" style
            if txt.lower().endswith(" " + value.lower()):
                target = dropdown_items.nth(i)
                break
        if target is not None:
            target.click()
        else:
            # Last resort: pick the Create option to avoid clicking the wrong row
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

    fill_field(page, "ref", "Bench Rent Apr")
    page.wait_for_timeout(400)

    _set_accounting_date(page, "05/01/2026")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    _add_entry_line(page, 0, "Rent", "April rent expense", "1000.00", "0.00")
    _add_entry_line(page, 1, "Tax Paid", "Input tax on rent", "50.00", "0.00")
    _add_entry_line(page, 2, "Bank", "April rent payment", "0.00", "1050.00")

    page.locator(".o_form_sheet").first.click()
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    schedule_activity(
        page,
        activity_type="To-Do",
        summary="Post next month's rent entry",
        due_date="06/01/2026",
    )
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    click_status_button(page, "Post")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
