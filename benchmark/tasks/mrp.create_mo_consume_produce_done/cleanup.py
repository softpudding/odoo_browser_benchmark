"""Cleanup for mrp.create_mo_consume_produce_done."""

FINISHED = "Bench Assembly"
PART_A = "Bench Part A"
PART_B = "Bench Part B"


def cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Scrap = env["stock.scrap"]

    products = Product.with_context(active_test=False).search([
        ("name", "in", [FINISHED, PART_A, PART_B]),
    ])

    if products:
        # Cancel and drop any MOs tied to the finished/component products.
        mos = MO.search([("product_id", "in", products.ids)])
        for mo in mos:
            if mo.state not in ("draft", "cancel"):
                try:
                    mo.action_cancel()
                except Exception:
                    pass
        # Draft scraps can be unlinked; done ones become harmless after
        # we remove the MO/product records.
        scraps = Scrap.with_context(active_test=False).search([
            ("production_id", "in", mos.ids),
        ])
        for s in scraps:
            if s.state == "draft":
                try:
                    s.unlink()
                except Exception:
                    pass
        try:
            mos.unlink()
        except Exception:
            pass

        boms = BOM.search([
            ("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids),
        ])
        try:
            boms.unlink()
        except Exception:
            pass
        try:
            products.mapped("product_tmpl_id").unlink()
        except Exception:
            pass
