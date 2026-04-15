"""Oracle for project.read_update_status.

Open the "Q2 Launch" project, navigate to project settings via the ⋮ menu,
and type the description "2 of 5 tasks complete". The oracle knows the answer
from the seed data (2 Done out of 5 total tasks).
"""

from benchmark.oracle_helpers import (
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # Open the ⋮ menu on the Q2 Launch project card and go to Settings
    card = page.locator(".o_kanban_record:has-text('Q2 Launch')").first
    kebab = card.locator(".o_kanban_manage_toggle_button, button.dropdown-toggle").first
    kebab.click()
    page.wait_for_timeout(500)

    page.locator(".dropdown-menu a:has-text('Settings'), .o_kanban_manage_section a:has-text('Settings')").first.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    # Click Description tab (if present) and fill description
    # Try to find a Description tab; if not found, the field may already be visible
    desc_tab = page.locator(".o_notebook .nav-link:has-text('Description')")
    if desc_tab.count() > 0:
        desc_tab.first.click()
        page.wait_for_timeout(500)

    # Fill the description field (HTML editor)
    desc_field = page.locator(".o_field_widget[name='description'] textarea, .o_field_widget[name='description'] .note-editable, .o_field_widget[name='description'] .odoo-editor-editable")
    desc_field.first.click()
    desc_field.first.fill("2 of 5 tasks complete")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
