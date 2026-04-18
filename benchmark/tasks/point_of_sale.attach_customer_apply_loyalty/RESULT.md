ROW: 333
TASK_ID: point_of_sale.attach_customer_apply_loyalty
DIFFICULTY: hard
SUMMARY: POS: add Bench POS Item x3 (EUR 60), attach Loyal Larry, redeem 10% loyalty-funded reward (-6), pay 54 cash, validate
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## point_of_sale.attach_customer_apply_loyalty

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale, loyalty, pos_loyalty (auto-installed via sale_loyalty in base) |
| **Workflow** | Open the seeded Bench Loyalty POS register, add Bench POS Item x3 (EUR 60.00), click Customer on the action pad and pick Loyal Larry, open the Rewards popup and redeem the '10% on your order' loyalty-funded reward for 50 points (-EUR 6.00), then pay Bench Loyalty Cash 54.00 and validate. |
| **Capability tested** | POS kiosk UI: attach a seeded customer mid-sale, open the Rewards popup, redeem a discount reward funded by the customer's loyalty.card point balance, pay cash, validate. Cross-module loyalty + POS. |
| **Notes** | pos_loyalty auto-installs when both point_of_sale and loyalty are present; both are already in the base snapshot via sale_loyalty, so no module install needed in seed. Seed creates a loyalty.program (program_type='loyalty', applies_on='both', reward=10% order discount at 50 points) scoped to the new POS config via pos_config_ids, and mints a loyalty.card for Loyal Larry with 100 points (enough for exactly one redemption). Oracle uses the JSON-RPC call_kw bypass pattern (same as split_payment_email_receipt) because the POS UI is timing-sensitive. Calibration: browser-use solved this on the first 91-second run (F1=1.0) — the Rewards popup and customer autocomplete are both well labelled. POS loyalty redemption does NOT add a strong failure mode. To re-harden this area we would need to escalate, e.g. (1) require a non-default reward (multiple rewards listed, pick the middle one), (2) combine with a per-line discount or pricelist override, or (3) require closing the session and reconciling cash with a deliberate difference. |
