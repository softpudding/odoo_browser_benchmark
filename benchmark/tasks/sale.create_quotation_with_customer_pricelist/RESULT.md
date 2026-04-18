# sale.create_quotation_with_customer_pricelist — Result

| Field | Value |
|---|---|
| **Task ID** | sale.create_quotation_with_customer_pricelist |
| **Difficulty** | medium |
| **Tier** | 2 |
| **Oracle** | PASS (F1=1.0) |
| **Browser-Use** | PASS (F1=1.0) |
| **Time limit** | 360s |
| **Step limit** | 200 |

## Workflow under test

Create a new draft sale.order for a seeded customer (`Bench Premium Co`)
whose contact record has a specific pricelist (`VIP 20% Off`) assigned via
`specific_property_product_pricelist`. The SO's `pricelist_id` compute
(`_compute_pricelist_id`, depends on `partner_id`) auto-populates from the
partner. Add a single line for `Bench Standard Widget` qty 5; the
pricelist rule (global 20% off sales price, list price 100.00) drives
`price_unit` to 80.00. Save without confirming — state stays `draft`.

## Calibration

Browser-use solved the task on the first attempt at F1=1.0 in ~88s. The
pricelist auto-applies silently after the customer picker commits, and
browser-use correctly leaves both the header `pricelist_id` and the
line's computed `price_unit` untouched. Postconditions (line qty=5,
price_unit≈80.00, single line, draft state, no stray SOs for the
`Bench Regular Co` distractor) all passed.

## Notes for future tuning

This task is currently too easy for browser-use to fail, but it stays
in the suite as a positive-signal baseline for the pricelist
auto-application pattern. To escalate, consider:

- Add a distractor pricelist (e.g. `VIP 30% Off`) active on the same
  company and instruct the agent to **verify** the auto-applied one is
  the VIP 20% variant — this invites the agent to second-guess and
  manually overwrite.
- Require the agent to ALSO trigger **Update Prices** (the fa-refresh
  button next to the pricelist field) after adding the line, which
  becomes non-trivial to spot.
- Ask the agent to flip the SO to an unrelated partner without a
  pricelist and back to `Bench Premium Co`, requiring the recompute to
  fire cleanly.
