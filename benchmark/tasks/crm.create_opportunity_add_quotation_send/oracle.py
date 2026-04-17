"""Oracle for crm.create_opportunity_add_quotation_send.

Create a new CRM opportunity for Pinnacle Logistics Group, move to
Qualified stage, create a linked quotation with two product lines,
set customer reference and expiration, save, then send by email with
a custom subject.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_button,
    click_create,
    click_kanban_card,
    click_status_button,
    click_tab,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)

    # ── Step 1: Create new opportunity via kanban quick-create ─────────
    click_create(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)

    # The kanban quick-create form has: commercial_partner_id, partner_id,
    # name, email_from, phone, expected_revenue. NOT contact_name.

    # Set the Company (commercial_partner_id) to Pinnacle Logistics Group
    set_many2one(page, "commercial_partner_id", "Pinnacle Logistics Group")
    page.wait_for_timeout(500)

    # Set the opportunity name
    fill_field(page, "name", "Pinnacle Logistics Group")
    page.wait_for_timeout(300)

    # Set expected revenue
    fill_field(page, "expected_revenue", "45000")
    page.wait_for_timeout(300)

    # Set email in quick-create
    fill_field(page, "email_from", "derek.voss@pinnacle-logistics.example.com")
    page.wait_for_timeout(300)

    # Click "Add" to save the quick-create record, then open the full form
    # via the "Edit" button (pencil icon or open-form link)
    edit_btn = page.locator(
        ".o_kanban_quick_create .o_kanban_edit:visible, "
        ".o_kanban_quick_create button:has-text('Edit'):visible"
    )
    if edit_btn.count() > 0:
        edit_btn.first.click()
    else:
        # Try "Add" first, then open the card
        add_btn = page.locator(
            ".o_kanban_quick_create button.o_kanban_add:visible, "
            ".o_kanban_quick_create .o_kanban_add:visible"
        )
        if add_btn.count() > 0:
            add_btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            # Open the newly created card
            click_kanban_card(page, "Pinnacle Logistics Group")
        else:
            # Last resort: just press Enter to add and then open
            page.keyboard.press("Enter")
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            click_kanban_card(page, "Pinnacle Logistics Group")

    page.wait_for_timeout(1500)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # We should now be on the full opportunity form.
    # Fill contact_name in the "Contacts" tab (for opportunities, contact_name
    # is in the Contacts tab, not the main form area)
    click_tab(page, "Contacts")
    page.wait_for_timeout(500)
    fill_field(page, "contact_name", "Derek Voss")
    page.wait_for_timeout(300)

    # Move to Qualified stage via status bar
    stage_btn = page.locator(".o_statusbar_status button:has-text('Qualified')")
    stage_btn.first.click()
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Save the opportunity
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ── Step 2: Create linked quotation ─────────────────────────────────
    click_button(page, "New Quotation")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # Handle any dialog that may appear after clicking New Quotation
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        action_btn = modal.last.locator(
            "button.btn-primary:visible, "
            "button:has-text('Create'):visible, "
            "button:has-text('Confirm'):visible, "
            "button:has-text('Ok'):visible"
        )
        if action_btn.count() > 0:
            action_btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            _wait_for_ready(page)

    # Add first line: Warehouse Management Module x3 @ 8500
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 0, "product_template_id", "Warehouse Management Module")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "product_uom_qty", "3")
    page.wait_for_timeout(500)
    set_o2m_field(page, 0, "price_unit", "8500")
    page.wait_for_timeout(500)

    # Add second line: Implementation Service x1 @ 12000
    click_add_a_line(page)
    page.wait_for_timeout(500)
    set_o2m_many2one(page, 1, "product_template_id", "Implementation Service")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "product_uom_qty", "1")
    page.wait_for_timeout(500)
    set_o2m_field(page, 1, "price_unit", "12000")
    page.wait_for_timeout(500)

    # Set Customer Reference in Other Info tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)
    fill_field(page, "client_order_ref", "PLG-Q2-2026")
    page.wait_for_timeout(500)

    # Set Expiration date
    set_date(page, "validity_date", "07/01/2026")
    page.wait_for_timeout(500)

    # Save the quotation
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)

    # ── Step 3: Send quotation by email ─────────────────────────────────
    click_status_button(page, "Send")
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # Handle the "Configure your document layout" dialog if it appears
    layout_modal = page.locator(".modal:visible:has-text('Configure your document layout')")
    if layout_modal.count() > 0:
        continue_btn = layout_modal.last.locator(
            "button:has-text('Continue'), "
            "button:has-text('Save'), "
            ".modal-footer button.btn-primary"
        ).first
        continue_btn.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)

    # Now we should see the email compose wizard modal
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        m = modal.last

        # Set the subject
        subject = m.locator(
            ".o_field_widget[name='subject'] input"
        ).first
        subject.click()
        subject.fill("")
        subject.fill("Pinnacle Logistics - Warehouse Management Proposal")
        subject.press("Tab")
        page.wait_for_timeout(1000)

        # Click Send in the modal
        m.locator("button:has-text('Send')").first.click()
        page.wait_for_timeout(2000)
        _wait_no_loading(page)


run_oracle(oracle)
