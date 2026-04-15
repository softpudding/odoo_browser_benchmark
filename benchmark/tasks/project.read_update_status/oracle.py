"""Oracle for project.read_update_status.

Open the "Q2 Launch" project, navigate to project settings via the kebab menu,
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

    # Open the kebab menu on the Q2 Launch project card and go to Settings
    card = page.locator(".o_kanban_record:has-text('Q2 Launch')").first
    # Hover to make the kebab visible
    card.hover()
    page.wait_for_timeout(300)

    # Click the kebab button inside .o_dropdown_kanban
    kebab = card.locator(".o_dropdown_kanban button, .o_dropdown_kanban .dropdown-toggle").first
    kebab.click(force=True)
    page.wait_for_timeout(500)

    # Click Settings in the dropdown — use specific selector to avoid
    # matching container divs
    settings_link = page.locator(".dropdown-item:visible:has-text('Settings')").first
    settings_link.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    # Click Description tab (if present)
    desc_tab = page.locator(".o_notebook .nav-link:has-text('Description')")
    if desc_tab.count() > 0:
        desc_tab.first.click()
        page.wait_for_timeout(500)

    # Fill the description field (try HTML editor, then textarea)
    desc_editable = page.locator(
        '.o_field_widget[name="description"] .note-editable, '
        '.o_field_widget[name="description"] .odoo-editor-editable, '
        '.o_field_widget[name="description"] [contenteditable="true"], '
        '.o_field_widget[name="description"] textarea'
    )
    if desc_editable.count() > 0:
        desc_editable.first.click()
        desc_editable.first.fill("2 of 5 tasks complete")
    else:
        page.locator('.o_field_widget[name="description"]').first.click()
        page.keyboard.type("2 of 5 tasks complete")
    page.wait_for_timeout(500)

    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
