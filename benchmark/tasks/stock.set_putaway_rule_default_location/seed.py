"""Seed for stock.set_putaway_rule_default_location (medium).

Category 5: Deep UI interaction (Configuration menu navigation + 3 m2o
fields in an inline editable list row).

Seeds:
  * Storable product 'Bench Putaway Item' (type='consu' + is_storable=True)
    with NO pre-existing putaway rule.
  * Sub-location 'Shelf B' under WH/Stock (usage='internal') — the
    destination location the agent must pick from the autocomplete.
  * Admin is granted `stock.group_stock_multi_locations` (so the Putaway
    Rules menu + Location columns are visible) AND `stock.group_adv_location`
    (advanced routing group; not strictly required for putaway but routinely
    paired with multi-locations tasks and unlocks adjacent advanced-routing
    UI the agent might inspect).

The task difficulty is: navigate from Inventory to Configuration > Putaway
Rules (not via the product form smart button), click New, and fill THREE
many2one fields inline (product_id, location_in_id, location_out_id) from
a single editable list row without leaving a blank placeholder behind.
"""

PRODUCT_NAME = "Bench Putaway Item"
SHELF_NAME = "Shelf B"
STOCK_COMPLETE = "WH/Stock"


def _cleanup(env):
    # Remove any pre-existing putaway rules that reference our seeded
    # artifacts so re-runs start fresh.
    prod = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if prod:
        env["stock.putaway.rule"].search([
            ("product_id", "=", prod.id)
        ]).unlink()

    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("complete_name", "=", f"WH/Stock/{SHELF_NAME}"),
    ], limit=1)
    if shelf:
        env["stock.putaway.rule"].search([
            ("location_out_id", "=", shelf.id),
        ]).unlink()

    # Remove the product itself so the seed recreates a pristine template
    # (keeps the state-diff minimal and avoids stale data from prior runs).
    if prod:
        try:
            env["stock.move.line"].search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "=", prod.id)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            prod.product_tmpl_id.sudo().unlink()
        except Exception:
            pass


def _ensure_stock_location(env):
    loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if not loc:
        wh = env["stock.warehouse"].search([], limit=1)
        loc = wh.lot_stock_id
    return loc


def _ensure_shelf(env, parent_stock):
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("location_id", "=", parent_stock.id),
    ], limit=1)
    if not shelf:
        shelf = env["stock.location"].create({
            "name": SHELF_NAME,
            "location_id": parent_stock.id,
            "usage": "internal",
        })
    return shelf


def setup(env):
    _cleanup(env)

    # Grant admin the multi-locations group (so Putaway Rules menu +
    # Location columns are visible) and the advanced-location group
    # (routinely paired with multi-locations for any warehouse routing
    # task — makes sure the advanced routing UI is discoverable).
    admin = env.ref("base.user_admin")
    mlg = env.ref("stock.group_stock_multi_locations", raise_if_not_found=False)
    if mlg:
        admin.group_ids |= mlg
    adv = env.ref("stock.group_adv_location", raise_if_not_found=False)
    if adv:
        admin.group_ids |= adv

    stock_loc = _ensure_stock_location(env)
    _ensure_shelf(env, stock_loc)

    # Create the storable product with no existing putaway rule.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 18.0,
        "standard_price": 9.0,
        "sale_ok": True,
        "purchase_ok": True,
    })
    product = tmpl.product_variant_id

    # Sanity: no putaway rule for this product yet.
    existing = env["stock.putaway.rule"].search(
        [("product_id", "=", product.id)]
    )
    if existing:
        existing.unlink()

    # Force flush
    env.cr.execute("SELECT 1")
