"""Seed for lunch.create_vendor_product_order_for_today.

Category: deep_ui_interaction (MEDIUM).

The Lunch app is NOT in the base snapshot -- seed installs it on
demand via ``button_immediate_install``.  After install:

- admin is auto-added to ``lunch.group_lunch_manager`` by the module's
  security data, so Configuration menus and the kiosk dashboard render.
- the default ``HQ Office`` lunch location and product categories
  (``Sandwich``, ``Pizza``, ``Burger``, ``Drinks``) are present from
  ``lunch_data.xml``.  The seed sets admin's ``last_lunch_location_id``
  so the kiosk dashboard pre-populates.
- the per-company ``lunch_minimum_threshold`` is bumped to 100 so
  admin's (empty) wallet doesn't block ``_check_wallet`` on
  ``update_quantity`` / ``action_order``.

We also:
- ensure an existing res.partner is flagged to auto-select in the
  vendor form (``Bench Cafe Partner``).
- clear out any ``lunch.supplier`` / ``lunch.product`` / ``lunch.order``
  rows with our target names from prior runs.
"""

VENDOR_NAME = "Bench Cafe"
PARTNER_NAME = "Bench Cafe Partner"
PRODUCT_NAME = "Veggie Wrap"


def _ensure_lunch_module(env):
    module = env["ir.module.module"].search([("name", "=", "lunch")], limit=1)
    if module and module.state != "installed":
        module.button_immediate_install()


def setup(env):
    _ensure_lunch_module(env)

    admin = env.ref("base.user_admin")

    # --- Cleanup prior runs (order -> product -> supplier -> partner) ---
    Order = env["lunch.order"].with_context(active_test=False)
    Order.search([("name", "=", PRODUCT_NAME)]).unlink()
    Order.search([("product_id.name", "=", PRODUCT_NAME)]).unlink()

    Product = env["lunch.product"].with_context(active_test=False)
    Product.search([("name", "=", PRODUCT_NAME)]).unlink()

    Supplier = env["lunch.supplier"].with_context(active_test=False)
    Supplier.search([("name", "=", VENDOR_NAME)]).unlink()

    # --- Ensure a pickable partner for the vendor form autocomplete ---
    # Picking the partner on the vendor form and then re-typing the Name
    # field RENAMES the partner (related name readonly=False).  Reset
    # the partner name back to PARTNER_NAME for deterministic re-runs.
    partner = env["res.partner"].search(
        [("name", "in", [PARTNER_NAME, VENDOR_NAME]), ("is_company", "=", True)],
        limit=1,
    )
    if partner:
        partner.write({"name": PARTNER_NAME, "phone": "+1 555 0199"})
    else:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "phone": "+1 555 0199",
        })

    # --- Ensure Sandwich category exists (default lunch_data ships it) ---
    categ = env["lunch.product.category"].search(
        [("name", "=", "Sandwich")], limit=1
    )
    if not categ:
        categ = env["lunch.product.category"].create({"name": "Sandwich"})

    # --- Make sure HQ Office location is admin's default ---
    location = env["lunch.location"].search([("name", "=", "HQ Office")], limit=1)
    if not location:
        location = env["lunch.location"].create({"name": "HQ Office"})
    admin.sudo().last_lunch_location_id = location.id

    # --- Fund the wallet threshold so orders don't trip _check_wallet
    # and so the kiosk modal's Add To Cart button (gated by
    # display_add_button) is visible. Bump every company to be safe.
    env["res.company"].sudo().search([]).write({"lunch_minimum_threshold": 100.0})
