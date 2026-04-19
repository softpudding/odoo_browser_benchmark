"""Oracle for fleet.assign_vehicle_create_contract_active.

Navigate to Fleet, open the seeded BENCH-VAN-01 vehicle, click its
Contracts smart button, create a new contract with Type=Leasing, Start
Date=2026-04-20, Recurring Cost=200 monthly, Vendor=Bench Lease Co,
save, then click 'Running' on the clickable statusbar to activate the
contract.
"""

from benchmark.oracle_helpers import (
    click_create,
    click_list_row,
    click_stat_button,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    set_date,
    set_many2one,
    _wait_for_ready,
    _wait_no_loading,
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/fleet")
    _wait_no_loading(page)
    page.wait_for_timeout(1000)

    # Open the seeded vehicle.
    click_list_row(page, "BENCH-VAN-01")
    _wait_for_ready(page)
    page.wait_for_timeout(800)

    # Click the Contracts stat button.
    click_stat_button(page, "Contracts")
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # Click New.
    click_create(page)
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    # Fill the contract form.
    set_many2one(page, "cost_subtype_id", "Leasing")
    page.wait_for_timeout(300)
    set_many2one(page, "insurer_id", "Bench Lease Co")
    page.wait_for_timeout(300)
    set_date(page, "start_date", "04/20/2026")
    page.wait_for_timeout(300)
    fill_field(page, "cost_generated", "200.00")
    page.wait_for_timeout(300)

    save_form(page)
    _wait_no_loading(page)
    page.wait_for_timeout(800)

    # state statusbar: click 'Running' unless state is already 'open'.
    # The `state` field uses widget='statusbar' options={'clickable':'1'}.
    # On fresh-create through the UI, default `state='open'` applies
    # (the write()-override hook that flips based on start_date fires
    # only on writes, not on initial create), so the Running step may
    # already be current (aria-current='step', disabled). In that case
    # we skip the click to avoid a Playwright timeout on a disabled btn.
    running_locator = page.locator(
        ".o_statusbar_status button[data-value='open']:visible"
    ).first
    already_open = False
    try:
        if running_locator.get_attribute("aria-current") == "step":
            already_open = True
    except Exception:
        already_open = False

    if not already_open:
        running_locator.click()
        page.wait_for_timeout(800)
        _wait_no_loading(page)

    # Re-save in case autosave did not fire.
    try:
        save_form(page)
    except Exception:
        pass
    _wait_no_loading(page)
    page.wait_for_timeout(500)


run_oracle(oracle)
