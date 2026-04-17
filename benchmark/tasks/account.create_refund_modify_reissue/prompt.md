Open the Invoicing (Accounting) app. There are several **posted** customer invoices.

| Customer                | Reference   | Lines                                          |
|-------------------------|-------------|-------------------------------------------------|
| Harborlight Engineering | HLE-MOD-01  | Technical Audit x 8 @ $200, Site Inspection x 3 @ $150 |
| Harborlight Solutions   | HLS-DIST-01 | Technical Audit x 4 @ $200                      |

The invoice for **Harborlight Engineering** (reference `HLE-MOD-01`) needs a quantity correction. Instead of editing it in place, you must use the **Reverse and Create Invoice** workflow so the original is properly reversed and a corrected replacement invoice is created.

Your job:

1. Open the posted invoice with reference `HLE-MOD-01` (customer: Harborlight Engineering).
2. Click the **Credit Note** button.
3. In the reversal wizard:
   - Set the **Reason** to exactly: `Quantity correction for project phase 2`
   - Set the **Reversal date** to **04/10/2026**
   - Click the **"Reverse and Create Invoice"** button (NOT the default "Reverse" button)
4. After the wizard completes, you will be redirected to a new **draft** invoice that is a copy of the original. This is the replacement invoice.
5. On this new draft invoice, change the **Technical Audit** line quantity from **8** to **5**. Do not change the Site Inspection line or any prices.
6. Set the **Invoice Date** to **06/10/2026**.
7. Click **Confirm** to post the new invoice.

After completing these steps:
- The original invoice (HLE-MOD-01) should be fully reversed (payment_state = "reversed")
- A credit note should exist and be posted
- A new invoice should be posted with Technical Audit qty = 5 and Site Inspection qty = 3

**Rules:**
- You MUST click **"Reverse and Create Invoice"** in the wizard, NOT the default "Reverse" button
- Do NOT modify the original invoice directly
- Do NOT change any prices, only the Technical Audit quantity
- Do NOT interact with the Harborlight Solutions invoice (HLS-DIST-01)
- Do NOT delete or cancel any invoices
