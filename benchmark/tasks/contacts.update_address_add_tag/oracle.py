"""Oracle for contacts.update_address_add_tag.

Find company "Brookfield Dynamics", update address fields, add "Supplier"
tag, set job position to "Procurement Partner", and save.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_list_row,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/contacts")
    _wait_no_loading(page)

    # Find and open Brookfield Dynamics
    click_list_row(page, "Brookfield Dynamics")
    page.wait_for_timeout(500)

    # Update address fields
    fill_field(page, "street", "742 Innovation Blvd")
    page.wait_for_timeout(300)
    fill_field(page, "city", "Portland")
    page.wait_for_timeout(300)

    # Set state to Oregon
    set_many2one(page, "state_id", "Oregon")
    page.wait_for_timeout(300)

    fill_field(page, "zip", "97201")
    page.wait_for_timeout(300)

    # Country should already be US, but set it to be safe
    set_many2one(page, "country_id", "United States")
    page.wait_for_timeout(300)

    # Add "Supplier" tag
    add_many2many_tag(page, "category_id", "Supplier")
    page.wait_for_timeout(300)

    # Set job position
    fill_field(page, "function", "Procurement Partner")
    page.wait_for_timeout(300)

    # Save
    save_form(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
