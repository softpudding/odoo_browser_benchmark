"""Oracle for sale_timesheet.log_timesheet_on_so_invoice_delivered.

Opens SO S-BENCH-TS-001, navigates to the auto-generated task, logs two
timesheet rows totalling 6h, returns to the SO, clicks Create Invoice,
keeps the Regular invoice radio, and creates the draft invoice.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


SO_REF = "S-BENCH-TS-001"


def _click_smart_button_by_text(page, text):
    """Click a smart button in the button_box whose label contains text."""
    btn = page.locator(
        f"button.oe_stat_button:has-text('{text}')"
    ).first
    btn.wait_for(state="visible", timeout=10000)
    btn.scroll_into_view_if_needed()
    btn.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def _find_ts_row(page):
    """Return the currently-selected row inside the timesheets o2m.

    The list uses editable='top' so newly-added rows are inserted at the
    top — fall back to .first (not .last) if the selected marker isn't
    on the row.
    """
    ts_field = page.locator(".o_field_widget[name='timesheet_ids']").first
    row = ts_field.locator(".o_data_row.o_selected_row").first
    if row.count() == 0:
        row = ts_field.locator(".o_data_row").first
    return row


def _fill_ts_cell(page, cell_name, text, *, as_textarea=False):
    """Click the cell, fill the visible input/textarea, commit via Tab."""
    row = _find_ts_row(page)
    cell = row.locator(f"td[name='{cell_name}']").first
    cell.scroll_into_view_if_needed()
    cell.click()
    page.wait_for_timeout(300)
    selector = "textarea, input" if as_textarea else "input, textarea"
    inp = cell.locator(selector).first
    inp.fill("")
    inp.type(text, delay=15)
    page.wait_for_timeout(200)


def _fill_ts_cell_m2o(page, cell_name, text):
    """Fill a many2one cell: type text, pick the dropdown item."""
    row = _find_ts_row(page)
    cell = row.locator(f"td[name='{cell_name}']").first
    cell.scroll_into_view_if_needed()
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.type(text, delay=20)
    page.wait_for_timeout(900)
    dropdown_item = page.locator(
        f".dropdown-menu .dropdown-item:has-text('{text}'), "
        f"ul.ui-autocomplete li:has-text('{text}')"
    ).first
    dropdown_item.wait_for(state="visible", timeout=5000)
    dropdown_item.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _add_timesheet_row(page, date_str, description, hours_str, employee_text):
    """Click 'Add a line' inside the Timesheets tab and fill one row."""
    # Make sure we're on the Timesheets tab
    tab = page.locator(
        "a.nav-link:has-text('Timesheets'), "
        ".o_notebook_headers a:has-text('Timesheets')"
    ).first
    tab.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Find the Timesheets one2many list inside the task form and click
    # "Add a line".
    ts_field = page.locator(".o_field_widget[name='timesheet_ids']").first
    add_link = ts_field.locator(
        "a.o_field_x2many_list_row_add, "
        "td.o_field_x2many_list_row_add a"
    ).first
    add_link.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Fill in order: date -> employee -> name -> unit_amount.
    # date cell
    _fill_ts_cell(page, "date", date_str)
    page.keyboard.press("Escape")  # close any datepicker popover
    page.wait_for_timeout(300)

    # employee_id — m2o with dropdown
    _fill_ts_cell_m2o(page, "employee_id", employee_text)

    # name (description)
    _fill_ts_cell(page, "name", description)

    # unit_amount (float_time)
    _fill_ts_cell(page, "unit_amount", hours_str)
    page.keyboard.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)

    # --- Step 1: open Sales app and SO ---
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    click_list_row(page, SO_REF)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # --- Step 2: click the combined Tasks smart button ---
    _click_smart_button_by_text(page, "Tasks")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # --- Step 3: open the single task in the list (or kanban) ---
    # The tasks action from action_view_project_ids lands on a list by default.
    # Click the first data row (only one task).
    task_row = page.locator(".o_list_view .o_data_row").first
    if task_row.count() > 0:
        task_row.click(force=True)
    else:
        # Fallback: kanban view
        page.locator(".o_kanban_view .o_kanban_record").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)
    _wait_no_loading(page)

    # --- Step 4: log two timesheet rows ---
    _add_timesheet_row(
        page,
        date_str="04/15/2026",
        description="Initial consulting session",
        hours_str="4:00",
        employee_text="Mitchell Admin",
    )
    # Save the form to persist the first row before adding another
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    _add_timesheet_row(
        page,
        date_str="04/19/2026",
        description="Follow-up session",
        hours_str="2:00",
        employee_text="Mitchell Admin",
    )

    # Save task
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # --- Step 5: return to the sales order ---
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    click_list_row(page, SO_REF)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # --- Step 6: click Create Invoice ---
    try:
        click_status_button(page, "Create Invoice")
    except Exception:
        page.locator(
            "button:visible:has-text('Create Invoice')"
        ).first.click()
        page.wait_for_load_state("load")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    # --- Step 7: wizard — keep Regular invoice, click create ---
    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    # Explicitly click the Regular invoice radio for determinism
    regular = modal.locator(
        ".o_field_widget[name='advance_payment_method'] "
        ".o_selection_badge:has-text('Regular invoice'), "
        ".o_field_widget[name='advance_payment_method'] "
        "label:has-text('Regular invoice'), "
        ".o_field_widget[name='advance_payment_method'] "
        ".o_radio_item:has-text('Regular invoice')"
    )
    if regular.count() > 0:
        try:
            regular.first.click()
            page.wait_for_timeout(400)
            _wait_no_loading(page)
        except Exception:
            pass

    create_btn = modal.locator(
        "button[name='create_invoices'], "
        "button:has-text('Create Draft'), "
        "button:has-text('Create Invoice')"
    )
    create_btn.first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)


run_oracle(oracle)
