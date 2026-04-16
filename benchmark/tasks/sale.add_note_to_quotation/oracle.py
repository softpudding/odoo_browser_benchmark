"""Oracle for sale.add_note_to_quotation."""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
)

EXPECTED_NOTE = "Customer requested delivery by May 1, 2026. Please coordinate with warehouse."


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    click_list_row(page, "Azure Interior")
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    page.locator(".o-mail-Chatter, .o_chatter").first.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    page.get_by_role("button", name="Log note").click()
    page.wait_for_timeout(800)

    editor = page.locator("div[contenteditable='true']:visible").last
    editor.click()
    page.wait_for_timeout(300)
    editor.evaluate("(el, text) => { el.textContent = text; el.dispatchEvent(new Event('input', { bubbles: true })); }", EXPECTED_NOTE)
    page.wait_for_timeout(1000)

    log_btn = page.locator("button.o-mail-Composer-send:has-text('Log'):visible")
    log_btn.wait_for(state="visible", timeout=5000)
    log_btn.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
