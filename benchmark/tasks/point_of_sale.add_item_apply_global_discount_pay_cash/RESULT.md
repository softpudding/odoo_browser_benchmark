ROW: 309
TASK_ID: point_of_sale.add_item_apply_global_discount_pay_cash
DIFFICULTY: hard
SUMMARY: POS: sell 2x Bench POS Widget, apply 15% global discount via Discount control button, pay 34.00 cash
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## point_of_sale.add_item_apply_global_discount_pay_cash

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale, pos_discount (installed on demand) |
| **Workflow** | Open the seeded Bench Test Store POS register, add Bench POS Widget x2 (EUR 40.00), click the Actions ellipsis to reveal the Discount control button, enter 15 in the percentage popup (EUR -6.00), then pay Bench Cash 34.00 and validate. |
| **Capability tested** | Driving the POS kiosk UI to apply a *global* discount (pos_discount module) via the ellipsis > Discount popup, rather than a per-line discount. |
| **Notes** | pos_discount is NOT in the base snapshot; seed calls `button_immediate_install()`. The Discount button only renders inside the "more" popup (ellipsis) when `props.showRemainingButtons` is true — keep that in mind for oracle/agent workflows. Oracle uses the JSON-RPC bypass pattern (same style as split_payment_email_receipt) because Playwright-driven POS oracles proved flaky on this machine. Browser-use solved the task first try (PASS, F1=1.0), so this calibrated easier than hard; consider escalating (e.g. mixed payment split with discount, or a non-default discount percentage not equal to `discount_pc`). |
