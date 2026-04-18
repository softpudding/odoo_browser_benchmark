# point_of_sale.attach_customer_apply_loyalty — Odoo 19 quirks

## pos_loyalty is auto-installed when loyalty + point_of_sale are present

`pos_loyalty/__manifest__.py` has `auto_install: True` and depends on both
`loyalty` and `point_of_sale`. The benchmark base snapshot already includes
`sale_loyalty` (which pulls `loyalty`) and `point_of_sale`, so `pos_loyalty`
is activated automatically — no `button_immediate_install()` needed in seed.

## Seeding a points-funded discount loyalty program for POS

The minimal program for "redeem N points for a discount reward in POS" is:

```python
env["loyalty.program"].create({
    "name": "Bench Loyalty Program",
    "program_type": "loyalty",          # nominative cards, tracks points
    "trigger": "auto",                  # customer attach triggers the rule
    "applies_on": "both",               # current + future (redeem + earn)
    "pos_ok": True,
    "pos_config_ids": [(6, 0, [config.id])],  # scope to the test POS
    "rule_ids": [(5, 0, 0), (0, 0, {
        "minimum_qty": 1,
        "reward_point_mode": "order",   # 1 point per order (earn-rule)
        "reward_point_amount": 1,
    })],
    "reward_ids": [(5, 0, 0), (0, 0, {
        "reward_type": "discount",
        "discount": 10,
        "discount_mode": "percent",
        "discount_applicability": "order",
        "required_points": 50,          # 50-point redemption
        "description": "10% on your order",
    })],
})
```

Then mint the card outside the UI:

```python
env["loyalty.card"].with_context(
    loyalty_no_mail=True, action_no_send_mail=True
).create({
    "program_id": program.id,
    "partner_id": partner.id,
    "points": 100.0,
})
```

`loyalty_no_mail=True` suppresses the welcome-email side effect that would
otherwise show up in `state_diff.json`.

## Earn-rule inflates the post-redemption balance by ~1

If the loyalty program has a non-zero `reward_point_amount` on its rule,
the POS order also *earns* points on the same order the reward is redeemed
on. With our seed (1 point per order, 50-point redemption), Larry starts at
100 and ends at 51, not 50. `check.py` must accept the ~1-point earn bonus
or zero out `reward_point_amount` (but then the UI-level "you earned N
points" toast is missing, which subtly changes the agent's perception).

## Oracle: JSON-RPC bypass + reward line structure

The POS UI is flaky (see `point_of_sale.add_item_apply_global_discount_pay_cash`
cookbook). The call_kw bypass pattern also works for loyalty-funded reward
lines — add an extra line dict with `is_reward_line: true`, `reward_id`,
`coupon_id`, `reward_identifier_code`, `points_cost`, and write the
loyalty.card's points down by the reward cost in the same transaction:

```js
[0, 0, {
  name: '10% on your order',
  product_id: productRes[0].id,
  price_unit: -6.0, qty: 1,
  tax_ids: [[6, 0, []]],
  price_subtotal: -6.0, price_subtotal_incl: -6.0,
  is_reward_line: true,
  reward_id: rewardRes[0].id,
  coupon_id: cardRes[0].id,
  reward_identifier_code: 'LOYALTY-10',
  points_cost: 50,
}]
```

Then `pos.make.payment.create` + `.check` to close the order.

## Browser-use solves this task easily — NOT a hard pattern

Single-shot BU run: 91s, PASS, F1=1.0. The Rewards popup and customer
autocomplete in the POS kiosk UI are plainly labelled, and the reward
description "10% on your order" is unambiguous. Combining customer-attach,
Rewards redemption, and cash pay does NOT stack into a hard task. Consider
escalation: multiple rewards in the popup (pick non-first), a non-default
redemption quantity, or a deliberate cash reconciliation mismatch.
