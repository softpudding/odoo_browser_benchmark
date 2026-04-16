"""Oracle for hr.create_employee_complete_profile.

Create a new employee Jordan Mercer with fields spread across three form areas:
- Main form: name, job position, work phone
- Work tab: work location (Home)
- Personal tab: certificate (Bachelor), marital status (Single)

Note: resource_calendar_id defaults to Standard 40h/week automatically.
"""

from benchmark.oracle_helpers import (
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def _click_tab(page, tab_text: str) -> None:
    """Click a notebook tab by visible text (case-insensitive partial match)."""
    page.locator(".o_notebook .nav-link").filter(has_text=tab_text).first.click()
    page.wait_for_timeout(500)


def _set_owl_selection(page, field_name: str, option_text: str) -> None:
    """Set an OWL select-menu field (o_select_menu widget, not native <select>)."""
    widget = page.locator(f".o_field_widget[name='{field_name}']").first
    widget.click()
    page.wait_for_timeout(300)
    page.locator(f".o_select_menu_item:has-text('{option_text}')").first.click()
    page.wait_for_timeout(300)


def oracle(page):
    login(page)
    navigate(page, "/odoo/employees")
    _wait_no_loading(page)

    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # --- Main form ---
    fill_field(page, "name", "Jordan Mercer")
    page.wait_for_timeout(300)

    set_many2one(page, "job_id", "Field Operations Coordinator")
    page.wait_for_timeout(500)

    fill_field(page, "work_phone", "+1 (555) 840-2200")
    page.wait_for_timeout(300)

    # --- Work tab ---
    _click_tab(page, "Work")

    set_many2one(page, "work_location_id", "Home")
    page.wait_for_timeout(500)

    # --- Personal tab ---
    _click_tab(page, "Personal")

    # Certificate level: OWL select-menu widget (not native <select>)
    _set_owl_selection(page, "certificate", "Bachelor")

    # Marital status: also OWL select-menu
    _set_owl_selection(page, "marital", "Single")

    # Save
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
