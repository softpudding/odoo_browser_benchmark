"""Oracle for fleet.add_vehicle_log_odometer.

Solves the task entirely through the Odoo UI (Playwright):
  1. Open the Fleet app.
  2. Click New and create a vehicle (Tesla Motors / Model 3, plate FLEET-ADD-01).
  3. Save the vehicle.
  4. Navigate to Fleet > Odometer (the fleet.vehicle.odometer editable list).
  5. Click New to insert a new editable row, then fill vehicle / date / value.
  6. Save the row.
"""

from benchmark.oracle_helpers import (
    _dismiss_tooltips,
    _wait_no_loading,
    click_create,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_many2one,
)


def _open_fleet_submenu(page, item_label: str) -> None:
    """Open the Fleet top-level menu and click a sub-item by (substring) label."""
    page.locator(
        '.o_main_navbar button.dropdown-toggle:has-text("Fleet")'
    ).first.click()
    page.wait_for_timeout(400)
    items = page.locator(".dropdown-menu:visible .dropdown-item")
    target = items.filter(has_text=item_label)
    if target.count() == 0:
        raise RuntimeError(
            f"Fleet menu has no item matching {item_label!r}"
        )
    target.first.click()
    page.wait_for_load_state("load")
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(500)

    # ---- Step 1: Create the vehicle ----
    click_create(page)
    page.wait_for_timeout(800)

    # fleet.vehicle form: model_id is a many2one to fleet.vehicle.model.
    # The dropdown label is "Tesla Motors/Model 3"; search by "Model 3".
    set_many2one(page, "model_id", "Model 3")

    # License plate is a simple Char field.
    fill_field(page, "license_plate", "FLEET-ADD-01")

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)

    # ---- Step 2: Navigate to the Odometer list (Fleet > Odometer) ----
    _open_fleet_submenu(page, "Odometer")
    page.wait_for_timeout(500)
    _dismiss_tooltips(page)

    # ---- Step 3: Create the odometer log ----
    # The list view is editable="top" — clicking "New" inserts an inline row
    # at the top, focused for inline editing.
    click_create(page)
    page.wait_for_timeout(500)

    # The inline row exposes cells keyed by field name. Helpers use the
    # ".o_list_view .o_data_row" locator which matches editable rows too.
    # vehicle_id many2one: search by plate for precision.
    _set_inline_many2one(page, "vehicle_id", "FLEET-ADD-01")

    # date cell — the editable list renders a plain input, not a button.
    _set_inline_input(page, "date", "04/15/2026")

    # value (odometer km) — numeric input.
    _set_inline_input(page, "value", "15000")

    save_form(page)
    page.wait_for_timeout(800)
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Inline (editable list) helpers — localised to this oracle to avoid touching
# the shared oracle_helpers.py.
# ---------------------------------------------------------------------------

def _editable_row(page):
    """Return the currently-editable row (the one with input fields)."""
    # The editable row is the one that contains a focused input or the
    # "o_selected_row" marker. Fall back to the first data row.
    selected = page.locator(".o_list_view .o_data_row.o_selected_row")
    if selected.count() > 0:
        return selected.first
    return page.locator(".o_list_view .o_data_row").first


def _set_inline_input(page, field_name: str, value: str) -> None:
    row = _editable_row(page)
    cell = row.locator(f"td[name='{field_name}']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(400)
    _wait_no_loading(page)


def _set_inline_many2one(page, field_name: str, search_text: str) -> None:
    row = _editable_row(page)
    cell = row.locator(f"td[name='{field_name}']").first
    cell.click()
    page.wait_for_timeout(300)
    inp = cell.locator("input").first
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(800)
    dropdown = page.locator(
        ".dropdown-menu .dropdown-item, .ui-autocomplete .ui-menu-item"
    )
    item = dropdown.filter(has_text=search_text).first
    item.click()
    page.wait_for_timeout(400)
    _wait_no_loading(page)


run_oracle(oracle)
