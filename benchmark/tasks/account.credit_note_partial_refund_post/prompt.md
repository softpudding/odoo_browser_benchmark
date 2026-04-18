Open the Invoicing (Accounting) app. There is one **posted** customer invoice:

| Customer     | Reference      | Total   |
|--------------|----------------|---------|
| Bench AR Co  | INV/BENCH/001  | 500.00  |

The invoice has two lines:

| Product      | Qty | Unit Price | Subtotal |
|--------------|-----|------------|----------|
| Bench Item A | 4   | 100.00     | 400.00   |
| Bench Item B | 2   | 50.00      | 100.00   |

The customer is disputing the `Bench Item A` quantity and wants a refund for **2 of the 4 units of Item A** (nothing else). You need to issue a partial credit note for `200.00`.

Your job:

1. Open the posted invoice with reference `INV/BENCH/001` (customer: Bench AR Co).
2. Click the **Reverse** button in the header. (On invoices this is labeled **Credit Note**.)
3. In the `Reverse` wizard:
   - Set the **Reason** to exactly: `Wrong qty`
   - Leave the **Reversal date** as today's date (do not change it).
   - Leave the **Journal** at its default value.
   - Click **Reverse** (the primary button — this creates a draft credit note you can edit. Do NOT click **Reverse and Create Invoice**).
4. You are now viewing the draft credit note (a `Customer Credit Note`). It will have **both** lines copied from the source invoice.
   Edit it so that only `Bench Item A` remains, with quantity `2`:
   - Change `Bench Item A` quantity from `4` to `2`.
   - **Delete the `Bench Item B` line entirely** (click the trash icon on that row).
5. Verify the total on the credit note reads `200.00`.
6. Click **Confirm** in the header to post the credit note.

**Rules:**
- Only create a credit note for `INV/BENCH/001`.
- The posted credit note must contain exactly one product line: `Bench Item A` with quantity `2`.
- The credit note total must be `200.00`.
- The source invoice `INV/BENCH/001` must remain `Posted` (do NOT reset it to draft or cancel it).
- You must click the **Reverse** primary button in the wizard (this creates the editable draft credit note). Do NOT click **Reverse and Create Invoice**.
