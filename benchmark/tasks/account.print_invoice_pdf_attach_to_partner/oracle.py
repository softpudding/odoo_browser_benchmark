"""Oracle for account.print_invoice_pdf_attach_to_partner.

Open the POSTED invoice BENCH-PRINT-001 (customer Bench Print Co),
click Send in the header to open the Send & Print wizard, and click
the primary Send button in the wizard footer. The wizard's
`_send_mails` path then posts a `mail.message` on the invoice with
the pre-seeded invoice PDF attached (filename ending `.pdf`,
mimetype `application/pdf`).

The seed pre-fills `invoice_pdf_report_file` on the invoice so the
wkhtmltopdf render path is skipped (see row 446 COOKBOOK_NOTES).
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    search_for,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/customer-invoices")
    _wait_no_loading(page)

    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(300)
    try:
        search_for(page, "BENCH-PRINT-001")
    except Exception:
        pass
    page.wait_for_timeout(700)

    click_list_row(page, "BENCH-PRINT-001")
    page.wait_for_timeout(1200)
    _wait_for_ready(page)
    _wait_no_loading(page)

    # Click Send in the header (action_invoice_sent -> opens wizard).
    click_status_button(page, "Send")
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # Defensive: dismiss the base_document_layout configurator if it
    # appears (seed pre-sets external_report_layout_id to avoid this).
    modal = page.locator(".modal:visible").last
    try:
        modal_title = modal.locator(
            ".modal-title, .o_dialog .modal-header"
        ).first.inner_text(timeout=1000)
    except Exception:
        modal_title = ""

    if "Document Layout" in modal_title or "Configure" in modal_title:
        save_btn = modal.locator(
            "button.btn-primary:has-text('Save'), "
            "button:has-text('Continue')"
        )
        if save_btn.count() > 0:
            save_btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
        modal = page.locator(".modal:visible").last

    # Click the primary Send button in the wizard footer
    # (name=action_send_and_print).
    send_btn = modal.locator(
        "footer button.btn-primary[name='action_send_and_print'], "
        ".modal-footer button.btn-primary[name='action_send_and_print']"
    )
    if send_btn.count() == 0:
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
        if picked is None and buttons.count() > 0:
            picked = buttons.first
        if picked is None:
            raise AssertionError(
                "Could not locate primary Send button in send wizard"
            )
        send_btn = picked
    else:
        send_btn = send_btn.first

    send_btn.click()
    page.wait_for_timeout(2800)
    _wait_no_loading(page)


run_oracle(oracle)
