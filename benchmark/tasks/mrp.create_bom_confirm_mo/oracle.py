"""Oracle for mrp.create_bom_confirm_mo.

Create a BOM for "Bench Assembly Table" with 3 components,
then create and confirm a Manufacturing Order for 10 units.
"""

from benchmark.oracle_helpers import (
    click_add_a_line,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
)


COMPONENTS = [
    ("Table Leg", "4"),
    ("Table Top Panel", "1"),
    ("Assembly Screw Pack", "2"),
]


def oracle(page):
    login(page)

    # Step 1: Create a Bill of Materials
    navigate(page, "/odoo/boms")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    click_create(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Set product
    set_many2one(page, "product_tmpl_id", "Bench Assembly Table")
    page.wait_for_timeout(500)

    # Add component lines
    for comp_name, qty in COMPONENTS:
        click_add_a_line(page)
        page.wait_for_timeout(500)

        # Set the product (component) on the new line
        rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
        row_idx = rows.count() - 1  # Last row is the new one
        set_o2m_many2one(page, row_idx, "product_id", comp_name)
        page.wait_for_timeout(300)

        # Set quantity
        set_o2m_field(page, row_idx, "product_qty", qty)
        page.wait_for_timeout(300)

    # Save the BOM
    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Step 2: Create Manufacturing Order
    navigate(page, "/odoo/manufacturing")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    click_create(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Set product - BOM should auto-fill
    set_many2one(page, "product_id", "Bench Assembly Table")
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Set quantity to 10
    fill_field(page, "product_qty", "10")
    page.wait_for_timeout(500)

    # Save first to ensure MO is persisted
    save_form(page)
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Confirm the MO - button is in the statusbar
    confirm_btn = page.locator(
        ".o_statusbar_buttons button[name='action_confirm']:visible, "
        ".o_form_statusbar button[name='action_confirm']:visible"
    )
    if confirm_btn.count() > 0:
        confirm_btn.first.click()
    else:
        # Fallback: click Confirm in the button area
        page.locator(
            ".o_statusbar_buttons button:has-text('Confirm'):visible"
        ).first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
