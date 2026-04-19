"""Oracle for crm.duplicate_lead_convert_to_opportunity.

Flow:
1. Open the Leads list action (crm.crm_lead_all_leads).
2. Open 'Bench Template Lead' row.
3. Open cog/Actions dropdown -> click Duplicate.
4. On the copy, rename title to 'Bench Cloned Opp' and Save.
5. Click header 'Convert to Opportunity' -> wizard opens.
6. In wizard: select 'Link to an existing customer' radio, type new
   partner name into the Customer autocomplete, pick the
   'Create "Bench Cloned Customer"' quick-create option.
7. Click 'Create Opportunity' to apply.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


TEMPLATE_LEAD_NAME = "Bench Template Lead"
CLONED_LEAD_NAME = "Bench Cloned Opp"
NEW_PARTNER_NAME = "Bench Cloned Customer"


def _dismiss_invite_modal_if_any(page):
    for _ in range(3):
        invite = page.locator(
            ".modal.show:visible, .modal.d-block:visible"
        ).filter(has_text="Invite teammates")
        if invite.count() == 0:
            return
        discard = invite.first.locator(
            "button:has-text('Discard'), "
            "button:has-text('Close'), "
            "button.btn-close"
        ).first
        try:
            discard.click(timeout=3000)
        except Exception:
            page.keyboard.press("Escape")
        page.wait_for_timeout(600)


def _click_cog_duplicate(page):
    # Open the cog/Actions menu in the control panel.
    cog = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_cp_action_menus button:has(.fa-cog):visible, "
        ".o_control_panel_actions button.dropdown-toggle:visible, "
        ".o_control_panel button:has(.fa-cog):visible"
    ).first
    cog.click()
    page.wait_for_timeout(500)
    dup_item = page.locator(
        ".o-dropdown--menu:visible .dropdown-item:has-text('Duplicate'), "
        ".dropdown-menu:visible .dropdown-item:has-text('Duplicate')"
    ).first
    dup_item.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


def _wizard_pick_convert_radio(page):
    """Force the Conversion Action radio (field 'name') to 'convert'."""
    modal = page.locator(".modal.show:visible, .modal.d-block:visible").last
    modal.wait_for(state="visible", timeout=10000)
    page.wait_for_timeout(400)
    radio = modal.locator(
        ".o_field_widget[name='name'] input.o_radio_input[data-value='convert']"
    ).first
    if radio.count() > 0:
        try:
            radio.check(force=True, timeout=3000)
        except Exception:
            radio.click(force=True, timeout=3000)
        page.wait_for_timeout(800)
        return
    # Fallback
    label = modal.locator(
        ".o_field_widget[name='name'] label:has-text('Convert to opportunity')"
    ).first
    if label.count() > 0:
        label.click(force=True, timeout=3000)
        page.wait_for_timeout(800)


def _wizard_pick_existing_radio(page):
    """In the convert-to-opportunity wizard, click the 'Link to an existing
    customer' radio inside the action group (value='exist')."""
    modal = page.locator(".modal.show:visible, .modal.d-block:visible").last
    modal.wait_for(state="visible", timeout=10000)
    page.wait_for_timeout(800)
    # Try broad search first — find any input[data-value='exist'] inside modal.
    attempts = [
        "input.o_radio_input[data-value='exist']",
        "input[type='radio'][data-value='exist']",
        ".o_radio_item:has-text('existing') input[type='radio']",
        ".o_radio_item:has-text('Link to an existing') input[type='radio']",
        "label.o_form_label:has-text('existing')",
        "label:has-text('Link to an existing customer')",
    ]
    for sel in attempts:
        loc = modal.locator(sel).first
        try:
            if loc.count() > 0:
                try:
                    loc.check(force=True, timeout=3000)
                except Exception:
                    loc.click(force=True, timeout=3000)
                page.wait_for_timeout(700)
                return
        except Exception:
            continue
    # Dump HTML for debug
    try:
        html = modal.inner_html()
        snippet = html[:1500]
        raise RuntimeError(
            "Could not find 'Link to an existing customer' radio. "
            f"Modal HTML snippet: {snippet}"
        )
    except Exception as e:
        raise RuntimeError(f"Radio not found; modal html capture failed: {e}")


def _wizard_quick_create_partner(page, value):
    """In the wizard, type the new partner name in the Customer autocomplete
    and pick the 'Create "<value>"' option."""
    modal = page.locator(".modal.show:visible, .modal.d-block:visible").last
    # After clicking the 'exist' radio, the partner_id widget materializes.
    # Wait a moment for the onchange to propagate then the DOM to mount.
    page.wait_for_timeout(800)
    widget = modal.locator(".o_field_widget[name='partner_id']").first
    try:
        widget.wait_for(state="visible", timeout=10000)
    except Exception:
        # Dump modal for debug
        html = modal.inner_html()[:2000]
        raise RuntimeError(
            f"partner_id widget not visible after clicking 'exist' radio. "
            f"Modal HTML: {html}"
        )
    inp = widget.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    page.wait_for_timeout(900)
    # The autocomplete dropdown can attach outside the modal (portal), so
    # use a page-level locator.
    dropdown = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".o-autocomplete--dropdown-menu:visible li, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete:visible .ui-menu-item"
    )
    # Prefer 'Create "X"' entries (quick-create via name_create).
    target = dropdown.filter(has_text=f'Create "{value}"').first
    if target.count() == 0:
        target = dropdown.filter(has_text=f"Create {value}").first
    if target.count() == 0:
        # Fallback to a generic 'Create' entry, but prefer one that doesn't
        # say 'Create and edit'.
        create_candidates = dropdown.filter(has_text="Create")
        chosen = None
        for i in range(create_candidates.count()):
            txt = create_candidates.nth(i).inner_text()
            if "edit" in txt.lower():
                continue
            chosen = create_candidates.nth(i)
            break
        target = chosen if chosen is not None else create_candidates.first
    target.click()
    page.wait_for_timeout(900)
    _wait_no_loading(page)


def oracle(page):
    login(page)

    # ---- Step 1: open the seeded lead ----
    navigate(page, "/odoo/action-crm.crm_lead_all_leads")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_list_row(page, TEMPLATE_LEAD_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(600)
    _dismiss_invite_modal_if_any(page)

    # ---- Step 2: Duplicate via cog Actions menu ----
    _click_cog_duplicate(page)
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # ---- Step 3: Rename copy + Save ----
    fill_text_field(page, "name", CLONED_LEAD_NAME)
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _dismiss_invite_modal_if_any(page)

    # ---- Step 4: Convert to Opportunity (header button) ----
    convert_btn = page.locator(
        "button.oe_highlight:has-text('Convert to Opportunity'):visible, "
        "button:has-text('Convert to Opportunity'):visible"
    ).first
    convert_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # ---- Wizard: first force Conversion Action='Convert' (the email was
    # copied from the template, so by default the wizard auto-selects
    # 'Merge with existing opportunities' when the duplicate shares email).
    _wizard_pick_convert_radio(page)
    _wizard_pick_existing_radio(page)
    _wizard_quick_create_partner(page, NEW_PARTNER_NAME)

    # Click 'Create Opportunity' to apply (name='action_apply').
    apply_btn = page.locator(
        ".modal:visible button[name='action_apply'], "
        ".modal:visible footer button:has-text('Create Opportunity'), "
        ".modal:visible footer button.btn-primary"
    ).first
    apply_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)
    _dismiss_invite_modal_if_any(page)


run_oracle(oracle)
