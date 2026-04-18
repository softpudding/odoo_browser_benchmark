# Receive a picking via the Barcode app (BLOCKED)

> **Note**: This task is BLOCKED because the `stock_barcode` addon is an
> **Odoo Enterprise** module that is NOT vendored in this Odoo 19
> Community checkout. The Barcode tablet UI at `/odoo/barcode`, the
> Receipts / Internal Transfers / Deliveries client actions, the scan
> buffer, and the "+ quantity" increment buttons all ship with the
> enterprise `stock_barcode` addon (and its optional siblings
> `stock_barcode_barcodelookup`, `stock_barcode_quality_control`, etc.).
>
> What is present in Community:
> - `addons/barcodes/` — low-level keyboard-event handler + nomenclature
>   model. Provides `barcode_scanned` bus events and the hidden `<input>`
>   element that captures Enter-terminated key bursts from USB scanners.
>   It does **NOT** provide a warehouse-receipt scanning UI.
> - `addons/barcodes_gs1_nomenclature/` — GS1 AI parser extension.
> - On `stock.res.config.settings`: `module_stock_barcode =
>   fields.Boolean("Barcode Scanner")` — an upgrade_boolean toggle that,
>   if ticked, asks Odoo to install the (absent) `stock_barcode` module.
>   Ticking it in this checkout fails with "Module not found".
>
> There is no `/odoo/barcode` route, no `stock_barcode.stock_barcode_action_main_menu`
> client action, no `main_menu.js`, no `receipt_line.js`, and no
> `BarcodePickingModel` in this codebase — `grep -rn "stock_barcode"` on
> `addons/` returns only i18n strings and the settings boolean.
>
> The original task intent is preserved below for future re-scoping when
> the enterprise addon is vendored.

You will use the Barcode tablet UI to receive an inbound picking by
scanning the products' barcodes.

## Phase 1 — Open the Barcode app

1. Navigate to `/odoo/barcode` (or Apps menu → Barcode).
2. Click **Operations** → **Receipts**.
3. Open the pre-seeded receipt `R-BENCH-BC-001`.

## Phase 2 — Scan the products

4. For product **Bench Barcode A** (barcode `BENCH-A-001`): scan the
   barcode three times (or tap the `+` button three times, or use the
   long-press quantity shortcut to type `3`).
5. For product **Bench Barcode B** (barcode `BENCH-B-002`): scan the
   barcode three times (same methods available).

## Phase 3 — Validate

6. Tap **Validate**. The confirmation toast should read "The transfer
   has been validated" and the receipt should show `Done` status.

## Rules

- Final state: `stock.picking` with `name = 'R-BENCH-BC-001'` has
  `state == 'done'`.
- Both `stock.move` rows under it have `quantity == 3.0` for Bench
  Barcode A and Bench Barcode B respectively.
- No backorder is created (scanning fulfilled the full demand).
