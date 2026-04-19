ROW: 420
TASK_ID: point_of_sale.apply_fixed_discount_before_payment
DIFFICULTY: hard
SUMMARY: POS: sell Bench POS Item A + Item B (35.00), apply pre-filled 14.29% global discount (~-5.00), pay 30.00 cash
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## point_of_sale.apply_fixed_discount_before_payment

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1=1.0, 19.2s wall clock) |
| **Browser-Use** | PASS (F1=1.0, 111.3s wall clock) |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale, pos_discount (installed on demand) |
| **Workflow** | Open the seeded Bench POS register, click Bench POS Item A (€20.00) and Bench POS Item B (€15.00) to fill the cart (subtotal €35.00), open the ellipsis/Actions popup and click the Discount control button, accept the pre-filled 14.29% in the percentage popup (→ -5.00 EUR discount line), then pay Bench Cash 30.00 and validate. |
| **Capability tested** | Driving the POS kiosk UI to apply a *global* discount (pos_discount module) with a non-default pre-filled percentage (14.29) via the Actions/ellipsis > Discount popup, rather than a per-line discount. |
| **Notes** | pos_discount is NOT in the base snapshot; seed calls `button_immediate_install()`. The Discount button only renders inside the "more" popup (ellipsis) when `props.showRemainingButtons` is true. pos_discount is **percent-only**, never fixed currency — the task simulates "fixed 5 EUR" by seeding `discount_pc=14.29` so 14.29% × 35.00 ≈ 5.00. Oracle uses the JSON-RPC bypass pattern (same style as `split_payment_email_receipt`) because Playwright-driven POS oracles are flaky. Browser-use solved the task first try (PASS, F1=1.0), so this calibrated easier than hard; consider escalating (e.g. split Cash+Bank payment with discount, or non-default percentage distinct from `discount_pc`, or mid-order customer change). |
