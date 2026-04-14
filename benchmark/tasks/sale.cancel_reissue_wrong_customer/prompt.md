Open the Sales app. There is a confirmed sales order for customer **Harbor Retail East** with customer reference `SALE-FIX-12`.

This order was confirmed for the **wrong customer**. It should have been sold to **Harbor Retail West**.

The incorrect confirmed order has these lines:

| Product           | Qty | Unit Price |
|------------------|-----|------------|
| Counter Display  | 4   | 210        |
| Shelf Signage Kit| 7   | 48         |

Because the order is already confirmed, do **not** try to edit the customer on that order.

You must:

1. Cancel the incorrect sales order for **Harbor Retail East**.
2. Create a new quotation for **Harbor Retail West** with the same lines:
   - Counter Display: qty 4, unit price 210
   - Shelf Signage Kit: qty 7, unit price 48
3. Set the new quotation's **Customer Reference** to `SALE-FIX-12-WEST`.
4. Confirm the new quotation.

**Rules:**
- The original order for Harbor Retail East must end in **Cancelled** status
- The new order for Harbor Retail West must end in **Sales Order** status
- Product names, quantities, and unit prices on the new order must match exactly
- Do not delete the cancelled order
