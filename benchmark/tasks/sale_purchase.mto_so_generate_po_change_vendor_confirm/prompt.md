Navigate to the **Sales** app and open the **Quotations** list.

Find the quotation (state = Quotation / draft) with customer reference
**`S-BENCH-MTO-001`** for customer **Harbor MTO Buyer**. The quotation has
1 line: **Harbor MTO Gadget** quantity **8** at **150.00** per unit (taxes
cleared).

The product **Harbor MTO Gadget** is configured with the **Buy** +
**Replenish on Order (MTO)** routes and has **two** approved vendors on its
purchase tab:

- **Alpha Precision Parts** (primary seller, seed default)
- **Orion Component Works** (alternative seller)

Because of the MTO configuration, confirming the sales order automatically
generates a draft Request for Quotation (RFQ) for the primary vendor
(**Alpha Precision Parts**).

Complete the workflow as follows:

1. Open the quotation `S-BENCH-MTO-001`.
2. Click **Confirm** to confirm the sales order. Its state must change from
   "Quotation" to "Sales Order" and a Purchase smart button should appear
   at the top of the form.
3. Click the **Purchase** smart button on the confirmed SO to navigate to
   the auto-generated draft RFQ.
4. On that RFQ (state = RFQ / draft, vendor = Alpha Precision Parts):
   - Change the **Vendor** from **Alpha Precision Parts** to
     **Orion Component Works** (use the vendor field autocomplete; pick the
     existing partner, do not quick-create a new contact).
   - Keep the line product, quantity (8), and unit price exactly as they
     are — do NOT edit the order line.
5. Click **Confirm Order** on the RFQ to convert it into a confirmed
   Purchase Order. Its state must become **"Purchase Order"**.

**Final state required:**
- Sales Order `S-BENCH-MTO-001` remains confirmed (state = "Sales Order")
  with its single line intact (Harbor MTO Gadget, qty 8, price 150.00).
- The auto-generated Purchase Order (origin references the SO) has
  **vendor = Orion Component Works** and state = **"Purchase Order"**.
- No purchase order for vendor **Alpha Precision Parts** referencing this
  SO remains in any state (the vendor swap must edit the existing RFQ, not
  create a second one).

**Rules:**
- Do NOT cancel, delete, or reset the SO or the RFQ.
- Do NOT create a new purchase order from scratch — edit the RFQ that the
  MTO configuration generated automatically.
- Do NOT change the customer, the product, the ordered quantity (8), or
  the unit price on either the SO line or the PO line.
- Do NOT create a new vendor contact — pick **Orion Component Works** from
  the vendor autocomplete (it already exists).
