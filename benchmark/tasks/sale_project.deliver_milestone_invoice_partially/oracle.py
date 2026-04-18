"""Oracle for sale_project.deliver_milestone_invoice_partially.

Mark only the "Design Phase" milestone as reached on the auto-generated
project, then return to S-BENCH-MS-001 and create a draft Regular invoice
for the partially-delivered quantity (1 of 3).
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    modal_click_button,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


PARTNER_NAME = "Bench Milestone Client"
SO_REF = "S-BENCH-MS-001"


def _open_project_kebab_action(page, project_name, action_text):
    """Open the kebab menu on a project kanban card and click an action."""
    card = page.locator(f".o_kanban_record:has-text('{project_name}')").first
    card.scroll_into_view_if_needed()
    card.hover()
    page.wait_for_timeout(400)

    kebab = card.locator(
        ".o_dropdown_kanban button, .o_dropdown_kanban .dropdown-toggle"
    ).first
    kebab.click(force=True)
    page.wait_for_timeout(500)

    action = page.locator(
        f"a.dropdown-item:visible:has-text('{action_text}'), "
        f"a.oe_kanban_action:visible:has-text('{action_text}'), "
        f"a[name]:visible:has-text('{action_text}'), "
        f".dropdown-menu:visible .dropdown-item:has-text('{action_text}')"
    ).first
    action.click()
    page.wait_for_load_state("load")
    _wait_for_ready(page)


def _mark_milestone_reached(page, milestone_name):
    """Tick the 'Reached' checkbox on the row for milestone_name."""
    # Wait for the milestones list to render
    page.wait_for_selector(
        ".o_list_view .o_data_row, .o_kanban_view .o_kanban_record",
        timeout=10000,
    )
    page.wait_for_timeout(500)

    row = page.locator(
        f".o_list_view .o_data_row:has-text('{milestone_name}')"
    ).first

    # Find the is_reached checkbox cell in this row
    cb = row.locator(
        "td[name='is_reached'] input[type='checkbox'], "
        ".o_field_widget[name='is_reached'] input[type='checkbox']"
    )
    if cb.count() > 0:
        if not cb.first.is_checked():
            cb.first.click(force=True)
            page.wait_for_timeout(500)
            _wait_no_loading(page)
        return

    # Fallback: open the row in form view, set boolean, save
    row.click(force=True)
    page.wait_for_load_state("load")
    _wait_for_ready(page)

    cb = page.locator(
        ".o_field_widget[name='is_reached'] input[type='checkbox']"
    ).first
    if not cb.is_checked():
        cb.click(force=True)
        page.wait_for_timeout(500)
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)

    # ------------------------------------------------------------------
    # Step 1: open Project app, find the auto-generated project, and open
    #         its Milestones list via the kanban kebab menu.
    # ------------------------------------------------------------------
    navigate(page, "/odoo/project")
    _wait_no_loading(page)

    # The auto-generated project is named after the SO line / partner.
    # Try by partner name first.
    project_card = page.locator(
        f".o_kanban_record:has-text('{PARTNER_NAME}')"
    )
    project_name = PARTNER_NAME
    if project_card.count() == 0:
        # Fall back to product / SO reference text.
        project_card = page.locator(
            f".o_kanban_record:has-text('{SO_REF}'), "
            f".o_kanban_record:has-text('Bench Milestone Service')"
        )
        if project_card.count() > 0:
            project_name = "Bench Milestone Service"

    _open_project_kebab_action(page, project_name, "Milestones")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # Step 2: Mark only "Design Phase" as reached.
    # ------------------------------------------------------------------
    _mark_milestone_reached(page, "Design Phase")

    # Save any pending changes (some flows require explicit save).
    try:
        save_form(page)
    except Exception:
        pass
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # Step 3: Open the SO and click Create Invoice.
    # ------------------------------------------------------------------
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, SO_REF)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # The Create Invoice button can live on the statusbar or as an
    # action button — try statusbar first.
    try:
        click_status_button(page, "Create Invoice")
    except Exception:
        page.locator(
            "button:visible:has-text('Create Invoice')"
        ).first.click()
        page.wait_for_load_state("load")
        _wait_no_loading(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # ------------------------------------------------------------------
    # Step 4: In the wizard, leave "Regular invoice" selected and click
    #         the Create Draft / Create Invoice button.
    # ------------------------------------------------------------------
    page.wait_for_selector(".modal:visible", timeout=10000)
    modal = page.locator(".modal:visible").last

    # Make sure "Regular invoice" radio is selected (it should be the default
    # but make this explicit so we don't depend on default ordering).
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
            page.wait_for_timeout(500)
            _wait_no_loading(page)
        except Exception:
            pass

    # Click the wizard's create button.
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
