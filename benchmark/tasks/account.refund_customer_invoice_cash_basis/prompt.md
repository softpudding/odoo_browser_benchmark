Open the Invoicing (Accounting) app. There is one **posted** customer invoice:

| Customer       | Reference          | Total    |
|----------------|--------------------|----------|
| Bench Ref Co   | BENCH-REFUND-001   | 500.00   |

The invoice has a single line:

| Product                 | Qty | Unit Price | Subtotal |
|-------------------------|-----|------------|----------|
| Bench Refund Service    | 1   | 500.00     | 500.00   |

The customer operates on a **cash basis** and has requested a **partial refund of 200.00** for this invoice (not a full refund of 500.00, and not a re-issue). You need to issue a partial credit note for `200.00` linked to this invoice.

Your job:

1. Open the posted invoice with reference `BENCH-REFUND-001` (customer: Bench Ref Co).
2. Click the **Credit Note** button in the header status bar. (This opens the `Reverse` wizard — on customer invoices its statusbar button is labeled "Credit Note".)
3. In the `Reverse` wizard:
   - Set the **Reason** to exactly: `Cash basis partial refund`
   - Leave the **Reversal date** at today's default value (do NOT change it).
   - Leave the **Journal** at its default value.
   - Click the primary **Reverse** button (this creates an editable draft credit note). Do NOT click **Reverse and Create Invoice** — that button creates a second draft invoice and is the wrong flow.
4. You are now viewing the draft credit note (a `Customer Credit Note`). It has **one** line, `Bench Refund Service`, with quantity `1` and unit price `500.00`, copied from the source invoice.
   Edit the line so the refund total is `200.00`:
   - Change the `Bench Refund Service` **Unit Price** from `500.00` to `200.00`.
   - Keep the quantity at `1`.
   - Do NOT delete the line, do NOT add new lines.
5. Verify the draft credit note total now reads `200.00`.
6. Click **Confirm** in the header to post the credit note.

**Rules:**
- Only create a credit note for `BENCH-REFUND-001`.
- The posted credit note must contain exactly one product line: `Bench Refund Service` with quantity `1` and unit price `200.00`.
- The credit note total must be `200.00` (NOT `500.00`).
- The source invoice `BENCH-REFUND-001` must remain `Posted` (do NOT reset it to draft or cancel it).
- You must click the **Reverse** primary button in the wizard — NOT `Reverse and Create Invoice`.
- Do NOT leave the credit note in draft state — it must be posted.
