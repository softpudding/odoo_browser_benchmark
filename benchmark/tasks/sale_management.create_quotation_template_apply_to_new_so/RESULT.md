# sale_management.create_quotation_template_apply_to_new_so — Result

| Field | Value |
|---|---|
| **Task ID** | sale_management.create_quotation_template_apply_to_new_so |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Oracle** | PASS (F1=1.0) |
| **Browser-Use** | PASS (F1=1.0) |
| **Time limit** | 360s |
| **Step limit** | 200 |

## Workflow under test

Two-stage configuration-then-application flow:

1. **Stage 1 — Configure a reusable Quotation Template.** Navigate
   Sales > Configuration > Quotation Templates > New, name it
   `Bench Starter Pack`, add two product lines
   (`Bench Widget` qty 5, `Bench Gadget` qty 2), save.
2. **Stage 2 — Apply the template to a new Sales Order.** New quotation
   for customer `Bench Test Co`, set `sale_order_template_id` to the
   just-saved template; the `_onchange_sale_order_template_id` hook
   auto-populates the two order lines. Save without confirming
   (state stays `draft`).

## Calibration

Browser-Use single-shot solved the task in 234.7s (well under the 360s
limit). F1=1.0 across both the state-diff track (5/5 expected edits)
and the trace track (0 forbidden writes, 0 required misses).

The Configuration submenu is gated by the
`sale_management.group_sale_order_template` group, but the seed grants
it to admin up-front, so BU did not need to enable the setting. The
nested inline-editable `so_template_line_o2m` list (editable bottom)
did not trip BU — the standard `Add a product` + cell-fill flow worked
cleanly on both the template form and as a read-through on the
auto-populated SO lines.

## Notes for future tuning

The task currently passes BU, which keeps it as a positive-signal
baseline for the `sale.order.template` workflow. To escalate to hard
tier, consider:

- **Add a distractor template** `Bench Legacy Pack` with different
  lines, and require the agent to verify the correct template's lines
  came through.
- **Require toggling the setting** (uncheck `group_sale_order_template`
  in seed so the agent must first open Settings and enable Quotation
  Templates before the menu appears).
- **Require an optional section** line in the template (`is_optional`
  rows have product_uom_qty=0 by default, exposes the
  SectionAndNoteListRenderer section button flow).
- **Add a confirmation mail template** requirement — forces the agent
  to navigate the mail.template domain-filtered autocomplete.
