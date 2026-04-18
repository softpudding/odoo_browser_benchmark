"""Seed for mrp_account.confirm_mo_check_account_move.

Category (MEDIUM): closed_loop_cross_module.

Creates a product category with property_valuation='real_time' (automated
inventory valuation), a finished product 'Bench Manuf Item' in that
category, three components, a BoM, components on-hand, and a confirmed
manufacturing order M-BENCH-ACC-001 for 5 units.

When the agent closes the MO (Produce -> Mark As Done), stock_account's
`_create_account_move` automatically creates and posts an account.move
for the finished stock move (WIP -> Stock Valuation). The agent then
navigates to Accounting -> Journal Entries to confirm that posted entry.

Required modules: mrp_account is auto-installed when mrp + stock_account
are present. The base snapshot ships with mrp (base_modules.txt) and
stock_account (pulled in via sale/account chain). If mrp_account is not
yet installed in the target DB, force-install it here.
"""


MO_NAME = "M-BENCH-ACC-001"
FINISHED_NAME = "Bench Manuf Item"
COMPONENTS = [
    ("Bench Acc Frame", 1.0),
    ("Bench Acc Bolt", 4.0),
    ("Bench Acc Panel", 1.0),
]
CATEG_NAME = "Bench Auto Valuation"
MO_QTY = 5.0


def _ensure_mrp_account(env):
    """Force-install mrp_account if it isn't already installed."""
    for mod_name in ("mrp_account", "stock_account"):
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
    clean_names = [FINISHED_NAME] + [n for n, _ in COMPONENTS]
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
    # Only unlink categories that have no products left.
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
    Production location's valuation_account_id (aka 'Cost of Production')
    all wired up. Without the Production location's valuation_account_id,
    stock_account's `_should_create_account_move` returns False on the
    finished move and no auto-account.move is created when the MO closes.
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

    # Cost of Production account on the Production location (required
    # for auto-generating an account.move on the finished stock move).
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

    # Also ensure a stock valuation account on the Stock (internal) loc
    # so the incoming leg of the finished move is balanced.
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

    # Grant admin accounting groups so the Journal Entries list is
    # reachable/usable.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "account.group_account_readonly",
        "account.group_account_invoice",
        "account.group_account_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})

    _cleanup(env)
    _ensure_valuation_accounts(env)

    Product = env["product.product"]
    Category = env["product.category"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    MO = env["mrp.production"]

    # --- Product category with automated (real_time) valuation ---
    categ = Category.search([("name", "=", CATEG_NAME)], limit=1)
    if not categ:
        categ = Category.create({
            "name": CATEG_NAME,
            "property_valuation": "real_time",
            "property_cost_method": "standard",
        })
    else:
        categ.write({
            "property_valuation": "real_time",
            "property_cost_method": "standard",
        })

    # --- Finished product (standard_price > 0 so valuation has value) ---
    finished = Product.create({
        "name": FINISHED_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "categ_id": categ.id,
        "standard_price": 100.0,
        "list_price": 200.0,
    })

    # --- Component products (also storable; standard_price so MO has cost) ---
    components = {}
    for name, _qty in COMPONENTS:
        components[name] = Product.create({
            "name": name,
            "type": "consu",
            "is_storable": True,
            "tracking": "none",
            "categ_id": categ.id,
            "standard_price": 10.0,
        })

    # --- Stock components on-hand at main WH stock location ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    for name, qty_per in COMPONENTS:
        env["stock.quant"]._update_available_quantity(
            components[name], stock_loc, qty_per * MO_QTY * 2,
        )

    # --- BoM: 1 finished = components at listed qty ---
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
