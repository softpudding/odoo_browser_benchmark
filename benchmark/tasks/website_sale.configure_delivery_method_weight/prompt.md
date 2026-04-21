You are on the backend **Inventory / Sales > Configuration > Delivery Methods** list (`/odoo/delivery-methods`).

Create a brand-new weight-based shipping method with two pricing tiers and publish it on the website.

## Step 1 - Create the delivery method

From the **Delivery Methods** list, click **New** and fill in:

- **Delivery Method** (name at the top of the form): `Bench Weight Shipping`
- **Provider**: `Based on Rules` (so `delivery_type` stores `base_on_rule`). Do **not** leave it on the default `Fixed Price`.
- **Delivery Product**: leave the auto-selected service product that Odoo fills in (don't blank it out; do not create a new one).
- Publish the method on the website by clicking the **globe / Published** stat button (so `is_published` becomes `true`).

## Step 2 - Add the weight-based pricing rules

On the form, open the **Pricing** tab (it only appears for the **Based on Rules** provider). Add **exactly two** rules to the Pricing list:

**Rule 1 - up to 5 kg**

- **Condition**: `Weight` `<=` `5.00`
- **Delivery Cost**: `10.00` + `0.00` * Weight (set the fixed part to `10.00`, leave the per-unit multiplier at `0.00`)

**Rule 2 - above 5 kg**

- **Condition**: `Weight` `>` `5.00`
- **Delivery Cost**: `20.00` + `0.00` * Weight (set the fixed part to `20.00`, leave the per-unit multiplier at `0.00`)

Both rules should end up with `variable_factor = Weight` (the default). **Save** the delivery method.

## Rules

- The delivery-method name must be **exactly** `Bench Weight Shipping` (no trailing space, same capitalisation).
- The provider must be **Based on Rules** (`delivery_type='base_on_rule'`) — not Fixed Price.
- The method must be **published** (`is_published=True`).
- There must be **exactly two** `delivery.price.rule` rows linked to this carrier, with the thresholds and base prices above.
- Do **not** create any other delivery method, do **not** edit or archive existing delivery methods, do **not** change the seeded `Bench Delivery Product`.
- Do **not** set the per-unit multiplier to `10` or `20` on either rule (that value is a per-unit multiplier; the fixed fee belongs in the first part of the **Delivery Cost** formula).
