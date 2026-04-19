"""Seed products for mrp.create_bom_kit_type_for_product.

HARD: create a Bill of Materials from scratch whose **BoM Type** must be
**Kit** (non-default; the default is `Manufacture this Product` →
`type='normal'`). Combined traps:

1. **Non-default radio selection** — the `mrp.bom.type` field renders in
   Odoo 19 as a `widget="radio"` group with three options
   (Manufacture / Kit / Subcontracting). The visible label for `phantom`
   is "Kit". Browser agents consistently click the default option (the
   first one) instead of reading the prompt.
2. **o2m inline BoM lines** — two component lines must be added via
   **Add a line** under the Components tab with exact product names and
   quantities (`Bench Kit Comp A` × 2, `Bench Kit Comp B` × 3).

Pre-seeded products (no BoM):
  - `Bench Kit Finished`   (storable, tracking='none')
  - `Bench Kit Comp A`     (storable, tracking='none')
  - `Bench Kit Comp B`     (storable, tracking='none')

The agent must create ONE `mrp.bom` with:
  - product_tmpl_id = Bench Kit Finished
  - type = 'phantom' (UI label 'Kit')
  - product_qty = 1 (default)
  - bom_line_ids: [
        (Bench Kit Comp A, qty=2),
        (Bench Kit Comp B, qty=3),
    ]

Nothing is pre-seeded on `mrp.bom` — the task is a full create-from-scratch.
"""


FINISHED_NAME = "Bench Kit Finished"
COMP_A_NAME = "Bench Kit Comp A"
COMP_B_NAME = "Bench Kit Comp B"

CLEAN_PRODUCT_NAMES = [FINISHED_NAME, COMP_A_NAME, COMP_B_NAME]


def _cleanup(env):
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", CLEAN_PRODUCT_NAMES),
    ])
    if stale_prod:
        stale_bom = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        try:
            stale_bom.unlink()
        except Exception:
            pass
        try:
            stale_prod.mapped("product_tmpl_id").unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    Product = env["product.product"]

    # --- Storable products (no BoMs pre-seeded) ---
    finished = Product.create({
        "name": FINISHED_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_a = Product.create({
        "name": COMP_A_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_b = Product.create({
        "name": COMP_B_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Sanity probes ---
    assert finished.product_tmpl_id, "finished product must have a product_tmpl_id"
    assert comp_a.product_tmpl_id, "comp A product must have a product_tmpl_id"
    assert comp_b.product_tmpl_id, "comp B product must have a product_tmpl_id"
    # No BoM should exist for any of these products at seed time.
    for prod in (finished, comp_a, comp_b):
        boms = env["mrp.bom"].search([
            ("product_tmpl_id", "=", prod.product_tmpl_id.id),
        ])
        assert not boms, (
            f"{prod.name!r} must have no BoM at seed time, found {boms.ids}"
        )
