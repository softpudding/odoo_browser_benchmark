"""Oracle for project.set_project_deadline_tags.

Find project "Meridian Platform Build" in kanban, open its settings via the
three-dot menu, set Deadline to 06/30/2026, add tags Launch and Q3, then save.

The seed pre-sets date_start=2026-06-01 so the form's required="date_start or date"
validation passes when only the deadline (end date) is set.  The daterange
widget opens focused on June 2026 (adjustFocus uses values[0]=June1 when
values[1] is empty), so no month navigation is needed.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    add_many2many_tag,
    save_form,
)

PROJECT_NAME = "Meridian Platform Build"
TAGS = ["Launch", "Q3"]


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Hover the project card to reveal the kebab menu
    card = page.locator(f".o_kanban_record:has-text('{PROJECT_NAME}')").first
    card.wait_for(state="visible", timeout=10000)
    card.hover()
    page.wait_for_timeout(500)

    # Click the three-dot (kebab) button
    kebab = card.locator(".o_dropdown_kanban button").first
    kebab.click(force=True)
    page.wait_for_timeout(500)

    # Open Settings
    page.locator("a:has-text('Settings'), .dropdown-item:has-text('Settings')").first.click()
    page.wait_for_timeout(1500)
    _wait_for_ready(page)

    # The end-date input (data-field="date") is inside the date_start daterange widget.
    # Clicking it fires t-on-focus → picker.activeInput = endDateField → OWL re-renders
    # → useEffect calls openPicker(1) → calendar opens focused on end date (index 1).
    # adjustFocus picks values[0]=June1 (pre-seeded start date) as the focus date,
    # so the picker opens showing June 2026 — no month navigation needed.
    end_inp = page.locator(".o_field_widget[name='date_start'] input[data-field='date']").first
    end_inp.wait_for(state="visible", timeout=10000)
    end_inp.click()
    page.wait_for_timeout(1200)

    # Wait for the date picker popover
    picker = page.locator(".o_datetime_picker").first
    picker.wait_for(state="visible", timeout=10000)

    # Click June 30 (no navigation needed — picker already shows June 2026)
    # Exclude o_out_of_range cells (days from adjacent months).
    # always_range=True → pickerProps.range=True → no auto-close after clicking a day.
    day_cell = picker.locator(".o_date_item_cell:not(.o_out_of_range)").filter(has_text="30").last
    day_cell.click()
    page.wait_for_timeout(800)

    # Close picker with Escape. Odoo popover has closeOnEscape=True by default:
    # Escape → props.close() → onClose() → apply() → record.update({date: June30})
    # The start date (June1) is already set and unchanged, so only {date: June30}
    # is sent, and the form validation passes.
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # Add tags
    for tag in TAGS:
        add_many2many_tag(page, "tag_ids", tag)

    # Save the form
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
