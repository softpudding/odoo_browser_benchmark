"""Oracle for sale.revise_target_quote_lines.

Find quotation with customer reference OPS-042 (Aurora Interiors).
Update order lines:
  - Standing Desk: description "Ergonomic standing desk bundle", discount 5%
  - Office Chair: description "Mesh chair support package", discount 10%
  - Whiteboard: description "Magnetic planning board", discount 0%
Set Payment Terms to "15 Days" in Other Info tab. Save.
"""

from benchmark.oracle_helpers import (
    click_list_row,
    click_tab,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    set_o2m_field,
    _wait_no_loading,
    _wait_for_ready,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)

    # Find and open the quotation with ref OPS-042
    click_list_row(page, "OPS-042")
    page.wait_for_timeout(1000)

    # Update Standing Desk line (row 0): description and discount
    # The 'name' field is the description. Click the cell to edit inline.
    row0 = page.locator(".o_list_view .o_data_row").nth(0)
    name_cell0 = row0.locator("td[name='name'], .o_field_widget[name='name']").first
    name_cell0.click()
    page.wait_for_timeout(300)
    inp0 = name_cell0.locator("textarea, input").first
    inp0.fill("Standing Desk\nErgonomic standing desk bundle")
    inp0.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    set_o2m_field(page, 0, "discount", "5")
    page.wait_for_timeout(500)

    # Update Office Chair line (row 1): description and discount
    row1 = page.locator(".o_list_view .o_data_row").nth(1)
    name_cell1 = row1.locator("td[name='name'], .o_field_widget[name='name']").first
    name_cell1.click()
    page.wait_for_timeout(300)
    inp1 = name_cell1.locator("textarea, input").first
    inp1.fill("Office Chair\nMesh chair support package")
    inp1.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    set_o2m_field(page, 1, "discount", "10")
    page.wait_for_timeout(500)

    # Update Whiteboard line (row 2): description only (discount stays 0)
    row2 = page.locator(".o_list_view .o_data_row").nth(2)
    name_cell2 = row2.locator("td[name='name'], .o_field_widget[name='name']").first
    name_cell2.click()
    page.wait_for_timeout(300)
    inp2 = name_cell2.locator("textarea, input").first
    inp2.fill("Whiteboard\nMagnetic planning board")
    inp2.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    # Set Payment Terms to "15 Days" in Other Info tab
    click_tab(page, "Other Info")
    page.wait_for_timeout(500)

    set_many2one(page, "payment_term_id", "15 Days")
    page.wait_for_timeout(500)

    # Save (don't confirm)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
