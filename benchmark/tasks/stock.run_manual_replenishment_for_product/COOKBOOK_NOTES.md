# Cookbook notes — stock.run_manual_replenishment_for_product

## Calibration confirmation: Replenishment dashboard + per-row Order is NOT hard

Row 491 corroborates row 286 `inventory.run_replenishment_from_dashboard`
(medium, PASS/PASS): a plain `Inventory > Operations > Replenishment`
navigation followed by a per-row fa-truck Order click does NOT trap
browser-use. BU solved in 9 steps / 71.5s / F1=1.0. The path is too
deterministic and the button too discoverable for a hard-tier score.

Key signals:

- The Replenishment menu item is plainly labelled under Operations; BU
  used the top menu dropdown without misclicks.
- The default search facets (`filter_to_reorder + filter_not_snoozed +
  trigger='manual'`) narrow a fresh DB to exactly one matching row, so
  no disambiguation click is required.
- The per-row Order button is NOT checkbox-gated — BU skipped the
  dropdown bulk-action trap entirely.
- The prompt's "Do not click Automate" warning removed the only
  adjacent mis-click trap (fa-refresh icon at the same x-position).

## Hard-band escalation ladder for replenishment tasks

To push a replenishment task into the hard band (≤40% BU pass):

1. **Distractor rows** — seed 2+ additional orderpoints with similar
   "Bench *" product names and `qty_to_order > 0`. BU must
   disambiguate by row text before clicking.
2. **Non-default qty** — require the agent to EDIT the `qty_to_order`
   cell (to e.g. 25) before clicking Order. Writing to
   `qty_to_order_manual` via inline edit + Tab + Order is a two-step
   gesture BU often leaves uncommitted.
3. **Forced bulk-action path** — prompt the agent to use the top
   `Order` dropdown (bulk menu) which is gated by `hasSelectedRecords`.
   Requires ticking the row checkbox first — BU frequently skips the
   checkbox and clicks the dropdown, which is a no-op.
4. **Multi-vendor sellers** — add a second `product.supplierinfo` at a
   different (cheaper/more expensive) price; the agent must reorder
   the seller sequence on the product BEFORE replenishing, or the
   generated PO will go to the wrong vendor.
5. **Closed-loop confirm** — extend the task with a subsequent Confirm
   Order step on the generated RFQ (cross-module round-trip — BU's
   standard failure mode after triggering a notification is to stop).

## Seed recipe: Replenishment + manual orderpoint + seller_ids

Reusable pattern for future replenishment tasks:

```python
vendor = env["res.partner"].create({
    "name": "Bench X Vendor",
    "email": "orders@...",
    "company_type": "company",
    "supplier_rank": 1,
})

tmpl = env["product.template"].create({
    "name": "Bench X Item",
    "type": "consu",
    "is_storable": True,
    "tracking": "none",
    "list_price": 75.0,
    "standard_price": 50.0,
    "purchase_ok": True,
    "seller_ids": [(0, 0, {
        "partner_id": vendor.id,
        "price": 50.0,
        "min_qty": 0.0,
        "delay": 1,
    })],
})

wh = env["stock.warehouse"].search([], limit=1)
op = env["stock.warehouse.orderpoint"].create({
    "product_id": tmpl.product_variant_id.id,
    "location_id": wh.lot_stock_id.id,
    "warehouse_id": wh.id,
    "trigger": "manual",                 # keeps the Automate icon visible
    "product_min_qty": 5.0,
    "product_max_qty": 20.0,
})
op._compute_qty()
op._compute_qty_to_order_computed()
op._compute_qty_to_order()
```

On-hand=0 + min=5 + max=20 yields `qty_to_order=20` → the per-row
fa-truck Order button is visible via
`invisible="qty_to_order &lt;= 0.0"`.

## action_replenish quirks

1. **Orderpoint auto-deletion**: The tail of
   `stock.warehouse.orderpoint.action_replenish` (line 365 in
   `addons/stock/models/stock_orderpoint.py`) does:
   ```python
   self.filtered(
       lambda o: o.create_uid.id == SUPERUSER_ID
                 and o.qty_to_order <= 0.0
                 and o.trigger == 'manual'
   ).unlink()
   ```
   Seed runs via `odoo shell` as uid=1 (= `SUPERUSER_ID`), so the
   seeded manual orderpoint WILL be auto-deleted after a successful
   replenish. check.py MUST tolerate `0 or 1 remaining orderpoint` —
   strict `== 1` would falsely flag every successful run.

2. **`action_replenish` return value** is a `display_notification`
   client action, NOT a form redirect. The notification's `links[0]`
   points to `/odoo/action-purchase.action_rfq_form/<po_id>`. The new
   PO is in `state='draft'` by default.

3. **`_run_buy` line pricing**: `stock.rule._run_buy` →
   `_prepare_purchase_order_line_from_procurement` stamps the
   product's `_select_seller().price` onto `product_qty` and
   `price_unit`. With `seller_ids[0].price=50.0` in seed, the new PO
   line gets `price_unit=50.0` deterministically — no need to stamp
   the standard_price.

## entity_key normalization rules observed (re-confirmed)

- `purchase.order` match_key=`[partner_id]` → `["Bench Replenish Vendor"]`
  (Many2one → display name).
- `purchase.order.line` match_key=`[product_id, order_id]` →
  `["Bench Replenish Item", null]`. The `order_id` Many2one normalizes
  to `null` (distinct from `sale.order.line.order_id` which normalizes
  to the SO name). Matches row 450 observation.
- `stock.warehouse.orderpoint` excluded from state_spec because
  post-replenish auto-deletion produces a spurious `unlink` edit on
  happy-path runs; check.py asserts the rule-integrity invariant
  directly instead.

## Menu-path differentiation (critical)

| Menu | action xml-id | list view | Order/Automate buttons |
|---|---|---|---|
| Operations → Replenishment | `stock.action_replenishment` (server action, path=`replenishment`) → `stock.action_orderpoint_replenish` | `view_warehouse_orderpoint_tree_editable` | **YES** (`.o_replenish_buttons` column rendered) |
| Operations → Reordering Rules | `stock.action_orderpoint` | `view_warehouse_orderpoint_tree_editable_show_trigger` (primary-mode inherit) | NO (same base view but the inherit leaves buttons visible too — empirically the row icons render, BUT the default filter `search_default_trigger='auto'` hides manual rules) |
| Product form → Reordering Rules smart button | `product.product.action_view_orderpoints` → `stock.action_orderpoint` | same | NO filter context forces single-product view |

Oracles and prompts MUST use `/odoo/replenishment` (the server-action
path) — `/odoo/action-stock.action_orderpoint_replenish` also works.
`/odoo/action-stock.action_orderpoint` does NOT apply the
`filter_to_reorder` default and therefore the row appears only when
the agent clears/adjusts facets.
