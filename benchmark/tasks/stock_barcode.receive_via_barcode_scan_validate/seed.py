"""Seed for stock_barcode.receive_via_barcode_scan_validate.

BLOCKED TASK — the `stock_barcode` addon is NOT present in this Odoo 19
Community checkout. The Barcode tablet UI at `/odoo/barcode` is shipped
exclusively in the Enterprise `stock_barcode` module.

Inspected the `odoo_benchmark` branch:
  - `addons/` contains `barcodes` (keyboard-event / nomenclature
    handler) and `barcodes_gs1_nomenclature` (GS1 AI parser) but NO
    `stock_barcode` directory.
  - `grep -rn "stock_barcode" addons/` returns only i18n strings and
    `addons/stock/models/res_config_settings.py` line 29:
        module_stock_barcode = fields.Boolean("Barcode Scanner")
    which is an `upgrade_boolean` toggle for the (absent) module.
  - No `/odoo/barcode` controller, no
    `stock_barcode.stock_barcode_action_main_menu` client action, no
    `BarcodePickingModel` JS class exists in this checkout.

Attempting to proceed would mean the agent navigates to `/odoo/barcode`
and hits an Odoo 404 (no client action registered), so there's no value
in seeding picking data that can never be processed through the
intended UI. This seed raises a clear error so the eval pipeline
records the blocker instead of silently creating orphan pickings.
"""


def setup(env):
    # Detect whether the Enterprise-only stock_barcode addon has been
    # vendored. If it ever becomes available, flip the branch below to
    # run the real seed.
    module = env["ir.module.module"].search(
        [("name", "=", "stock_barcode")], limit=1
    )
    has_stock_barcode = bool(module) and module.state == "installed"
    if not has_stock_barcode:
        raise RuntimeError(
            "BLOCKED: the `stock_barcode` addon is not installed "
            "(Enterprise-only). The Barcode tablet UI at /odoo/barcode "
            "is not reachable in this Odoo 19 Community checkout. "
            "See STATUS.md row 401 and RESULT.md for the re-enabling "
            "procedure."
        )

    # --- If / when enterprise addon is vendored, fill in the real seed ---
    # The sketch below documents what the real seed would do, kept as a
    # comment so future agents can flesh it out without rediscovering the
    # requirements.
    #
    # product_a = env["product.product"].search(
    #     [("default_code", "=", "BENCH-A-001")], limit=1
    # ) or env["product.product"].create({
    #     "name": "Bench Barcode A",
    #     "default_code": "BENCH-A-001",
    #     "barcode": "BENCH-A-001",
    #     "is_storable": True,
    # })
    # product_b = env["product.product"].search(
    #     [("default_code", "=", "BENCH-B-002")], limit=1
    # ) or env["product.product"].create({
    #     "name": "Bench Barcode B",
    #     "default_code": "BENCH-B-002",
    #     "barcode": "BENCH-B-002",
    #     "is_storable": True,
    # })
    # # Ensure no stale picking from a prior run
    # env["stock.picking"].with_context(active_test=False).search(
    #     [("name", "=", "R-BENCH-BC-001")]
    # ).sudo().write({"state": "cancel"})
    # warehouse = env["stock.warehouse"].search([], limit=1)
    # picking_type = warehouse.in_type_id
    # picking = env["stock.picking"].create({
    #     "name": "R-BENCH-BC-001",
    #     "picking_type_id": picking_type.id,
    #     "location_id": picking_type.default_location_src_id.id or
    #                    env.ref("stock.stock_location_suppliers").id,
    #     "location_dest_id": picking_type.default_location_dest_id.id,
    #     "move_ids": [
    #         (0, 0, {
    #             "name": product_a.display_name,
    #             "product_id": product_a.id,
    #             "product_uom_qty": 3.0,
    #             "product_uom": product_a.uom_id.id,
    #             "location_id": picking_type.default_location_src_id.id or
    #                            env.ref("stock.stock_location_suppliers").id,
    #             "location_dest_id": picking_type.default_location_dest_id.id,
    #         }),
    #         (0, 0, {
    #             "name": product_b.display_name,
    #             "product_id": product_b.id,
    #             "product_uom_qty": 3.0,
    #             "product_uom": product_b.uom_id.id,
    #             "location_id": picking_type.default_location_src_id.id or
    #                            env.ref("stock.stock_location_suppliers").id,
    #             "location_dest_id": picking_type.default_location_dest_id.id,
    #         }),
    #     ],
    # })
    # picking.action_confirm()
    # picking.action_assign()
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "stock_barcode is vendored into addons/."
    )
