"""Oracle for mrp.convert_bom_to_kit_type.

Navigate to Bills of Materials, open the seeded BOM, change its type
from Manufacture this Product (normal) to Kit (phantom), save.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/boms")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open BOM for Benchmark Modular Shelving
    row = page.locator(
        ".o_data_row:has-text('Benchmark Modular Shelving')"
    ).first
    row.click()
    _wait_for_ready(page)
    page.wait_for_timeout(1000)

    # Change BOM Type field to Kit. Odoo 19 renders `type` as a radio group.
    # The label reads "Kit" for the phantom option.
    type_field = page.locator("div[name='type']").first
    kit_option = type_field.locator("label:has-text('Kit')").first
    if kit_option.count() == 0:
        # Fallback: input value='phantom'
        kit_option = type_field.locator("input[value='phantom']").first
    kit_option.click()
    page.wait_for_timeout(500)

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
