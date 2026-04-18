Go to the **Delivery Methods** configuration page.

Create a new delivery method with these exact values:

- **Delivery Method**: `US Harbor Freight`
- **Provider**: `Fixed Price`
- **Delivery Product**: create a new service product named `US Harbor Shipping`
- **Fixed Price**: `15.00`
- **Countries**: `United States` only
- Enable **Free if order amount is above**
- **Amount**: `100.00`

Save the delivery method.

Then go to the **Sales** app and open the draft quotation whose customer reference is **`SHIP-US-100`**.

Add the delivery method **`US Harbor Freight`** to the quotation. Because the untaxed order amount is already at least `100.00`, the shipping line should be added at **0.00**.

Finally, **Confirm** the quotation.

## Rules

- Do not change the customer or any existing quotation line
- Do not edit any other delivery method
- Do not create more than one delivery line on the quotation
- Leave the distractor quotation `SHIP-CA-100` untouched
