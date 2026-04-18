"""Oracle for purchase.send_rfq_email_with_template_signature.

Steps:
  1. Open Purchase app, click target RFQ R-BENCH-EMAIL-001.
  2. Click 'Send RFQ' header button.
  3. In compose wizard, open the template selector dropdown
     (`.mail-composer-template-dropdown-btn`) and pick
     'Purchase: Purchase Order' to replace the default 'Purchase: Request
     For Quotation'.
  4. Wait for the body to re-render with the new template, then append
     'Please confirm by Friday.' at the very end.
  5. Click primary Send in the wizard footer.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_status_button,
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
)


APPEND_TEXT = "Please confirm by Friday."
TARGET_TEMPLATE = "Purchase: Purchase Order"


def _find_body(modal):
    body_selectors = [
        ".o_field_widget[name='body'] .odoo-editor-editable",
        ".o_field_widget[name='body'] [contenteditable='true']",
        ".o_field_html .odoo-editor-editable",
        "[contenteditable='true']",
        "div.note-editable",
    ]
    for sel in body_selectors:
        loc = modal.locator(sel).first
        try:
            loc.wait_for(state="visible", timeout=3_000)
            return loc
        except Exception:
            continue
    # Last-ditch fallback.
    loc = modal.locator("[contenteditable='true']").first
    loc.wait_for(state="visible", timeout=10_000)
    return loc


def oracle(page):
    login(page)
    navigate(page, "/odoo/purchase")
    _wait_no_loading(page)

    # Open the target RFQ.
    click_list_row(page, "R-BENCH-EMAIL-001")
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # Click 'Send RFQ' in the form header.
    try:
        click_status_button(page, "Send RFQ")
    except Exception:
        header_btn = page.locator(
            "button[name='action_rfq_send']:visible:has-text('Send RFQ')"
        ).first
        header_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    modal = page.locator(".modal:visible").last
    modal.wait_for(state="visible", timeout=15_000)

    # --- Switch template to 'Purchase: Purchase Order' ---------------------
    template_btn = modal.locator(
        ".mail-composer-template-dropdown-btn"
    ).first
    template_btn.wait_for(state="visible", timeout=10_000)
    template_btn.click()
    page.wait_for_timeout(500)
    # Dropdown items land at page level (Owl portals them out of the modal).
    item = page.locator(
        f".mail-composer-template-dropdown .dropdown-item:has-text('{TARGET_TEMPLATE}')"
    ).first
    if item.count() == 0:
        item = page.locator(
            f".dropdown-menu:visible .dropdown-item:has-text('{TARGET_TEMPLATE}')"
        ).first
    item.wait_for(state="visible", timeout=5_000)
    item.click()
    # Wait for onLoadTemplate → onchange → body re-render to complete.
    page.wait_for_timeout(2000)
    _wait_no_loading(page)

    # --- Locate the body AFTER template switch (element may be re-mounted) -
    body = _find_body(modal)

    # Focus via JS and place caret at the very end.
    body.evaluate(
        """el => {
            el.focus();
            const range = document.createRange();
            range.selectNodeContents(el);
            range.collapse(false);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        }"""
    )
    page.wait_for_timeout(200)

    page.keyboard.press("Enter")
    page.keyboard.press("Enter")
    page.keyboard.insert_text(APPEND_TEXT)
    page.wait_for_timeout(500)

    # --- Click primary Send (enabled variant). -----------------------------
    candidates = [
        "button.o_mail_send:not([disabled]):visible",
        "button.btn-primary.o_mail_send:not([disabled]):visible",
    ]
    send_btn = None
    for sel in candidates:
        loc = modal.locator(sel).first
        if loc.count() > 0:
            send_btn = loc
            break
    if send_btn is None:
        raise AssertionError(
            "Could not locate enabled Send button in the compose wizard"
        )
    send_btn.click()
    page.wait_for_timeout(3000)
    _wait_no_loading(page)


run_oracle(oracle)
