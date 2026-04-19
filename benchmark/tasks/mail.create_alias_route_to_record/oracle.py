"""Oracle for mail.create_alias_route_to_record.

Flow:
1. Navigate to /odoo/settings.
2. Scroll down to Developer Tools block, click 'Activate the developer mode'.
3. After the page reloads with ?debug=1, navigate to the Aliases list
   (action=mail.mail_alias_action).
4. Click New to open a fresh mail.alias form.
5. Fill alias_name = 'benchalias'.
6. Set alias_model_id = 'Lead/Opportunity' (crm.lead).
7. Fill alias_defaults with "{'team_id': <id-of-Bench-Alias-Team>}".
8. Set alias_contact = 'Everyone'.
9. Save.
"""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_create,
    login,
    navigate,
    run_oracle,
    save_form,
)


TEAM_NAME = "Bench Alias Team"
TARGET_ALIAS = "benchalias"


def _activate_developer_mode(page):
    """Click the 'Activate the developer mode' link in Settings.

    The link lives inside the ResConfigDevTool widget rendered at the
    bottom of the Developer Tools section on the Settings form. It
    triggers `router.pushState({ debug: 1 }, { reload: true })`, so the
    page reloads with ?debug=1 in the URL, which unlocks the Technical
    menu (gated by base.group_no_one).
    """
    # Already in debug mode? Nothing to do.
    if "debug=" in (page.url or "") and "debug=0" not in (page.url or ""):
        return

    # The developer-tool widget block lives deep in the Settings form.
    link = page.locator(
        "#developer_tool a:has-text('Activate the developer mode'), "
        ".o_widget_res_config_dev_tool a:has-text('Activate the developer mode')"
    ).filter(has_not_text="assets").filter(has_not_text="tests").first
    if link.count() == 0:
        link = page.locator("a:has-text('Activate the developer mode')").filter(
            has_not_text="assets",
        ).filter(has_not_text="tests").first
    if link.count() == 0:
        raise RuntimeError("Could not locate 'Activate the developer mode' link on Settings page")

    link.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    link.click()
    # The widget calls router.pushState(..., { reload: true }) — the page
    # performs a full reload. Wait robustly for the reload + client init.
    try:
        page.wait_for_url("**debug=1**", timeout=15000)
    except Exception:
        pass
    page.wait_for_load_state("load")
    page.wait_for_load_state("domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    # Wait for the webclient action manager to re-render after reload.
    try:
        page.wait_for_selector(".o_action_manager", timeout=30000)
    except Exception:
        pass
    _wait_no_loading(page)
    page.wait_for_timeout(1500)


def _resolve_team_id(page):
    """Read the database id of the seeded Bench Alias Team via the web
    orm_service. The oracle cheats here because the human prompt tells
    the agent to do the same lookup via the UI — an oracle doing the UI
    lookup would be brittle.
    """
    result = page.evaluate(
        """
        async (teamName) => {
            const resp = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'crm.team',
                        method: 'search_read',
                        args: [[['name', '=', teamName]], ['id']],
                        kwargs: {},
                    },
                }),
            });
            const data = await resp.json();
            return data.result;
        }
        """,
        TEAM_NAME,
    )
    if not result:
        raise RuntimeError(f"Could not find crm.team named '{TEAM_NAME}'")
    return result[0]["id"]


def _fill_alias_defaults(page, value):
    """alias_defaults is a plain Text field rendered as a textarea."""
    # Dismiss anything (autocomplete dropdowns, tooltips) that might be
    # covering the area around the textarea.
    page.evaluate(
        "document.querySelectorAll('.o-tooltip, .tooltip, .o-autocomplete--dropdown-menu, .o-dropdown--menu').forEach(el => { if (el && el.remove) el.remove(); })"
    )
    page.mouse.move(0, 0)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)

    widget = page.locator(".o_field_widget[name='alias_defaults']").first
    widget.wait_for(state="visible", timeout=10000)
    ta = widget.locator("textarea").first
    ta.scroll_into_view_if_needed()
    page.wait_for_timeout(200)
    try:
        ta.click(force=True, timeout=5000)
    except Exception:
        # If click-through still fails, focus via JS and type directly.
        ta.evaluate("el => el.focus()")
    ta.fill("")
    ta.fill(value)
    ta.press("Tab")
    page.wait_for_timeout(500)


def _set_alias_contact_everyone(page):
    """alias_contact is a standard HTML <select> on the generic
    mail.alias form view (unlike the custom o_select_menu on crm.team).
    """
    widget = page.locator(".o_field_widget[name='alias_contact']").first
    widget.wait_for(state="visible", timeout=10000)

    # Try native <select> first (mail.alias default form uses it).
    select = widget.locator("select")
    if select.count() > 0:
        try:
            select.first.select_option(label="Everyone")
            page.wait_for_timeout(300)
            return
        except Exception:
            pass

    # Fall back to the o_select_menu custom widget.
    toggler = widget.locator(".o_select_menu_toggler").first
    if toggler.count() > 0:
        toggler.click()
        page.wait_for_timeout(400)
        option = page.locator(
            ".o_select_menu_menu .o_select_menu_item:has-text('Everyone'), "
            ".o-dropdown--menu .o_select_menu_item:has-text('Everyone')"
        ).first
        option.click()
        page.wait_for_timeout(300)


def oracle(page):
    login(page)

    # --- Step 1: Activate developer mode ---
    navigate(page, "/odoo/settings")
    _wait_no_loading(page)
    page.wait_for_timeout(600)
    _activate_developer_mode(page)

    # --- Step 2: Fetch the seeded Bench Alias Team id via the orm ---
    team_id = _resolve_team_id(page)

    # --- Step 3: Open the Aliases list (Technical > Email > Aliases) ---
    # Direct action URL (equivalent to Settings > Technical > Email > Aliases).
    navigate(page, "/odoo/action-mail.mail_alias_action")
    _wait_no_loading(page)
    page.wait_for_timeout(600)

    # --- Step 4: Create a new alias ---
    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # --- Step 5: Fill alias_name ---
    # alias_name renders inside a .oe_inline flex header on the alias form.
    widget = page.locator(".o_field_widget[name='alias_name']").first
    widget.wait_for(state="visible", timeout=10000)
    inp = widget.locator("input").first
    inp.click()
    inp.fill("")
    inp.fill(TARGET_ALIAS)
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # --- Step 6: Set alias_model_id = Lead (crm.lead) ---
    # The ir.model record for crm.lead has name='Lead' (from
    # `_description = 'Lead'`) and model='crm.lead'. We type the technical
    # name 'crm.lead' because it uniquely identifies the record via
    # `_rec_names_search = ['name', 'model']`.
    model_widget = page.locator(".o_field_widget[name='alias_model_id']").first
    model_widget.wait_for(state="visible", timeout=10000)
    m2o_input = model_widget.locator("input").first
    m2o_input.click()
    m2o_input.fill("")
    m2o_input.type("crm.lead", delay=30)
    page.wait_for_timeout(1200)

    # Scan autocomplete options; click the first one whose <li> is NOT a
    # "Create …" / "Search More …" quick-create entry and whose label
    # matches the 'Lead' display name for crm.lead.
    items = page.locator(
        "ul.o-autocomplete--dropdown-menu li.o-autocomplete--dropdown-item"
    )
    items.first.wait_for(state="visible", timeout=10000)
    n = items.count()
    clicked = False
    for i in range(n):
        item = items.nth(i)
        css = item.get_attribute("class") or ""
        text = (item.inner_text() or "").strip()
        if "o_m2o_dropdown_option" in css:
            continue  # skip Create / Search More entries
        # For ir.model the autocomplete label is the `name` ('Lead'),
        # which may equal just 'Lead'. Ensure it's not another model
        # whose name contains 'Lead' (e.g. 'Lead Tag').
        if text == "Lead":
            item.click()
            clicked = True
            break
    if not clicked:
        # Fall back: first non-create option (name_search via 'crm.lead'
        # should return exactly one row — the crm.lead ir.model).
        for i in range(n):
            item = items.nth(i)
            css = item.get_attribute("class") or ""
            if "o_m2o_dropdown_option" in css:
                continue
            item.click()
            clicked = True
            break
    if not clicked:
        raise RuntimeError(
            "Could not find crm.lead autocomplete option; options seen: "
            + str([items.nth(i).inner_text() for i in range(n)])
        )
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # --- Step 7: alias_defaults = "{'team_id': N}" ---
    _fill_alias_defaults(page, "{'team_id': %d}" % team_id)

    # --- Step 8: alias_contact = 'Everyone' ---
    _set_alias_contact_everyone(page)

    # --- Step 9: Save ---
    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
