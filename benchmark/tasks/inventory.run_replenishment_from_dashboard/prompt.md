Open the **Inventory** app.

In the top menu, open **Operations → Replenishment**. (The Replenishment dashboard lives under the Operations menu in Inventory.)

The list shows products that need to be replenished. Find the row for the product **"Bench Reorder Widget"** (it should show a **To Order** quantity of **28** with vendor **"Bench Supplies Ltd"** in its supply chain).

On that row, click the **Order** button (the truck icon at the right of the row, tooltip "Order"). This launches the replenishment for the chosen quantity and creates a draft purchase order with vendor "Bench Supplies Ltd" for **28** units of "Bench Reorder Widget".

If a confirmation/wizard dialog appears asking for the quantity, keep the default of **28** and confirm.

When you are done, the system will have a single draft `purchase.order` for vendor "Bench Supplies Ltd" with one line for "Bench Reorder Widget", quantity **28**.

**Rules:**
- Run replenishment only for **"Bench Reorder Widget"**.
- Do NOT change the Min/Max values on the reordering rule.
- Do NOT confirm the resulting purchase order — leave it in draft.
- Do NOT create extra purchase orders or RFQs manually.
- Do NOT modify the product master record.
