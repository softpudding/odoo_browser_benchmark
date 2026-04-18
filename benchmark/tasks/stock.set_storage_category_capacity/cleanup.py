"""Cleanup for stock.set_storage_category_capacity."""


CATEGORY_NAME = "Bench Small Bin"
LOCATION_NAME = "Bench Small Bin Area"
LOCATION_COMPLETE_NAME = "WH/Stock/Bench Small Bin Area"


def cleanup(env):
    # Detach the storage category from any location using it so it can be
    # deleted cleanly.
    cat = env["stock.storage.category"].search([("name", "=", CATEGORY_NAME)])
    if cat:
        env["stock.location"].search(
            [("storage_category_id", "in", cat.ids)]
        ).write({"storage_category_id": False})
        try:
            cat.unlink()
        except Exception:
            # Fallback: detach via sudo if possible
            try:
                cat.sudo().unlink()
            except Exception:
                pass

    # Remove the seeded sub-location (idempotent across re-runs).
    loc = env["stock.location"].search(
        [("complete_name", "=", LOCATION_COMPLETE_NAME)], limit=1
    )
    if not loc:
        loc = env["stock.location"].search(
            [("name", "=", LOCATION_NAME)], limit=1
        )
    if loc:
        env["stock.quant"].search(
            [("location_id", "in", loc.ids)]
        ).unlink()
        other_moves = env["stock.move"].search_count([
            "|",
            ("location_id", "in", loc.ids),
            ("location_dest_id", "in", loc.ids),
        ])
        if other_moves == 0:
            try:
                loc.unlink()
            except Exception:
                try:
                    loc.active = False
                except Exception:
                    pass
        else:
            try:
                loc.active = False
            except Exception:
                pass
