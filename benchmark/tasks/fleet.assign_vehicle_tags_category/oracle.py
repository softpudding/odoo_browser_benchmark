"""Oracle for fleet.assign_vehicle_tags_category.

Navigate to Fleet, open the seeded vehicle (Toyota/Benchmark Tag Vehicle/TAG-001),
add two tags ("Executive" and "Sales Team") via the many2many_tags widget,
set the Category to "Company Cars", then save.
"""

from benchmark.oracle_helpers import (
    add_many2many_tag,
    click_list_row,
    ensure_list_view,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # The default fleet view may be kanban; switch to list for a deterministic
    # row click.
    ensure_list_view(page)
    page.wait_for_timeout(500)

    # Open the seeded vehicle by its label
    click_list_row(page, "Benchmark Tag Vehicle")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Add the two tags (m2m tags widget, options: no_create_edit=True,
    # so we must pick existing tags — which the seed created).
    add_many2many_tag(page, "tag_ids", "Executive")
    page.wait_for_timeout(300)
    add_many2many_tag(page, "tag_ids", "Sales Team")
    page.wait_for_timeout(300)

    # Set the category (many2one selector)
    set_many2one(page, "category_id", "Company Cars")
    page.wait_for_timeout(300)

    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
