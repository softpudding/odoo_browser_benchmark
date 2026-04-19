"""Seed for fleet.assign_vehicle_create_contract_active.

Creates vehicle BENCH-VAN-01 (Bench Van 01, driver = Bench Driver Partner)
and a vendor partner 'Bench Lease Co'. Also ensures the 'Leasing' contract
cost_subtype (category='contract') exists. The agent must open the
vehicle, click the Contracts smart button, create a new contract with
Type=Leasing + Vendor=Bench Lease Co + Start Date=2026-04-20 +
Recurring Cost=200 monthly, save, then click 'Running' on the clickable
statusbar to flip `state` from 'futur' -> 'open'.

Medium-tier calibration:
- The contract form's state default is 'open', BUT the `write()` override
  auto-flips state to 'futur' when start_date is in the future (relative
  to today). So a contract saved with start_date=2026-04-20 when today
  is 2026-04-19 lands in 'New' (futur), not 'Running' (open). The agent
  must click the 'Running' step on the clickable statusbar to satisfy
  `state='open'`.
- The form has NO `action_activate` or similar header button; the only
  way to flip state is via the clickable statusbar (widget='statusbar',
  options={'clickable': '1'}).
- `fleet.vehicle.write({'driver_id': ...})` auto-creates an
  `fleet.vehicle.assignation.log`. Using create() instead so this log
  is created once at seed time (harmless; task does not track it).
"""

BRAND_NAME = "Bench Mobility"
MODEL_NAME = "Bench Van"
PLATE = "BENCH-VAN-01"
DRIVER_NAME = "Bench Driver Partner"
VENDOR_NAME = "Bench Lease Co"
CONTRACT_TYPE_NAME = "Leasing"


def setup(env):
    Vehicle = env["fleet.vehicle"]
    Contract = env["fleet.vehicle.log.contract"]
    Partner = env["res.partner"]
    Brand = env["fleet.vehicle.model.brand"]
    Model = env["fleet.vehicle.model"]
    ServiceType = env["fleet.service.type"]

    # --- Cleanup prior runs (child-first) ---
    stale_vehicles = Vehicle.with_context(active_test=False).search([
        ("license_plate", "=", PLATE),
    ])
    if stale_vehicles:
        Contract.with_context(active_test=False).search([
            ("vehicle_id", "in", stale_vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.log.services"].with_context(active_test=False).search([
            ("vehicle_id", "in", stale_vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.odometer"].search([
            ("vehicle_id", "in", stale_vehicles.ids),
        ]).unlink()
        env["fleet.vehicle.assignation.log"].search([
            ("vehicle_id", "in", stale_vehicles.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "in", stale_vehicles.ids),
        ]).unlink()
        stale_vehicles.unlink()

    # Clean duplicate models with our name (safe: filter by brand match later).
    stale_models = Model.search([("name", "=", MODEL_NAME)])
    stale_models.unlink()

    # Clean any prior vendor/driver partners named like our seeds.
    Partner.with_context(active_test=False).search([
        ("name", "in", [VENDOR_NAME, DRIVER_NAME]),
    ]).unlink()

    # --- Ensure brand + model exist ---
    brand = Brand.search([("name", "=", BRAND_NAME)], limit=1)
    if not brand:
        brand = Brand.create({"name": BRAND_NAME})

    model = Model.search([
        ("name", "=", MODEL_NAME),
        ("brand_id", "=", brand.id),
    ], limit=1)
    if not model:
        model = Model.create({
            "name": MODEL_NAME,
            "brand_id": brand.id,
            "vehicle_type": "car",
        })

    # --- Ensure the Leasing contract type exists (category='contract')
    contract_type = ServiceType.search([
        ("name", "=", CONTRACT_TYPE_NAME),
        ("category", "=", "contract"),
    ], limit=1)
    if not contract_type:
        ServiceType.create({
            "name": CONTRACT_TYPE_NAME,
            "category": "contract",
        })

    # --- Seeded vendor partner (for contract vendor autocomplete)
    Partner.create({
        "name": VENDOR_NAME,
        "supplier_rank": 1,
        "company_type": "company",
    })

    # --- Seeded driver partner (non-admin so the task explicitly
    # references a distinct partner per spec)
    driver = Partner.create({
        "name": DRIVER_NAME,
        "company_type": "person",
    })

    # --- Create the vehicle using create() (single assignation log side-effect)
    Vehicle.create({
        "license_plate": PLATE,
        "model_id": model.id,
        "driver_id": driver.id,
    })
