"""Oracle for website_sale.unpublish_archive_unarchive_publish_cycle.

Walks the seeded product through:
    Unpublish -> Archive -> (toggle Archived filter) -> Unarchive ->
    Publish -> set Internal Reference (BCG-RESTORED).
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_list_row,
    click_tab,
    ensure_list_view,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


PRODUCT_NAME = "Bench Cycle Gadget"
NEW_CODE = "BCG-RESTORED"


def _toggle_publish(page, *, want_published: bool):
    """Toggle the website publish switch in the product form.

    The publish toggle (`is_published`, widget="boolean_toggle") lives on
    the **Sales** notebook tab in the eCommerce Shop group, so make sure
    the tab is open before grabbing it.
    """
    try:
        click_tab(page, "Sales")
    except Exception:
        pass
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    toggle = page.locator(
        ".o_field_widget[name='is_published'] input[type='checkbox']"
    ).last
    toggle.wait_for(state="attached", timeout=10000)
    if toggle.is_checked() != want_published:
        toggle.click(force=True)
        page.wait_for_timeout(800)
        _wait_no_loading(page)


def _click_cog(page):
    cog = page.locator(
        ".o_cp_action_menus button.dropdown-toggle:visible, "
        ".o_cp_action_menus button:visible"
    ).first
    cog.wait_for(state="visible", timeout=10000)
    cog.click()
    page.wait_for_timeout(600)


def _click_menu_item(page, label: str):
    selector = (
        f".o-dropdown--menu:visible .dropdown-item:has-text('{label}'), "
        f".dropdown-menu:visible .dropdown-item:has-text('{label}')"
    )
    page.wait_for_selector(selector, state="visible", timeout=10000)
    page.locator(selector).first.click()
    page.wait_for_timeout(800)


def _confirm_modal_if_present(page):
    modal = page.locator(".modal:visible")
    if modal.count() > 0:
        btn = modal.last.locator(
            "button:has-text('Archive'), "
            "button:has-text('Unarchive'), "
            "button:has-text('OK'), "
            "button:has-text('Confirm')"
        ).first
        if btn.count() > 0:
            btn.click()
            page.wait_for_timeout(800)


def _action_menu(page, label: str):
    _click_cog(page)
    _click_menu_item(page, label)
    _confirm_modal_if_present(page)
    _wait_no_loading(page)


def _toggle_archived_filter(page):
    toggler = page.locator(".o_searchview_dropdown_toggler:visible").first
    toggler.click()
    page.wait_for_timeout(500)
    archived = page.locator(
        ".o_search_bar_menu .o_filter_menu .o_menu_item:has-text('Archived'), "
        ".o-dropdown--menu:visible .o_menu_item:has-text('Archived')"
    ).first
    archived.click()
    page.wait_for_timeout(500)
    page.keyboard.press("Escape")
    _wait_no_loading(page)


def _back_to_products(page):
    navigate(page, "/odoo/ecommerce-products")
    _wait_no_loading(page)
    page.wait_for_timeout(800)
    # Default view is kanban; switch to list so click_list_row works.
    ensure_list_view(page)
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _open_product(page):
    """Open the seeded product. The default view applies a 'Published' filter
    that hides archived/unpublished records, so clear filters first."""
    clear_search_filters(page)
    page.wait_for_timeout(400)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, PRODUCT_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(800)


def oracle(page):
    login(page)
    _back_to_products(page)

    # --- Step 1: Open product, Unpublish, save ---
    _open_product(page)
    _toggle_publish(page, want_published=False)
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # --- Step 2: Archive via Actions menu ---
    _action_menu(page, "Archive")
    page.wait_for_timeout(800)

    # --- Step 3: Go back to list, clear Published filter, enable
    # Archived filter, reopen, Unarchive. ---
    _back_to_products(page)
    clear_search_filters(page)
    page.wait_for_timeout(400)
    _toggle_archived_filter(page)
    page.wait_for_timeout(800)
    ensure_list_view(page)
    page.wait_for_timeout(400)
    click_list_row(page, PRODUCT_NAME)
    _wait_for_ready(page)
    page.wait_for_timeout(800)
    _action_menu(page, "Unarchive")
    page.wait_for_timeout(800)

    # --- Step 4: Publish back ---
    _toggle_publish(page, want_published=True)
    page.wait_for_timeout(500)

    # --- Step 5: Set Internal Reference and save. The field lives in the
    # General Information tab (typically the default open tab); switch to
    # it first since the previous step left us on the Sales tab. ---
    try:
        click_tab(page, "General Information")
    except Exception:
        pass
    page.wait_for_timeout(400)
    _wait_no_loading(page)
    fill_field(page, "default_code", NEW_CODE)
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)


run_oracle(oracle)
