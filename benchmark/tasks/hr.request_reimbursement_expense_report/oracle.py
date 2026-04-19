"""Oracle for hr.request_reimbursement_expense_report.

Drives the full Odoo 19 reimbursement lifecycle:

  Draft → (Submit) → Submitted → (Approve) → Approved →
          (Post Journal Entries → wizard: Post Expenses) → Posted

The hr.expense.sheet model was removed in v19, so there's no "Submit to Manager"
on a sheet — everything happens on the single hr.expense form. The statusbar
exposes three distinct buttons in sequence: Submit, Approve, Post Journal Entries.
The final step opens a `hr.expense.post.wizard` modal whose primary button
"Post Expenses" (name=action_post_entry) creates + posts the account.move.
"""

from benchmark.oracle_helpers import (
    _wait_no_loading,
    _wait_for_ready,
    click_list_row,
    login,
    navigate,
    run_oracle,
)


EXPENSE_NAME = "Bench Travel Expense"


def _click_statusbar_button(page, name, label):
    """Click a statusbar button by `name` attribute, with a visible-text fallback.

    Returns True if a click was dispatched.
    """
    # Prefer the name attribute — unambiguous across languages/versions.
    btn = page.locator(
        f".o_statusbar_buttons button[name='{name}']:visible"
    )
    if btn.count() > 0:
        try:
            btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            return True
        except Exception:
            pass

    # Fallback: match by label.
    btn = page.locator(
        f".o_statusbar_buttons button:visible:has-text('{label}')"
    )
    if btn.count() > 0:
        try:
            btn.first.click()
            page.wait_for_timeout(1500)
            _wait_no_loading(page)
            return True
        except Exception:
            pass
    return False


def _confirm_post_wizard(page):
    """Click the 'Post Expenses' button in the hr.expense.post.wizard modal."""
    # Wait for the modal to appear.
    try:
        page.wait_for_selector(".modal.o_dialog:visible, .o_dialog:visible", timeout=10000)
    except Exception:
        pass
    page.wait_for_timeout(500)

    # The wizard footer button: name=action_post_entry, label "Post Expenses".
    candidates = [
        ".o_dialog:visible button[name='action_post_entry']",
        ".modal:visible button[name='action_post_entry']",
        ".o_dialog:visible footer button.oe_highlight",
        ".o_dialog:visible footer button.btn-primary",
        ".modal:visible .modal-footer button.btn-primary",
    ]
    for sel in candidates:
        btn = page.locator(sel)
        if btn.count() > 0:
            try:
                btn.first.click()
                page.wait_for_timeout(2000)
                _wait_no_loading(page)
                return True
            except Exception:
                continue

    # Last resort: click a button whose visible text is "Post Expenses".
    btn = page.locator(".o_dialog:visible button:has-text('Post Expenses')")
    if btn.count() > 0:
        try:
            btn.first.click()
            page.wait_for_timeout(2000)
            _wait_no_loading(page)
            return True
        except Exception:
            pass
    return False


def oracle(page):
    login(page)
    navigate(page, "/odoo/expenses")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the seeded Bench Travel Expense from My Expenses (list or kanban).
    click_list_row(page, EXPENSE_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Step 1: Submit. draft → submitted.
    _click_statusbar_button(page, "action_submit", "Submit")
    page.wait_for_timeout(1000)

    # Step 2: Approve. submitted → approved.
    _click_statusbar_button(page, "action_approve", "Approve")
    page.wait_for_timeout(1000)

    # Step 3: Post Journal Entries. opens the post wizard modal.
    _click_statusbar_button(
        page, "action_post", "Post Journal Entries",
    )
    page.wait_for_timeout(1200)

    # Step 3b: In the wizard, click "Post Expenses" (accept default journal +
    # accounting date).
    _confirm_post_wizard(page)
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
