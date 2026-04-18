"""Seed a phantom-kit BoM + a normal BoM that references the kit.

Category (HARD): deep_ui_interaction — tests whether the agent understands
kit (phantom) BoM auto-expansion on MO confirm.

Pre-seeded products:
  - Bench Sub-A (storable)
  - Bench Sub-B (storable)
  - Bench Frame (storable)
  - Bench Kit (storable) — has mrp.bom type='phantom' with 1xSub-A + 2xSub-B
  - Bench Assembly (storable) — has mrp.bom type='normal' with 1xBench Kit +
    1xBench Frame

The agent must create a draft MO for Bench Assembly (qty 1, reference
'M-BENCH-KIT-001') and click Confirm. On confirm, _get_moves_raw_values
calls bom.explode(), which recursively expands the phantom Bench Kit into
its sub-components. The confirmed MO then has THREE move_raw_ids rows:
  - Bench Sub-A (qty 1)
  - Bench Sub-B (qty 2)
  - Bench Frame (qty 1)

NO raw move should reference 'Bench Kit' directly.

Calibration: browser-use may mis-read the prompt as "add 2 components"
and try to manually edit the Components tab or BoM, OR confuse the two
BoMs (kit vs assembly) and pick the wrong one.
"""


ASSEMBLY_NAME = "Bench Assembly"
KIT_NAME = "Bench Kit"
FRAME_NAME = "Bench Frame"
SUB_A_NAME = "Bench Sub-A"
SUB_B_NAME = "Bench Sub-B"
MO_NAME = "M-BENCH-KIT-001"

CLEAN_PRODUCT_NAMES = [
    ASSEMBLY_NAME,
    KIT_NAME,
    FRAME_NAME,
    SUB_A_NAME,
    SUB_B_NAME,
]


def _cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

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

    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", CLEAN_PRODUCT_NAMES),
    ])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()


def setup(env):
    _cleanup(env)

    Product = env["product.product"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]

    # --- Create the five products. ---
    sub_a = Product.create({
        "name": SUB_A_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    sub_b = Product.create({
        "name": SUB_B_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    frame = Product.create({
        "name": FRAME_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    kit = Product.create({
        "name": KIT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    assembly = Product.create({
        "name": ASSEMBLY_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create the phantom/kit BoM for Bench Kit (1 kit = 1 Sub-A + 2 Sub-B). ---
    kit_bom = BOM.create({
        "product_tmpl_id": kit.product_tmpl_id.id,
        "product_qty": 1,
        "type": "phantom",
        "consumption": "flexible",
    })
    BOMLine.create({
        "bom_id": kit_bom.id,
        "product_id": sub_a.id,
        "product_qty": 1.0,
    })
    BOMLine.create({
        "bom_id": kit_bom.id,
        "product_id": sub_b.id,
        "product_qty": 2.0,
    })

    # --- Create the normal BoM for Bench Assembly
    #     (1 assembly = 1 Bench Kit + 1 Bench Frame). ---
    assembly_bom = BOM.create({
        "product_tmpl_id": assembly.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({
        "bom_id": assembly_bom.id,
        "product_id": kit.id,
        "product_qty": 1.0,
    })
    BOMLine.create({
        "bom_id": assembly_bom.id,
        "product_id": frame.id,
        "product_qty": 1.0,
    })

    # --- Optionally stock the atomic components so the MO will also show
    #     reserved availability (not required to confirm, but avoids red
    #     availability badges that could distract the agent). ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    for prod, qty in ((sub_a, 5.0), (sub_b, 10.0), (frame, 5.0)):
        env["stock.quant"]._update_available_quantity(prod, stock_loc, qty)

    # --- Sanity probe: confirm the BoM explode expands the kit as expected. ---
    # Do NOT create the MO here — the agent must do that. Verify seed invariants:
    assert kit_bom.type == "phantom", "kit BoM must be phantom"
    assert assembly_bom.type == "normal", "assembly BoM must be normal"
    assert len(assembly_bom.bom_line_ids) == 2, "assembly BoM must have 2 lines"
    assert len(kit_bom.bom_line_ids) == 2, "kit BoM must have 2 lines"
