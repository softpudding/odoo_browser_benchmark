Go to **Delivery Methods**.

Create a new delivery method with these exact values:
- **Delivery Method**: `Bench Margin Courier`
- **Provider**: `Based on Rules`
- **Delivery Product**: `Bench Margin Shipping`
- **Fixed Margin**: `6.00`

In the pricing rules, add exactly one rule:
- Condition: `Weight <= 10`
- Delivery Cost: `12.00`
- Variable Cost: `0`

Save the delivery method.

Then go to the **Sales** app and open the draft quotation with customer reference **`MARGIN-DEL-01`**.
Use **Add Shipping** to apply **`Bench Margin Courier`** and then **Confirm** the quotation.

Rules:
- Do not change the customer or the product line.
- Do not create more than one delivery line.
- The computed shipping price must come from the rule plus the fixed margin.
