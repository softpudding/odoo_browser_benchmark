"""Oracle for account.create_recurring_entry_template.

Opens the existing draft journal entry with ref='Bench Office Supplies Tmpl',
switches to the Other Info tab, changes Auto-post from 'No' to 'Monthly',
sets Auto-post until to 08/01/2026, and saves the form.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def _set_auto_post_monthly(page):
    """Odoo 19 renders selection fields with o_select_menu custom widget
    rather than <select>. Click the toggler and pick the Monthly item.
    Falls back to native select for compatibility with other renderers.
    """
    widget = page.locator(".o_field_widget[name='auto_post']").first
    widget.scroll_into_view_if_needed()

    # Try native select first (some flows still render it)
    native = widget.locator("select")
    if native.count() > 0:
        native.select_option(label="Monthly")
        page.wait_for_timeout(500)
        return

    # o_select_menu custom dropdown
    toggler = widget.locator(
        ".o_select_menu_toggler, .o_select_menu, button.o_select_menu_toggler"
    )
    toggler.first.click()
    page.wait_for_timeout(500)
    item = page.locator(
        ".o_select_menu_menu .o_select_menu_item:has-text('Monthly'), "
        ".dropdown-menu .dropdown-item:has-text('Monthly')"
    )
    item.first.click()
    page.wait_for_timeout(500)


def _set_auto_post_until(page, date_str):
    """Fill the Auto-post until date that appears after choosing Monthly.

    In Odoo 19 a date field with no initial value renders as an empty input
    inside the widget. We use Playwright to clear + type + Tab.
    """
    widget = page.locator(".o_field_widget[name='auto_post_until']").first
    widget.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    inp = widget.locator("input:visible").first
    if inp.count() == 0:
        # Date fields without a value can render as a button/span placeholder.
        control = widget.locator("button, span, input").first
        control.click()
        page.wait_for_timeout(400)
        inp = widget.locator("input:visible").first
        if inp.count() == 0:
            inp = page.locator(
                ".o_datetime_picker:visible input, "
                ".o_datetime_picker_container:visible input"
            ).first

    inp.click(click_count=3)
    inp.press("Delete")
    inp.type(date_str, delay=40)
    page.wait_for_timeout(300)
    inp.press("Escape")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/accounting/entries")
    _wait_no_loading(page)

    ensure_list_view(page)
    click_list_row(page, "Bench Office Supplies Tmpl")
    _wait_for_ready(page)

    click_tab(page, "Other Info")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # Set Auto-post = Monthly. The field uses Odoo's o_select_menu widget.
    _set_auto_post_monthly(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # The auto_post_until field is conditionally rendered once auto_post != 'no'.
    _set_auto_post_until(page, "08/01/2026")

    save_form(page)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)


run_oracle(oracle)
