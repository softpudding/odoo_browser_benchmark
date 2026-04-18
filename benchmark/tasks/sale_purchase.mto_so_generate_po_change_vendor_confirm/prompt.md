Open the **Sales** app.

There is a confirmed Sales Order with customer reference **`S-BENCH-MTO-001`**
for customer **Bench MTO Customer** containing one line:
**Bench MTO Widget** quantity **5** at unit price 80.00.

The product is configured with the **Replenish on Order (MTO) + Buy** routes
and has two vendors configured:

- **Acme Supply Co** (default / first vendor, price 50.00)
- **Brook Trading Ltd** (alternative vendor, price 40.00)

Because of the MTO route, confirming the SO has already auto-generated a
draft Request for Quotation (RFQ) for the default vendor **Acme Supply Co**.

Your procurement manager wants to source from **Brook Trading Ltd** instead
(they offered better terms this month). Do the following:

1. Open the SO `S-BENCH-MTO-001`.
2. Click the **Purchase** smart button at the top of the SO. This navigates
   to the auto-generated draft RFQ for Acme Supply Co.
3. On the generated RFQ:
   - Change the **Vendor** from **Acme Supply Co** to
     **Brook Trading Ltd**. The Bench MTO Widget line's **Unit Price** should
     recompute automatically to **40.00** (Brook Trading Ltd's vendor
     pricelist). Leave the quantity at **5**.
   - Save the form.
4. Click **Confirm Order** to convert the RFQ into a confirmed Purchase
   Order (state becomes "Purchase Order").

**Final state required:**
- The auto-generated Purchase Order linked to SO `S-BENCH-MTO-001` has
  **Vendor = Brook Trading Ltd**, **state = Purchase Order**, and one line
  with **5 × Bench MTO Widget at 40.00** unit price.
- SO `S-BENCH-MTO-001` remains in state "Sales Order" and still shows
  exactly **1** Purchase smart-button count (no second PO created).
- No RFQ for Acme Supply Co exists (it was replaced, not duplicated).

**Rules:**
- Do NOT create a brand new Purchase Order from scratch — you must edit the
  auto-generated RFQ that the SO created.
- Do NOT cancel the SO.
- Do NOT change the customer, the product, or the ordered quantity (5).
- Do NOT change the unit price manually — simply changing the vendor to
  Brook Trading Ltd must trigger the recompute to 40.00.
- Do NOT validate any receipt / transfer — the task ends once the PO is in
  "Purchase Order" state.
