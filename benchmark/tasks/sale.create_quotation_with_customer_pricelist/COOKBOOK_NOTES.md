# Cookbook notes from sale.create_quotation_with_customer_pricelist

## `product.group_product_pricelist` is a feature flag, not just a visibility flag

`product.pricelist._get_partner_pricelist_multi` short-circuits to an
empty result (no pricelist for any partner, regardless of their
`specific_property_product_pricelist`) if the
`product.group_product_pricelist` group is **not** enabled on
`SUPERUSER_ID` (see `_is_feature_enabled` → `res.users.browse(SUPERUSER_ID)._has_group(...)`).

Implication for seeds that want a partner's pricelist to auto-apply on a
new sale.order:
1. Grant `product.group_product_pricelist` to **both** `base.user_admin`
   **and** `base.user_root`. Writing only to admin is not enough — the
   compute consults SUPERUSER before it even looks at the partner.
2. After granting, write
   `partner.specific_property_product_pricelist = <pricelist>.id` (the
   actual company-dependent storage field). Setting the public
   `property_product_pricelist` at create-time is unreliable (the
   inverse method is guarded by `partner.country_id` fallback logic).

Working pattern:

```python
pricelist_group = env.ref("product.group_product_pricelist")
pricelist_group.sudo().write({"user_ids": [
    (4, env.ref("base.user_admin").id),
    (4, env.ref("base.user_root").id),
]})

partner = env["res.partner"].create({"name": "Bench Premium Co"})
partner.with_company(env.company).write({
    "specific_property_product_pricelist": pricelist.id,
})
assert partner.property_product_pricelist.id == pricelist.id
```

## `sale.order.pricelist_id` display_name includes the currency suffix

A pricelist named `"VIP 20% Off"` surfaces as `"VIP 20% Off (USD)"` in
the state diff (`display_name` appends `(<currency_code>)`). Expected
state must include the suffix, or the match will fail.

## `sol_o2m` widget: line product field is `product_template_id`

On the SO form's Order Lines tab, the list view uses the `sol_o2m`
widget whose inline cell name is `product_template_id`, NOT
`product_id`. Oracles that call `set_o2m_many2one(page, 0,
"product_id", ...)` time out waiting for a missing cell. Use
`product_template_id` in `set_o2m_many2one`.

## `has_active_pricelist` is per-order but based on a global search

`sale.order.has_active_pricelist` is computed from
`product.pricelist.search([('active', '=', True)])` — as long as one
active pricelist exists for the company (or no company), the
Pricelist header field is visible. No need to create a per-order
pricelist.
