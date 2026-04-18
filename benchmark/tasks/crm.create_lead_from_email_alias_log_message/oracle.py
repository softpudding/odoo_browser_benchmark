"""Oracle for crm.create_lead_from_email_alias_log_message.

Flow:
1. Open Sales Teams list, click 'Inbound' team form.
2. Type 'leads-inbound' into the alias_name inline input and Save.
3. Navigate to /odoo/crm, create a new Lead with the requested name/email.
4. Open the chatter, click 'Send message', type the message, click Send.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_create,
    click_list_row,
    ensure_list_view,
    fill_field,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


TEAM_NAME = "Inbound"
TARGET_ALIAS = "leads-inbound"
LEAD_NAME = "Inbound Inquiry from Sample"
LEAD_EMAIL = "prospect@external.test"
CHATTER_MESSAGE = "Asked about Bench Pro pricing."
TAG_NAME = "Website"


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


def _set_alias_name(page, value):
    """Type into the alias_name inline input inside the Team Details group.

    On crm.team form, the alias_name field is rendered with `class='oe_inline'`
    inside a div[name='edit_alias']. Two inputs sit side-by-side
    (alias_name and alias_domain_id), so we target by [name='alias_name'].
    """
    widget = page.locator(".o_field_widget[name='alias_name']").first
    widget.wait_for(state="visible", timeout=15000)
    inp = widget.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)

    # ---- Step 1: Configure the team's email alias ----
    navigate(page, "/odoo/action-sales_team.crm_team_action_config")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    ensure_list_view(page)
    page.wait_for_timeout(500)

    click_list_row(page, TEAM_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    _set_alias_name(page, TARGET_ALIAS)
    page.wait_for_timeout(400)

    # Set Accept Emails From -> Authenticated Partners (alias_contact='partners').
    # In Odoo 19 this renders as Odoo's custom `o_select_menu` (NOT a native
    # <select>), so `set_selection` won't work. Click the toggler to open the
    # popover and click the matching option.
    toggler = page.locator(
        ".o_field_widget[name='alias_contact'] .o_select_menu_toggler"
    ).first
    toggler.click()
    page.wait_for_timeout(500)
    option = page.locator(
        ".o_select_menu_menu .o_select_menu_item:has-text('Authenticated Partners'), "
        ".o-dropdown--menu .o_select_menu_item:has-text('Authenticated Partners')"
    ).first
    option.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _dismiss_invite_modal_if_any(page)

    # ---- Step 2: Create the lead ----
    # Leads menu url in Odoo 19 CRM
    navigate(page, "/odoo/action-crm.crm_lead_all_leads")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    click_create(page)
    page.wait_for_timeout(900)
    _wait_for_ready(page)

    # Name on crm.lead form uses widget="text" -> textarea, not an input
    fill_text_field(page, "name", LEAD_NAME)
    page.wait_for_timeout(300)
    fill_field(page, "email_from", LEAD_EMAIL)
    page.wait_for_timeout(300)

    # Priority: click ONLY the first star -> priority='1' (Medium).
    # Per ODOO19_PATTERNS: star index 0 of o_priority_star widget writes '1'.
    stars = page.locator(".o_field_widget[name='priority'] .o_priority_star")
    if stars.count() >= 1:
        stars.nth(0).click()
        page.wait_for_timeout(300)

    # Tag: add existing 'Website' tag.
    add_many2many_tag(page, "tag_ids", TAG_NAME)
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _dismiss_invite_modal_if_any(page)

    # ---- Step 3: Post chatter message ----
    chatter = page.locator(".o-mail-Chatter, .o_chatter")
    if chatter.count() > 0:
        chatter.first.scroll_into_view_if_needed()
        page.wait_for_timeout(400)

    send_msg_btn = page.locator(
        "button:has-text('Send message'), "
        ".o-mail-Chatter button:has-text('Send message')"
    ).first
    send_msg_btn.click()
    page.wait_for_timeout(800)

    composer = page.locator(
        ".o-mail-Composer .o-mail-Composer-input, "
        ".o-mail-composer [contenteditable='true'], "
        ".o_mail_composer_input textarea, "
        "div[contenteditable='true'].odoo-editor-editable, "
        ".o-mail-Composer-input [contenteditable='true']"
    ).last
    composer.click()
    page.wait_for_timeout(300)
    composer.fill(CHATTER_MESSAGE)
    page.wait_for_timeout(400)

    send_btn = page.locator(
        "button.o-mail-Composer-send, "
        ".o-mail-Composer button:has-text('Send'), "
        ".o-mail-Composer button[type='submit']"
    ).first
    send_btn.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
