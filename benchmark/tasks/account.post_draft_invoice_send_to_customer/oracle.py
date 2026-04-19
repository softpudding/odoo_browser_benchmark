"""Oracle for account.post_draft_invoice_send_to_customer.

Open the draft invoice BENCH-POST-SEND-001 (customer Bench Post Co),
click Confirm to post, then click Send in the header to open the
account.move.send.wizard, and finally click the primary Send button in
the wizard footer (NOT Discard).
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    # The Customers > Invoices list is filtered by default to posted
    # invoices in some configurations; expand the filter to include
    # drafts so BENCH-POST-SEND-001 is visible.
    # Strategy: just use the search bar to find the ref directly.
    from benchmark.oracle_helpers import search_for, clear_search_filters

    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(300)
    try:
        search_for(page, "BENCH-POST-SEND-001")
    except Exception:
        pass
    page.wait_for_timeout(600)

    click_list_row(page, "BENCH-POST-SEND-001")
    page.wait_for_timeout(1200)
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Click Confirm in the statusbar to post the draft.
    click_status_button(page, "Confirm")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click Send in the header to open the send wizard.
    click_status_button(page, "Send")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # It's possible that the base_document_layout configurator opens
    # first. The seed pre-sets external_report_layout_id on the company
    # so this should NOT happen, but handle defensively: if a dialog
    # with "Configure Document Layout" appears, click Save/Confirm.
    modal = page.locator(".modal:visible").last
    modal_title = ""
    try:
        modal_title = modal.locator(
            ".modal-title, .o_dialog .modal-header"
        ).first.inner_text(timeout=1000)
    except Exception:
        modal_title = ""

    if "Document Layout" in modal_title or "Configure" in modal_title:
        # Click Save button to dismiss the layout configurator.
        save_btn = modal.locator(
            "button.btn-primary:has-text('Save'), "
            "button:has-text('Continue')"
        )
        if save_btn.count() > 0:
            save_btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
        modal = page.locator(".modal:visible").last

    # Now the account.move.send.wizard dialog should be open. Click the
    # primary Send button in the footer. The footer has:
    #   <button name="action_send_and_print" class="btn-primary">Send</button>
    # and a "Discard" secondary button.
    send_btn = modal.locator(
        "footer button.btn-primary[name='action_send_and_print'], "
        ".modal-footer button.btn-primary[name='action_send_and_print']"
    )
    if send_btn.count() == 0:
        # Fallback: loose match on footer primary button named Send
        footer = modal.locator("footer, .modal-footer").first
        buttons = footer.locator("button.btn-primary")
        picked = None
        for i in range(buttons.count()):
            b = buttons.nth(i)
            try:
                t = b.inner_text().strip()
            except Exception:
                continue
            if t in ("Send", "Generate"):
                picked = b
                break
        if picked is None:
            # Very loose fallback: any primary button in the footer.
            if buttons.count() > 0:
                picked = buttons.first
        if picked is None:
            raise AssertionError("Could not locate primary Send button in send wizard")
        send_btn = picked
    else:
        send_btn = send_btn.first

    send_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)


run_oracle(oracle)
