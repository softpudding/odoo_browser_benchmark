You are in the Odoo 19 **Purchase** app, logged in as **Administrator**.

You must do a full 3-way match workflow: create a new Request for Quotation,
confirm it, partially receive the goods (with a backorder), and post a vendor
bill for the quantities actually received.

Two storable products are already in the catalog: **Bench PO Item A**
(price 20.00) and **Bench PO Item B** (price 40.00). The vendor
**Bench Supply Co** already exists.

## Part A — Create and confirm the RFQ

1. From the Purchase app, click **New** to open a blank Request for
   Quotation.
2. Set **Vendor** to `Bench Supply Co`.
3. On the **Products** tab, add exactly these **two** lines:

   | Product            | Quantity | Unit Price |
   |--------------------|----------|------------|
   | Bench PO Item A    | 10       | 20.00      |
   | Bench PO Item B    | 5        | 40.00      |

4. Click **Confirm Order** (the status bar primary button) to convert the
   RFQ into a purchase order (the status becomes **Purchase Order**).

## Part B — Receive partial quantity (A = 7, B = 5) with a backorder

5. Click the **Receipt** smart button in the PO header to open the
   auto-generated vendor receipt (state **Ready**).
6. On the **Operations** tab of the receipt, locate the `Bench PO Item A`
   row and change the **Quantity** (Done) cell from `10` to **7**. Leave
   the `Bench PO Item B` row at the already-filled **5**.
7. Click **Validate** in the receipt's status bar.
8. A **Create Backorder?** dialog appears asking how to handle the 3
   remaining units of Item A. Click **Create Backorder** (the primary
   left-hand button) — do NOT click **No Backorder**.
9. The original receipt flips to state **Done**. A fresh backorder
   picking is created for the 3 remaining Item A units — leave it alone.

## Part C — Post a vendor bill for the received quantities

10. Navigate to the **Purchase Orders** list (Purchase → Orders →
    Purchase Orders, or the URL `/odoo/purchase-orders`).
11. In the Purchase Orders list, **select the checkbox** on the row for
    your newly created PO (vendor **Bench Supply Co**).
12. Click the **Create Bills** button that appears in the list header
    after selection. A draft vendor bill opens, pre-populated with the
    PO lines, **each line already defaulted to the received quantity**
    (A = 7, B = 5).
13. Set the **Bill Reference** to `BSC-BILL-3WM`.
14. Click **Confirm** (the status bar primary button) to post the bill.
    Its state should change from Draft to **Posted**.

## Rules

- You MUST create **exactly two** PO lines. Do not leave a phantom empty
  third line — tab through the editor only as far as needed.
- You MUST lower the Done quantity on **Item A** from 10 to **7** before
  clicking Validate. Do not validate with the default 10.
- You MUST click **Create Backorder** in the dialog, not No Backorder.
- The vendor bill MUST keep the auto-filled quantities (A = 7, B = 5) —
  do NOT edit them back to 10 / 5 on the bill.
- You MUST set the Bill Reference exactly to `BSC-BILL-3WM` and then
  post the bill with **Confirm**.
- Do NOT cancel the PO, cancel the receipt, or delete the backorder.
- Do NOT register a payment on the bill — Confirm (Post) is the final
  step.
