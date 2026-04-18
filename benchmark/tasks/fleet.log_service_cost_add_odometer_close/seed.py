"""Seed for fleet.log_service_cost_add_odometer_close.

Creates vehicle BENCH-TRUCK-01 (Benchmark Truck, driver = admin) and
a vendor 'Bench Garage'. The agent must create a service record with
a cost of 120 EUR, fill the odometer field (which auto-creates an
fleet.vehicle.odometer log), save, then advance the service state to
'Done' via the clickable statusbar.

Hard-tier calibration:
- The odometer field lives in the RIGHT column of the service form
  (below Driver); browser-use tends to fill the left column (type, date,
  cost, vendor) and skip the right column.
- The status bar (state = new/running/done/cancelled) is clickable
  only from the saved record header. Agents often stop after Save and
  forget the state transition.
- 'Cost' is displayed via monetary widget with EUR symbol; the company
  default currency is flipped to EUR in seed so the widget matches
  the prompt description and check.py arithmetic.
"""

BRAND_NAME = "Benchmark Auto"
MODEL_NAME = "Benchmark Truck"
PLATE = "BENCH-TRUCK-01"
VENDOR_NAME = "Bench Garage"
SERVICE_TYPE_NAME = "Oil Change"


def setup(env):
    Vehicle = env["fleet.vehicle"]
    Service = env["fleet.vehicle.log.services"]
    Odometer = env["fleet.vehicle.odometer"]
    Partner = env["res.partner"]
    Brand = env["fleet.vehicle.model.brand"]
    Model = env["fleet.vehicle.model"]
    ServiceType = env["fleet.service.type"]

    # --- Cleanup prior runs (child-first) ---
    stale_vehicles = Vehicle.with_context(active_test=False).search([
        ("license_plate", "=", PLATE),
    ])
    if stale_vehicles:
        Service.with_context(active_test=False).search([
            ("vehicle_id", "in", stale_vehicles.ids),
        ]).unlink()
        Odometer.search([("vehicle_id", "in", stale_vehicles.ids)]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "fleet.vehicle"),
            ("res_id", "in", stale_vehicles.ids),
        ]).unlink()
        stale_vehicles.unlink()

    stale_models = Model.search([
        ("name", "=", MODEL_NAME),
    ])
    stale_models.unlink()

    Partner.with_context(active_test=False).search([
        ("name", "=", VENDOR_NAME),
    ]).unlink()

    # --- Flip company currency to EUR so the 'Cost' monetary widget
    # displays with the same currency the prompt specifies. If EUR is
    # inactive in the fresh DB, activate it.
    eur = env["res.currency"].with_context(active_test=False).search([
        ("name", "=", "EUR"),
    ], limit=1)
    if eur:
        if not eur.active:
            eur.write({"active": True})
        env.company.write({"currency_id": eur.id})

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

    # --- Ensure the Oil Change service type exists (category='service')
    service_type = ServiceType.search([
        ("name", "=", SERVICE_TYPE_NAME),
        ("category", "=", "service"),
    ], limit=1)
    if not service_type:
        ServiceType.create({
            "name": SERVICE_TYPE_NAME,
            "category": "service",
        })

    # --- Seeded vendor (so autocomplete finds it without quick-create)
    Partner.create({
        "name": VENDOR_NAME,
        "supplier_rank": 1,
    })

    # --- Create the vehicle with admin as driver.
    # Note: fleet.vehicle.write({'driver_id': ...}) auto-creates a
    # fleet.vehicle.assignation.log with date_start=today. Using
    # create() instead of write() so the log is created at seed time
    # (harmless; task does not track assignation logs).
    admin = env.ref("base.user_admin")
    Vehicle.create({
        "license_plate": PLATE,
        "model_id": model.id,
        "driver_id": admin.partner_id.id,
    })
