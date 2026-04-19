"""Oracle for sale.create_sale_quotation_from_opportunity_smart_button.

Open the CRM opportunity 'Bench Opp Sale', click the Quotations smart
button (button name='action_view_sale_quotation', statinfo field
'quotation_count'), click New on the empty quotation list, add one line
of Bench Opp Product qty=2, Save (do NOT confirm).
"""

from benchmark.oracle_helpers import (
    clear_search_filters,
    click_add_a_line,
    click_create,
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    save_form,
    set_o2m_field,
    set_o2m_many2one,
    _wait_no_loading,
    _wait_for_ready,
)


TARGET = "Bench Opp Sale"
PRODUCT = "Bench Opp Product"


def oracle(page):
    login(page)
    navigate(page, "/odoo/crm")
    _wait_no_loading(page)
    page.wait_for_timeout(1200)

    try:
        clear_search_filters(page)
    except Exception:
        pass
    page.wait_for_timeout(400)
    _wait_no_loading(page)

    # 1. Open the opportunity
    click_kanban_card(page, TARGET)
    page.wait_for_timeout(1000)
    _wait_for_ready(page)
    page.locator(".o_form_view").first.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(400)

    # 2. Click the Quotations smart button. The button has
    #    name='action_view_sale_quotation' and contains a statinfo field
    #    rendering 'quotation_count'. Match by name attribute for robustness.
    smart_btn = page.locator(
        "button[name='action_view_sale_quotation']:visible"
    ).first
    smart_btn.wait_for(state="visible", timeout=15000)
    smart_btn.click()
    page.wait_for_timeout(1200)
    _wait_no_loading(page)
    _wait_for_ready(page)

    # 3. Click New on the (empty) filtered quotation list
    click_create(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # Wait for sale.order form to be ready
    page.locator(
        ".o_form_view .o_field_widget[name='partner_id'], "
        ".o_form_view .o_field_widget[name='order_line']"
    ).first.wait_for(state="visible", timeout=15000)
    page.wait_for_timeout(400)

    # 4. Add order line: Bench Opp Product qty=2
    click_add_a_line(page)
    page.wait_for_timeout(600)

    # sol o2m list uses product_template_id (as in sale.create_quotation_with_customer_pricelist)
    set_o2m_many2one(page, 0, "product_template_id", PRODUCT)
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    set_o2m_field(page, 0, "product_uom_qty", "2")
    page.wait_for_timeout(600)
    _wait_no_loading(page)

    # 5. Save (NOT confirm). Press Escape first to close any open popover.
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(900)
    _wait_no_loading(page)


run_oracle(oracle)
