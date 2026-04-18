"""Postcondition checks for stock.scrap_specific_serial_unit."""


PRODUCT_NAME = "Bench Sensor Module"
TARGET_SERIAL = "SN-A002"
KEEP_SERIALS = ["SN-A001", "SN-A003"]


def check(env):
    failures = []

    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if not products:
        return [f"Product '{PRODUCT_NAME}' is missing"]
    product = products[0]

    scraps = env["stock.scrap"].search([("product_id", "=", product.id)])
    if len(scraps) != 1:
        return [
            f"Expected exactly 1 stock.scrap for '{PRODUCT_NAME}', "
            f"found {len(scraps)}"
        ]

    scrap = scraps[0]
    if scrap.state != "done":
        failures.append(
            f"Scrap state is '{scrap.state}', expected 'done' (agent did not "
            f"click Validate)"
        )
    if abs(scrap.scrap_qty - 1.0) > 0.01:
        failures.append(
            f"Scrap quantity is {scrap.scrap_qty}, expected 1.0"
        )
    if not scrap.lot_id:
        failures.append(
            "Scrap has no Lot/Serial selected — agent did not pick a serial "
            "(product is serial-tracked, so a specific lot is required)"
        )
    elif scrap.lot_id.name != TARGET_SERIAL:
        failures.append(
            f"Scrap lot is '{scrap.lot_id.name}', expected '{TARGET_SERIAL}' "
            f"— agent picked the wrong serial"
        )

    target_lot = env["stock.lot"].search(
        [("name", "=", TARGET_SERIAL), ("product_id", "=", product.id)],
        limit=1,
    )
    if target_lot:
        target_qty = sum(
            env["stock.quant"].search([
                ("lot_id", "=", target_lot.id),
                ("location_id.usage", "=", "internal"),
            ]).mapped("quantity")
        )
        if target_qty > 0.01:
            failures.append(
                f"{TARGET_SERIAL} still has on-hand qty {target_qty}, "
                f"expected 0 after scrap"
            )

    for keep_name in KEEP_SERIALS:
        keep_lot = env["stock.lot"].search(
            [("name", "=", keep_name), ("product_id", "=", product.id)],
            limit=1,
        )
        if not keep_lot:
            failures.append(f"Serial '{keep_name}' was deleted unexpectedly")
            continue
        keep_qty = sum(
            env["stock.quant"].search([
                ("lot_id", "=", keep_lot.id),
                ("location_id.usage", "=", "internal"),
            ]).mapped("quantity")
        )
        if keep_qty < 0.99:
            failures.append(
                f"Serial '{keep_name}' on-hand qty is {keep_qty}, expected to "
                f"remain at 1 (agent scrapped the wrong serial)"
            )

    return failures
