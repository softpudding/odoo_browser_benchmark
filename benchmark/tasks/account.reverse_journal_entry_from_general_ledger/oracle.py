"""Oracle for account.reverse_journal_entry_from_general_ledger.

Drill into the Miscellaneous Journal Items report (grouped by move),
expand the group whose reference is BENCH-GL-REV, open the
account.move form, click the 'Reverse Entry' header statusbar button
to open the account.move.reversal wizard, leave the default
(today) Reversal date and default Journal, then click the primary
'Reverse' button.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    # Navigate to the Misc Journal Items report (same place the menu
    # Accounting > Accounting > Miscellaneous points to).
    navigate(page, "/odoo/action-account.action_account_moves_journal_misc")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # The list is grouped by move. Find the group-header row whose text
    # includes BENCH-GL-REV and click the entry label link that navigates
    # to the account.move form.
    # Expand the group first so child rows are visible.
    group_rows = page.locator(
        ".o_list_view .o_group_header:has-text('BENCH-GL-REV'), "
        ".o_list_view tr.o_group_header:has-text('BENCH-GL-REV')"
    )
    if group_rows.count() > 0:
        group_rows.first.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Open the account.move form by clicking the group-header link to the
    # move. In Odoo 19 the grouped-by-move header contains an anchor on
    # the move name; clicking it navigates to the form. Fall back: click
    # any child data row to reach the move.line form then breadcrumb up
    # — but a simpler deterministic path is to use the move's internal
    # button that opens the form. We look for an element named
    # 'move_name' anchor inside the expanded group.
    move_link = page.locator(
        ".o_list_view .o_group_header:has-text('BENCH-GL-REV') "
        "button, "
        ".o_list_view .o_group_header:has-text('BENCH-GL-REV') a"
    )
    clicked = False
    if move_link.count() > 0:
        for i in range(move_link.count()):
            el = move_link.nth(i)
            try:
                text = el.inner_text().strip()
            except Exception:
                continue
            if "BENCH-GL-REV" in text or el.get_attribute("name") == "action_open_business_doc":
                try:
                    el.click()
                    clicked = True
                    break
                except Exception:
                    continue

    if not clicked:
        # Fallback: click any child row under the expanded group, then
        # click the breadcrumb/move name link to the move form.
        child_row = page.locator(
            ".o_list_view .o_data_row:has-text('BENCH-GL-REV')"
        )
        if child_row.count() > 0:
            child_row.first.click()
            page.wait_for_timeout(1200)
            _wait_no_loading(page)

    # Another robust fallback: resolve via JSON-RPC to get the move id
    # and navigate directly to the account.move form. This keeps the
    # oracle deterministic regardless of the grouped-list anchor shape.
    if "account.move/" not in (page.url or "") and "model=account.move" not in (page.url or ""):
        # Use Odoo's web client to open the move form via action URL.
        move_id = page.evaluate(
            """
            () => fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'account.move',
                        method: 'search_read',
                        args: [[['ref', '=', 'BENCH-GL-REV']], ['id']],
                        kwargs: {limit: 1},
                    },
                }),
            }).then(r => r.json()).then(j => (j.result && j.result[0] && j.result[0].id) || 0)
            """
        )
        if move_id:
            page.goto(page.url.split("#")[0] + f"odoo/action-account.action_move_journal_line/{move_id}")
            page.wait_for_timeout(500)
            # Simpler: use the canonical form-view URL.
            page.goto(f"{page.url.split('/odoo')[0]}/odoo/action-account.action_move_journal_line/{move_id}")
            page.wait_for_load_state("load")
            _wait_for_ready(page)

    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click 'Reverse Entry' header statusbar button (visible on posted
    # move_type='entry' records).
    reverse_btn = page.locator(
        ".o_statusbar_buttons button:has-text('Reverse Entry'):visible"
    )
    if reverse_btn.count() == 0:
        # Occasionally a hotkey-less variant hides the exact text; try
        # loose match on button with the reversal action name.
        reverse_btn = page.locator(
            ".o_statusbar_buttons button[name*='account_move_reversal']:visible"
        )
    reverse_btn.first.click(force=True)
    page.wait_for_selector(".modal:visible", timeout=10000)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Leave defaults (journal=misc, date=today). Click primary 'Reverse'.
    modal = page.locator(".modal:visible").last
    btn = modal.locator(
        "button.btn-primary[name='refund_moves']"
    ).first
    if btn.count() == 0:
        # Fallback: exact-text match to avoid picking Discard.
        buttons = modal.locator("footer button")
        for i in range(buttons.count()):
            b = buttons.nth(i)
            if b.inner_text().strip() == "Reverse":
                btn = b
                break
    btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
