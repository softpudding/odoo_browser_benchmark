Open the Invoicing (Accounting) app. There are two **posted** customer invoices for similar companies.

| Customer              | Reference      |
|-----------------------|----------------|
| Beacon Offshore Ltd.  | `SEND-APR-17`  |
| Beacon Onshore Ltd.   | `SEND-APR-18`  |

Work only on the invoice for **Beacon Offshore Ltd.** with reference `SEND-APR-17`.

Before you send the invoice, create a new contact in the **Contacts** app:

- **Name:** `Beacon Offshore Approvals`
- **Company:** `Beacon Offshore Ltd.`
- **Job Position:** `Finance Controller`
- **Email:** `approvals@beacon-offshore.example.com`

1. Create the new contact linked to **Beacon Offshore Ltd.**
2. Return to the Invoicing app and open the posted invoice with reference `SEND-APR-17`.
3. Click **Send**.
4. In the send dialog:
   - keep `finance@beacon-offshore.example.com` as a recipient
   - add `approvals@beacon-offshore.example.com` as an additional recipient
   - set **Subject** to exactly `Beacon Offshore invoice review`
   - set the message body to exactly `Please review the April service invoice and route any approval comments through the offshore billing desk.`
5. Click **Send**.

**Rules:**
- Only send invoice `SEND-APR-17`
- Do not remove the finance recipient
- Do not add any recipient other than `approvals@beacon-offshore.example.com`
- Create the new contact under **Beacon Offshore Ltd.**, not **Beacon Onshore Ltd.**
- Do not change the invoice lines, totals, date, or customer
- Do not send or modify invoice `SEND-APR-18`
