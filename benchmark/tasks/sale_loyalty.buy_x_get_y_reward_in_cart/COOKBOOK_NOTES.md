# sale_loyalty.buy_x_get_y_reward_in_cart — Odoo 19 quirks

## loyalty.reward: free-product reward lines are NOT price_unit=0

When a `loyalty.reward.reward_type='product'` reward is applied to a cart,
`sale_loyalty.sale.order._get_reward_values_product` creates the reward line
with `price_unit = product.list_price`, `discount = 100`, and the product's
own `tax_ids`. The visible cart total contribution is zero because of the
100% discount — NOT because of `price_unit=0`. Check logic for this pattern
must use `price_subtotal` (post-discount) or `discount == 100`, not
`price_unit`. Distinct from `discount` reward lines, which do carry a
negative `price_unit` directly.

## program_type='promotion' + trigger='auto' auto-applies on /shop/cart

`website_sale_loyalty.Cart.cart` (in `controllers/cart.py`) calls
`order_sudo._auto_apply_rewards()` on every GET of `/shop/cart`. For a
single-reward promotion with `trigger='auto'` whose rule condition is met,
this is sufficient — no button click, no code entry, no wizard. The agent
only has to navigate to `/shop/cart` and the reward line materializes.

The alternative `buy_x_get_y` program type is semantically similar but
imposes a reward-product-qty constraint coupled with `required_points`
matching the consumed qty; `promotion` + product reward is more flexible
for "any 2 widgets -> 1 gadget free" and was the pattern the task spec
explicitly requested.

## Rule editor structure (loyalty.rule form)

- Conditions group: `minimum_qty` (Integer), `minimum_amount` (+ tax mode),
  `product_ids` (m2m tags, the "Among" product list), `product_domain`
  (debug-only), `product_category_id`, `product_tag_id`.
- For `program_type='promotion'` the `minimum_amount` is visible and
  defaults to 50 (per `_program_type_default_values`). Agents should be
  told to leave it at 0 or not touched unless it matters for the task.
- The rule Save button in the inline dialog is "Save & Close" (not just
  "Save"), since rules are one2many children opened in a popup.

## Reward editor structure (loyalty.reward form)

- The `reward_type` selection switches visibility of two groups: Discount
  group (mode/%/applicability radio) vs "Among" product group
  (`reward_product_qty` + `reward_product_id`). For `program_type='buy_x_get_y'`
  the field is readonly (locked to 'product'); for 'promotion' it is
  freely selectable and the UI defaults to 'discount'.
- The cascade means the agent must: (1) click the reward card to open the
  dialog, (2) change Reward type selection to "Free Product" (Odoo
  `o_select_menu`-style dropdown), (3) the "Among" group then becomes
  visible so they can fill `reward_product_id`.
- `required_points` defaults to 1 for the promotion template and doesn't
  need modification for a simple "rule triggers 1 reward" flow.

## JSON-RPC gotcha

- In oracle, `rule_ids` with `product_ids: [[6, 0, [<variant_id>]]]` must
  pass product.product ids (variant), NOT product.template. Similarly,
  `reward_product_id` is a product.product FK. Use
  `product.template.product_variant_id` to resolve.
