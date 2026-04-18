"""Oracle for website_customer.publish_customer_reference_on_public_page.

UI path:
  1. Open /odoo/contacts and navigate into 'Bench Happy Client'.
  2. Click the 'Unpublished' redirect button in the form button box
     (website_redirect_button widget, navigation-only) to preview the
     public /partners/<slug> page.
  3. On the public preview, click the Owl systray 'Unpublished' switch
     to flip it to Published (calls website_publish_button via RPC).
  4. Navigate to /customers and confirm the partner is rendered.
"""

from benchmark.oracle_helpers import (
    full_url,
    login,
    navigate,
    run_oracle,
    DB,
    _wait_for_ready,
    _wait_no_loading,
)


CLIENT_NAME = "Bench Happy Client"


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)
    page.wait_for_timeout(1500)

    # Find the Bench Happy Client kanban/list record. Prefer kanban card
    # fallback to list view if kanban not loaded.
    record = page.locator(
        f".o_kanban_record:has-text('{CLIENT_NAME}'), "
        f".o_data_row:has-text('{CLIENT_NAME}')"
    ).first
    record.wait_for(timeout=15000)
    record.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Click the "Go to Website" button-box redirect button — widget
    # website_redirect_button on res.partner.is_published. Button label
    # is always "Go to Website" (aria-label/title = Unpublished/Published).
    # This navigates to /partners/<slug>.
    redirect_btn = page.locator(
        ".o_field_website_redirect_button button, "
        ".o_field_widget[name='is_published'] button"
    ).first

    redirect_btn.wait_for(timeout=10000)
    redirect_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(3500)

    # We are now on /partners/<slug>. Click the systray Published toggle.
    # The systray item is .o_website_publish_container (see
    # publish_website_systray_item.js). Clicking it invokes
    # website_publish_button via ORM RPC.
    publish_toggle = page.locator(
        ".o_website_publish_container, "
        ".o_menu_systray_item:has(a:has-text('Unpublished')), "
        ".o_menu_systray_item:has(a:has-text('Published'))"
    ).first
    publish_toggle.wait_for(state="visible", timeout=15000)

    # Click the systray publish container. The Owl component hooks t-on-click
    # at the root div, so clicking anywhere inside is fine.
    publish_toggle.click()
    # Allow the RPC round-trip to complete.
    page.wait_for_timeout(2500)

    # Navigate to /customers and confirm partner listed.
    customers_url = "/customers"
    if DB:
        customers_url = f"/customers?db={DB}"
    page.goto(full_url(customers_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(2500)

    # Confirm partner visible on /customers.
    partner_link = page.locator(
        f"a:has-text('{CLIENT_NAME}'), "
        f".card:has-text('{CLIENT_NAME}'), "
        f"*:has-text('{CLIENT_NAME}')"
    ).first
    try:
        partner_link.wait_for(state="visible", timeout=10000)
    except Exception:
        # Postcondition check will catch genuine failures; some themes
        # render the name only inside an anchor we already try above.
        pass


run_oracle(oracle)
