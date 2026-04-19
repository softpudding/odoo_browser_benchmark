# website_sale.checkout_portal_apply_coupon_complete — Odoo 19 quirks

## Pre-generated coupon code flow (program_type='coupons')

`program_type='coupons'` is the flavour that LETS the code be entered at
checkout but, unlike `program_type='promo_code'`, the code lives on
individual `loyalty.card` records rather than on the program's rule.
Seed pattern:

```python
program = env["loyalty.program"].create({
    "name": "BENCH10",
    "program_type": "coupons",
    "applies_on": "current",
    "trigger": "with_code",
    "rule_ids": [(5, 0, 0), (0, 0, {
        "minimum_qty": 0,
        "minimum_amount": 0,
        # NO `code` field on the rule — code lives on the card.
    })],
    "reward_ids": [(5, 0, 0), (0, 0, {
        "reward_type": "discount",
        "discount": 10,
        "discount_mode": "percent",
        "discount_applicability": "order",
        "required_points": 1,
        "description": "10% off",
    })],
})
env["loyalty.card"].create({
    "program_id": program.id,
    "code": "BENCH10CODE",
    "points": 1.0,
})
```

`sale.order._try_apply_code("BENCH10CODE")` dispatches to the
`loyalty.card` branch and applies the reward directly — same code
path as gift cards, distinct from promo-code's `loyalty.rule.code`
branch.

## Wire Transfer leaves `sale.order.state='sent'`, NOT `'sale'`

`payment_custom._apply_updates()` transitions the transaction to
`pending`.  Sale's `PaymentTransaction._post_process` override then
runs `action_quotation_sent()` on the linked draft SO — moving it to
`state='sent'` without calling `action_confirm`.  check.py MUST accept
`state in ('sent','sale','done')` for Wire-Transfer-only checkout
flows, otherwise PASS runs will false-negative.

## Delivery line appears on the finalised SO even without choosing a carrier

In the base snapshot, at least one shipping method (`Standard delivery`,
`Delivery_007`) has `is_published=True`.  Going through `/shop/payment`
auto-attaches a delivery line to the SO via the cart's carrier pick,
even when the checkout form never shows a carrier choice.  The
auto-added `sale.order.line` carries `is_delivery=True` (price 0.0 in
the default seed).  check.py has to filter these out of the "unexpected
extra products" assertion:

```python
product_lines = order.order_line.filtered(
    lambda l: not l.is_reward_line and not bool(getattr(l, "is_delivery", False))
)
```

Without this filter, the postcondition fails on a perfectly-completed
checkout run.

## Adding to cart via JSON-RPC keeps the oracle deterministic

The public `Add to cart` `<a id='add_to_cart' class='a-submit'>` button
submits the enclosing `<form>` via Odoo's `a-submit` shim + optional
upsell/variant modal.  Oracle scripts reliably pass through the
process by calling `/shop/cart/add` JSON-RPC directly with the
`product_template_id`, `product_id` (variant) and `quantity` fields
— the same endpoint the button ultimately hits.  Empirically this
halves the wall clock and removes the "optional products" modal
ambiguity on themes that enable it.

## state_spec match_key + entity_key for post-checkout `sale.order`

The pre-task state is EMPTY (no prior SO), so a `match_key` of
`[partner_id, amount_total]` resolves to `(null, 90.0)` in the
observed state diff for a newly-created SO.  `expected_state.json`
MUST mirror that exact tuple — `[null, 90.0]` with `"op": "create"` —
for F1=1.0 on the state-diff track.  Using `["Bench Coupon Item"]` or
any name-based key silently produces F1=0 even when the flow passed.

## `ir.config_parameter['sale.async_emails']=True` is mandatory

Same quirk documented for event_sale Wire-Transfer flows.  Without
this ICP, the missing SMTP provider in the ephemeral bench DB raises
inside `_send_payment_succeeded_for_order_mail`, rolls back the
`/payment/status/poll` cursor, and leaves the SO stuck in `draft`
(no `action_quotation_sent`).  Seed must set this BEFORE the oracle
hits `/shop/payment/validate`.
