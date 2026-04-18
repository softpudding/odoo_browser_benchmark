"""Oracle for lunch.create_vendor_product_order_for_today.

Flow:
1. /odoo/lunch-vendors-menu (lunch_vendors_action) -> New vendor form
   -> Name, pick partner, phone, set delivery=Delivery -> Save.
2. /odoo/lunch-product-menu (lunch_product_action) -> New product form
   -> Name, category=Sandwich, vendor=Bench Cafe, price=8 -> Save.
3. /odoo/lunch (lunch_product_action_order) -> click Veggie Wrap kanban
   card -> modal form opens -> fill Notes, click Add To Cart.
4. Back on dashboard, click the Order Now sidebar button.
"""

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    click_create,
    fill_field,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_selection,
)


VENDOR_NAME = "Bench Cafe"
PARTNER_NAME = "Bench Cafe Partner"
PRODUCT_NAME = "Veggie Wrap"


def _menu_url(page, menu_xml_id):
    """Navigate to an action-of-a-menu URL if possible."""
    navigate(page, menu_xml_id)


def oracle(page):
    login(page)

    # ---- Step 1: Create the vendor ----
    # The Lunch app's config submenu for Vendors.
    navigate(page, "/odoo/action-lunch.lunch_vendors_action")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    # Pick the partner first from autocomplete. The `name` field is
    # related to partner_id.name, so picking an existing partner
    # clobbers whatever we typed into name beforehand.
    set_many2one(page, "partner_id", PARTNER_NAME)
    page.wait_for_timeout(600)

    # NOW fill the vendor name (this also writes back to partner.name
    # because the related field is readonly=False).
    fill_field(page, "name", VENDOR_NAME)
    page.wait_for_timeout(400)

    # Phone (required when send_by=phone, which is the default).
    phone_inp = page.locator(".o_field_widget[name='phone'] input").first
    phone_inp.click()
    phone_inp.fill("")
    phone_inp.fill("+1 555 0199")
    phone_inp.press("Tab")
    page.wait_for_timeout(300)

    # Delivery: Odoo 19 Selection fields use the custom SelectMenu
    # widget, NOT a native <select>. Click the menu toggler then pick
    # the "Delivery" option from the visible dropdown.
    delivery_widget = page.locator(".o_field_widget[name='delivery']").first
    delivery_widget.locator(".o_select_menu_toggler, button, .o_select_menu").first.click()
    page.wait_for_timeout(500)
    page.locator(
        ".o_select_menu_menu .o_select_menu_item:has-text('Delivery'), "
        ".dropdown-menu.show .dropdown-item:has-text('Delivery'), "
        ".o_select_menu_menu div:has-text('Delivery'):not(:has-text('No Delivery'))"
    ).first.click()
    page.wait_for_timeout(500)

    # Enable Sat/Sun on the week-days widget (default Mon-Fri only).
    # The web.WeekDays widget renders a 2-row table: row 1 is the day
    # label headers, row 2 is the checkboxes. Locate each header cell
    # by its tooltip text and toggle the same-column checkbox.
    for day_label in ("Sat", "Sun"):
        table = page.locator(".o_recurrent_weekdays table").first
        headers = table.locator("th")
        n = headers.count()
        col_idx = None
        for i in range(n):
            if day_label in (headers.nth(i).inner_text().strip()):
                col_idx = i
                break
        if col_idx is None:
            # fallback: match via tooltip attribute
            for i in range(n):
                tip = headers.nth(i).locator("[data-tooltip]").get_attribute("data-tooltip") or ""
                if day_label in tip:
                    col_idx = i
                    break
        if col_idx is None:
            continue
        cb = table.locator("tr").nth(1).locator("td").nth(col_idx).locator("input[type='checkbox']")
        if cb.count() > 0 and not cb.first.is_checked():
            cb.first.click()
            page.wait_for_timeout(250)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # ---- Step 2: Create the product ----
    navigate(page, "/odoo/action-lunch.lunch_product_action")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    click_create(page)
    page.wait_for_timeout(800)
    _wait_for_ready(page)

    fill_field(page, "name", PRODUCT_NAME)
    page.wait_for_timeout(400)
    set_many2one(page, "category_id", "Sandwich")
    page.wait_for_timeout(400)
    set_many2one(page, "supplier_id", VENDOR_NAME)
    page.wait_for_timeout(400)

    price_inp = page.locator(".o_field_widget[name='price'] input").first
    price_inp.click()
    price_inp.fill("")
    price_inp.fill("8.00")
    price_inp.press("Tab")
    page.wait_for_timeout(400)

    save_form(page)
    page.wait_for_timeout(1200)
    _wait_no_loading(page)

    # ---- Step 3: Order it via the kiosk dashboard ----
    navigate(page, "/odoo/lunch")
    _wait_no_loading(page)
    # Let the LunchDashboard's /lunch/infos RPC resolve and lunchState
    # locationId populate so the kanban renders records.
    page.wait_for_timeout(2500)

    # Locate the Veggie Wrap kanban card and click the product name
    # text (avoids the favorite star in the corner).
    card = page.locator(
        f".o_kanban_view .o_kanban_record:has-text('{PRODUCT_NAME}')"
    ).first
    card.wait_for(state="visible", timeout=20000)
    card.scroll_into_view_if_needed()
    name_target = card.locator(
        f".fw-bolder:has-text('{PRODUCT_NAME}'), "
        f"span:has-text('{PRODUCT_NAME}'), "
        f"[name='name']"
    ).first
    name_target.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    # Wait for the order modal form to open. Use o_form_view inside a
    # visible dialog as a more specific signal than the generic .modal.
    page.wait_for_selector(
        ".o_dialog .o_form_view, .modal-dialog:visible .o_form_view",
        timeout=20000,
    )
    page.wait_for_timeout(800)

    modal = page.locator(".o_dialog:has(.o_form_view), .modal.show").last

    # Fill the Notes textarea inside the modal.
    note_field = modal.locator(
        ".o_field_widget[name='note'] textarea, "
        ".o_field_widget[name='note'] input"
    ).first
    note_field.wait_for(state="visible", timeout=10000)
    note_field.click()
    note_field.fill("no onions")
    note_field.press("Tab")
    page.wait_for_timeout(400)

    # Click "Add To Cart" in the modal footer (the form's <footer>).
    # Use page-wide locator because Playwright's .modal locator scope
    # sometimes doesn't include Owl-rendered footers.
    add_btn = page.locator(
        "button[name='add_to_cart']:visible, "
        "footer button:has-text('Add To Cart'):visible, "
        "button.oe_highlight:has-text('Add To Cart'):visible, "
        "button:has-text('Add To Cart'):visible"
    ).first
    add_btn.wait_for(state="visible", timeout=15000)
    add_btn.click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    # Dialog should close. Now click Order Now in the sidebar dashboard.
    order_now = page.locator(
        "button:has-text('Order Now'):visible"
    ).first
    order_now.wait_for(state="visible", timeout=20000)
    order_now.click()
    page.wait_for_timeout(2000)
    _wait_no_loading(page)


run_oracle(oracle)
