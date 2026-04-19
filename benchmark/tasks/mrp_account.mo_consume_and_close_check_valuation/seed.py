"""Seed for mrp_account.mo_consume_and_close_check_valuation.

Category (HARD): closed_loop_cross_module.

Creates a product category with property_valuation='real_time'
(automated inventory valuation), a finished product 'Bench Assembly'
in that category (standard_price=0 so the finished move's value is
derived from component cost, not overridden by the standard price),
two components 'Bench Component 1' / 'Bench Component 2' (each at
standard_price=10 with 1 unit consumed per kit), a BoM, components
on-hand, and a confirmed manufacturing order 'MO-BENCH-VAL' for 1
unit.

When the agent closes the MO (Produce All / Mark as Done),
stock_account's `_action_done` calls `_set_value()` on the raw-out
and finished-in moves: each raw move.value becomes the consumed
standard cost (10.0 each), and the finished move.value ends up
equal to the summed component cost (20.0) thanks to the Odoo 19
`_get_value_from_production` fallback path.

`stock.account` is the key dependency that upgrades `stock.move` with
`value`, `is_in`, `is_out`, `is_valued`, and the auto-journal logic.
mrp_account (auto-installed when mrp + stock_account are present) is
what lets the MRP-side seeing real-time valuation on production.
"""


MO_NAME = "MO-BENCH-VAL"
FINISHED_NAME = "Bench Assembly"
COMPONENTS = [
    ("Bench Component 1", 1.0),
    ("Bench Component 2", 1.0),
]
CATEG_NAME = "Bench Val Real Time"
COMPONENT_COST = 10.0
MO_QTY = 1.0


def _ensure_mrp_account(env):
    """Force-install stock_account and mrp_account if not already installed.

    mrp_account is auto_install=True with deps [mrp, stock_account]; both
    mrp (base_modules.txt) and stock_account (pulled in via sale/account
    chain) ship in the base snapshot, so mrp_account is normally already
    installed. Defensive install in case a benchmark_base variant drops
    one of them.
    """
    for mod_name in ("stock_account", "mrp_account"):
        mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
        if mod and mod.state != "installed":
            mod.button_immediate_install()


def _cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Category = env["product.category"]

    # MOs: cancel + unlink (including backorders).
    stale_mo = MO.search([
        "|",
        ("name", "=", MO_NAME),
        ("name", "=like", MO_NAME + "-%"),
    ])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    stale_mo.unlink()

    # Products + BoMs.
    clean_names = [FINISHED_NAME] + [n for n, _q in COMPONENTS]
    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", clean_names),
    ])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    # Product category (delete only if unused).
    stale_categ = Category.search([("name", "=", CATEG_NAME)])
    for categ in stale_categ:
        prod_count = Product.with_context(active_test=False).search_count([
            ("categ_id", "=", categ.id),
        ])
        if prod_count == 0:
            try:
                categ.unlink()
            except Exception:
                pass


def _ensure_valuation_accounts(env):
    """Ensure the company has the stock valuation accounts + journal +
    Production location's valuation_account_id (aka "Cost of Production")
    all wired up. Without the Production location's valuation_account_id,
    stock_account's `_should_create_account_move` returns False on the
    finished move and no auto-account.move is created when the MO closes.
    Even though we only assert on stock.move.value (not account.move) in
    this task, the account_move side acts as an invariant guard against
    silent misconfiguration of the base snapshot.
    """
    company = env.company

    # company.account_stock_valuation_id
    if not company.account_stock_valuation_id:
        acc = env["account.account"].search([
            ("name", "=", "Stock Valuation"),
            ("company_ids", "in", company.id),
        ], limit=1)
        if not acc:
            acc = env["account.account"].create({
                "name": "Stock Valuation",
                "code": "140000",
                "account_type": "asset_current",
            })
        company.account_stock_valuation_id = acc

    # company.account_stock_journal_id (fallback to any general journal)
    if not company.account_stock_journal_id:
        journal = env["account.journal"].search([
            ("type", "=", "general"),
            ("company_id", "=", company.id),
        ], limit=1)
        if journal:
            company.account_stock_journal_id = journal

    cost_of_prod = env["account.account"].search([
        ("company_ids", "in", company.id),
        ("name", "=", "Cost of Production"),
    ], limit=1)
    if not cost_of_prod:
        cost_of_prod = env["account.account"].create({
            "name": "Cost of Production",
            "code": "500100",
            "account_type": "expense",
        })

    prod_locations = env["stock.location"].search([
        ("usage", "=", "production"),
        ("company_id", "=", company.id),
    ])
    for loc in prod_locations:
        if not loc.valuation_account_id:
            loc.valuation_account_id = cost_of_prod

    stock_val_acc = company.account_stock_valuation_id
    wh_stock_locs = env["stock.location"].search([
        ("usage", "=", "internal"),
        ("company_id", "=", company.id),
    ])
    for loc in wh_stock_locs:
        if not loc.valuation_account_id and stock_val_acc:
            loc.valuation_account_id = stock_val_acc


def setup(env):
    _ensure_mrp_account(env)
    _cleanup(env)
    _ensure_valuation_accounts(env)

    Product = env["product.product"]
    Category = env["product.category"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    MO = env["mrp.production"]

    # --- Product category with automated (real_time) valuation ---
    # cost_method='average' is required for the finished product so that
    # its move value comes from `_cal_price` (sum of consumed component
    # values + work-center cost) and NOT from `product.standard_price`
    # (which is 0 here by design). Under cost_method='standard' the
    # finished move would pick up `standard_price=0` and value=0.
    categ = Category.search([("name", "=", CATEG_NAME)], limit=1)
    if not categ:
        categ = Category.create({
            "name": CATEG_NAME,
            "property_valuation": "real_time",
            "property_cost_method": "average",
        })
    else:
        categ.write({
            "property_valuation": "real_time",
            "property_cost_method": "average",
        })

    # --- Finished product (standard_price=0 so the finished stock.move
    # gets valued via production's raw-cost rollup, not overridden) ---
    finished = Product.create({
        "name": FINISHED_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "categ_id": categ.id,
        "standard_price": 0.0,
        "list_price": 50.0,
    })

    # --- Component products (standard_price=10 drives per-component
    # consumption value) ---
    components = {}
    for name, _qty in COMPONENTS:
        components[name] = Product.create({
            "name": name,
            "type": "consu",
            "is_storable": True,
            "tracking": "none",
            "categ_id": categ.id,
            "standard_price": COMPONENT_COST,
        })

    # --- Stock components on-hand at main WH stock location ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    for name, qty_per in COMPONENTS:
        env["stock.quant"]._update_available_quantity(
            components[name], stock_loc, qty_per * MO_QTY * 5,
        )

    # --- BoM: 1 finished Bench Assembly = 1 x Component 1 + 1 x Component 2 ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    for name, qty in COMPONENTS:
        BOMLine.create({
            "bom_id": bom.id,
            "product_id": components[name].id,
            "product_qty": qty,
        })

    # --- Create + confirm MO (state='confirmed') ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": MO_QTY,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    if mo.state != "confirmed":
        raise RuntimeError(
            f"Seed invariant failed: MO state is {mo.state!r}, expected 'confirmed'"
        )
    # Sanity check the raw moves are wired to the components (2 raw moves).
    if len(mo.move_raw_ids) != 2:
        raise RuntimeError(
            f"Seed invariant failed: MO has {len(mo.move_raw_ids)} raw moves, expected 2"
        )
