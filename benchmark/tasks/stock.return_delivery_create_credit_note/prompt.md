Go to the **Inventory** app.

Navigate to **Delivery Orders** — either from the overview card or via
**Operations > Transfers** filtered to Delivery Orders.

Find the validated (Done) delivery with source document **"BENCH-DEL-RET"**
for customer **Cascade Dynamics**. It contains two products:

- **Industrial Fan Unit** — delivered qty: 10
- **Rubber Gasket Set** — delivered qty: 20

Perform a **partial return** of this delivery:

1. Open the delivery order.
2. Click the **Return** button.
3. In the Return wizard that appears:
   - Set the return quantity for **Industrial Fan Unit** to **4**.
   - Keep the **Rubber Gasket Set** return quantity at **0** (do NOT return it).
   - Click **Return**.
4. On the newly created return picking:
   - Set the **Done** quantity for **Industrial Fan Unit** to **4**.
   - Click **Validate** to complete the return.

Now navigate back to the original **Sales Order** (use breadcrumbs, smart
buttons, or any other navigation method) that created this delivery.

5. On the Sales Order, click the **Invoices** smart button (or navigate to
   the posted invoice).
6. On the posted invoice, click the **Credit Note** button.
7. In the Credit Note wizard:
   - Set **Reason** to: `Partial return - defective units`
   - Set **Credit Note Date** (Reversal date) to: **06/08/2026** (June 8, 2026)
   - Click **Reverse** (or the equivalent button) to create the credit note.
8. On the draft credit note that opens, click **Confirm** to post it.

**Rules:**
- Return ONLY **4 units** of **Industrial Fan Unit**. Do NOT return the Rubber Gasket Set.
- Do NOT modify the original delivery order in any other way.
- Do NOT touch any other delivery orders (there is a distractor delivery for "Cascade Design").
- The credit note must be posted (confirmed), not left in draft.
