Open the Invoicing (Accounting) app. There is a **posted** customer invoice for **Redwood Consulting** with reference `SURG-EDIT-01`.

This invoice has four lines:

| Product          | Quantity | Unit Price | Discount |
|------------------|----------|------------|----------|
| Strategy Report  | 1        | 3,000      | 0%       |
| Market Analysis  | 2        | 1,500      | 10%      |
| Risk Assessment  | 1        | 2,200      | 5%       |
| Compliance Audit | 3        | 800        | 0%       |

The **Risk Assessment** line has an error: the quantity should be **2**, not 1.

Your job:

1. **Reset the invoice to Draft** (use the "Reset to Draft" button).
2. Edit the **Risk Assessment** line and change its quantity from 1 to **2**.
3. **Do not change anything else** — all other lines must keep their exact quantities, prices, and discounts.
4. **Post** the invoice again.

**Rules:**
- Only the Risk Assessment quantity changes (1 -> 2)
- Strategy Report, Market Analysis, and Compliance Audit lines must remain exactly as they are
- The invoice must end in Posted status
- Do not create a new invoice or credit note
