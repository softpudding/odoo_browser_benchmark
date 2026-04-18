ROW: 355
TASK_ID: sale_loyalty.buy_x_get_y_reward_in_cart
DIFFICULTY: hard
SUMMARY: Configure a Buy-2-Widgets-Get-1-Gadget promotion (rule qty_min=2 on Bench Widget, product reward of 1 Bench Gadget) and verify the free reward line auto-applies on /shop/cart.
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0
CALIBRATION: easier

DETAIL_SECTION:
## sale_loyalty.buy_x_get_y_reward_in_cart

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Sales, Loyalty (sale_loyalty + website_sale_loyalty) |
| **Workflow** | Back-office: `/odoo/discount-loyalty`, create program "Buy 2 Widgets Get 1 Gadget" with `program_type='promotion'`, `trigger='auto'`. Edit the default rule: set Minimum Quantity=2 and add `Bench Widget` to Among-products. Edit the default reward: switch Reward type to `Free Product`, pick `Bench Gadget` as the product, set Quantity rewarded=1 and Description="Free Bench Gadget". Save. Public portal: navigate `/shop/cart` (already has 2 Bench Widgets) and the free Bench Gadget reward line appears automatically via `_auto_apply_rewards`. |
| **Capability tested** | Buy-X-Get-Y promotion configuration using the loyalty cascading dropdown widgets (reward type switch from default discount to Free Product flips the "Among" group of the reward form), combined with the auto-apply side-effect of `website_sale_loyalty.Cart.cart` on /shop/cart. |
| **Notes** | Calibration FAILED: BU solved this on a single headed run (139s, 46 API calls, 16 steps). BU successfully navigated both cascading dropdowns (opened Rule editor, typed minimum qty + product autocomplete; opened Reward editor, switched Reward type selection dropdown to "Free Product", autocompleted Bench Gadget). The "price_unit=0" phrasing in the task spec was misleading — free-product reward lines carry `price_unit=list_price` with `discount=100`, so `price_subtotal=0` is the correct check (updated check.py accordingly). Task is well-formed and verifies the full flow; keep as tier-3 despite BU pass since the reward dropdown switch is a genuine cascade test and BU sometimes fails it under load. |
