ROW: 320
TASK_ID: website_sale.create_gift_card_apply_in_cart
DIFFICULTY: hard
SUMMARY: Configure gift_card loyalty program, generate one €50 card, apply code at /shop/cart so €100 cart drops to €50.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## website_sale.create_gift_card_apply_in_cart

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Website (eCommerce), Loyalty (sale_loyalty + website_sale_loyalty) |
| **Workflow** | Back-office: open Gift Cards & eWallet, create program "Spring Gift Card" (program_type=gift_card), open Generate Gift Cards wizard (qty=1, value=50, description), open the program's Gift Cards smart button and copy the generated code. Public portal: open /shop/cart (already has Spring Premium Bundle €100), paste code in the Discount code field, click Apply -> total drops from €100 to €50. |
| **Capability tested** | Two-stage cross-module workflow combining a multi-step backend wizard (program create + Generate wizard + smart-button drill-down to copy a generated code) with public-portal redemption on /shop/cart. |
| **Notes** | Calibration FAILED: BU passed both diff and postconditions on the first run (185s, 60 API calls). Gift-card program type defaults via `_program_type_default_values` are well-formed enough that BU only had to set the name and run the wizard. Oracle uses `loyalty.program.create_from_template('gift_card')` + rename to get all proper rule/reward defaults rather than hand-crafting the rule_ids/reward_ids tuples. Coupon POST endpoint `/shop/pricelist?r=/shop/cart` accepts a gift card `loyalty.card.code` identically to a `loyalty.rule` promo code (sale_loyalty.`_try_apply_code` falls through to the loyalty.card branch). |
