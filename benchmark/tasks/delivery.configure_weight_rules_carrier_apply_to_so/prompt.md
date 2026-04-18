Go to the **Delivery Methods** configuration page (Inventory → Configuration → Shipping Methods).

Create a new delivery method with these exact values:

- **Delivery Method**: `Bench Weight Courier`
- **Provider**: `Based on Rules`
- **Delivery Product**: create a new product named `Bench Shipping Charge` (use the create-and-edit shortcut, then save the product) — or pick an existing product with that exact name if one is offered.

In the **Pricing** tab, add **two** pricing rules:

1. Condition `Weight  <=  5`, Delivery Cost `8.00` (no per-unit factor — set the second cost field to `0`).
2. Condition `Weight  <=  20`, Delivery Cost `18.00` (no per-unit factor — set the second cost field to `0`).

Save the delivery method.

Then go to the **Sales** app and open the draft quotation identified by customer reference **`S-BENCH-DEL-001`** (it has a single line of `Bench Weighted Widget` × 1 with weight 3 kg).

Click **Add shipping**, pick **`Bench Weight Courier`**, then click **Add** in the dialog. The shipping price must be computed automatically from the weight rules (3 kg ≤ 5 kg ⇒ 8.00).

Finally, **Confirm** the quotation.

## Rules

- Do not change the customer or any existing quotation line.
- Do not edit any other delivery method.
- Do not create more than one delivery line on the quotation.
- The first pricing rule (≤ 5 kg) must come before the second (≤ 20 kg) in the list so the right one matches first.
