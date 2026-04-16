Open the Invoicing (Accounting) app. There are two **posted** customer invoices for similar companies.

| Customer              | Reference      |
|-----------------------|----------------|
| Beacon Offshore Ltd.  | `SEND-APR-17`  |
| Beacon Onshore Ltd.   | `SEND-APR-18`  |

Work only on the invoice for **Beacon Offshore Ltd.** with reference `SEND-APR-17`.

1. Open the posted invoice with reference `SEND-APR-17`.
2. Click **Send**.
3. In the send dialog:
   - keep `finance@beacon-offshore.example.com` as a recipient
   - add `controller@beacon-offshore.example.com` as an additional recipient
   - set **Subject** to exactly `Beacon Offshore invoice review`
   - set the message body to exactly `Please review the April service invoice and reply with any approval notes by Friday.`
4. Click **Send**.

**Rules:**
- Only send invoice `SEND-APR-17`
- Do not remove the finance recipient
- Do not add any recipient other than `controller@beacon-offshore.example.com`
- Do not change the invoice lines, totals, date, or customer
- Do not send or modify invoice `SEND-APR-18`
