# website_sale.create_gift_card_apply_in_cart — Odoo 19 quirks

## Loyalty: gift_card programs in oracle / seed

- Backend menu for gift cards is `/odoo/gift-cards-ewallet` (action xmlid
  `loyalty.loyalty_program_gift_ewallet_action`). Domain hides everything
  except `program_type in ('gift_card', 'ewallet')`.
- The cleanest way to mint a fully-configured gift_card program from
  JSON-RPC is `loyalty.program.create_from_template('gift_card')` followed
  by a rename. It auto-populates the matching rule (`reward_point_mode='money'`,
  `product_ids=loyalty.gift_card_product_50`, `reward_point_split=True`)
  and the per-point order discount reward — hand-rolling the
  `rule_ids` / `reward_ids` tuples in `create()` works but is brittle when
  the defaults change between minor versions.
- `loyalty.card.create({program_id, points, partner_id: false})` mints an
  anonymous gift card without going through `loyalty.generate.wizard`. Pass
  `context={loyalty_no_mail: True, action_no_send_mail: True}` to suppress
  the demo "send creation email" side effect.
- Default Odoo demo program `loyalty.gift_card_program` (display name
  "Gift Cards") ships pre-installed when sale_loyalty is in the base.
  Distractor checks must look it up by name AND program_type, since the
  word "Gift Cards" also appears as a label elsewhere.

## Applying a gift-card code at the cart

- `sale.order._try_apply_code(code)` accepts both `loyalty.rule` codes
  (promo programs) and `loyalty.card` codes (gift cards / coupons): when no
  rule matches, it falls through to a `loyalty.card` lookup. So the same
  `/shop/pricelist?r=/shop/cart` form POST that applies a promo code also
  works for a gift card code — no special endpoint needed.
- The webshop renders `loyalty.card.code` as a copy-clipboard span on the
  gift-card form view (`portal_visible=True` makes it appear under the
  smart button list). Browser-use can read it from a list-view text cell
  even without clicking the copy widget.

## Calibration note

- Despite the two-stage workflow (back-office wizard chain + portal
  redemption), browser-use solved this on a single run with no postcondition
  failures. The Generate Gift Cards wizard only has 3 fields above the fold
  (qty / value / description) and they're plainly labeled, so the
  "wizard with non-default values" failure pattern doesn't fire here. To
  re-harden, either add a constraint that requires editing a non-default
  trigger product on the rule, or shift the difficulty to a multi-card
  generate (qty>1 with "Selected Customers" mode) where each row needs a
  partner.
