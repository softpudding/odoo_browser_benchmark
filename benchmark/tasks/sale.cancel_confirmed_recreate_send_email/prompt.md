Open the Sales app. There is a confirmed sales order with customer reference `BENCH-CANCEL-RESEND` for customer **Ironwood Distribution**.

This order needs to be cancelled and replaced with a new quotation for a different customer.

The original confirmed order has these lines:

| Product                | Qty | Unit Price |
|------------------------|-----|------------|
| Heavy-Duty Shelf Unit  | 12  | 145.00     |
| Packing Tape Industrial| 150 | 3.50       |

You must:

1. Navigate to **Sales → Orders** and remove any **"My Quotations"** filter so you can see all orders.
2. Find the confirmed sales order `BENCH-CANCEL-RESEND` for **Ironwood Distribution**.
3. Click **Cancel** to cancel this order.
4. Confirm the cancellation in the dialog that appears.
5. Create a **new quotation** with the following details:
   - Customer: **Clearwater Supply Co** (a different customer)
   - Add the same products but with **updated quantities**:

   | Product                | Qty | Unit Price |
   |------------------------|-----|------------|
   | Heavy-Duty Shelf Unit  | 8   | 145.00     |
   | Packing Tape Industrial| 200 | 3.50       |

   - Set **Customer Reference** to `CWS-REPLACE-01`
   - Set **Expiration Date** to **07/15/2026**
6. Save the quotation.
7. Click **Send by Email** (or **Send**) on the quotation.
8. In the email compose wizard:
   - Set the **Subject** to: `Clearwater Supply - Replacement Order Proposal`
   - Click **Send**

**Rules:**
- Do NOT modify or delete the cancelled order
- The new quotation must have EXACTLY 2 product lines (no extra blank lines)
- Product names, quantities, and unit prices must match exactly as specified above
- The cancelled order must remain in **Cancelled** status
- The new quotation must end in **Quotation Sent** status after the email is sent
