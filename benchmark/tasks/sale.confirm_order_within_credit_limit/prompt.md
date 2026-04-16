Open the Sales app. There is already one draft quotation for a similar customer.

If a default **My Quotations** filter is active, clear it first.

Create a **brand new quotation** for **Atlas Field Systems**.
Do **not** edit the existing quotation for **Atlas Fleet Services**.

Atlas Field Systems already has **$1,700** due and a credit limit of **$4,000**, so the new quotation must stay within the remaining **$2,300** before it can be confirmed.

For the new Atlas Field Systems quotation:

- set **Customer Reference** to `CREDIT-OPS-09`
- set **Expiration** to `2026-05-22`
- add `Field Router Kit` at unit price `400`
- add `On-site Commissioning` at unit price `1100`

Sales requested `Field Router Kit` quantity `4` and `On-site Commissioning` quantity `1`, but before you confirm the order you must reduce **only** `Field Router Kit` to the highest whole quantity that still fits within the remaining credit.

Your job:

1. Create the new quotation for **Atlas Field Systems**.
2. Add the two product lines.
3. Keep `On-site Commissioning` at quantity `1`.
4. Reduce only `Field Router Kit` as needed to fit the credit limit.
5. Save the quotation.
6. Click **Send**.
7. In the quotation email dialog:
   - keep `billing@atlas-field.example.com` as a recipient
   - add `creditdesk@atlas-field.example.com` as an additional recipient
   - set **Subject** to exactly `Atlas credit-cleared quotation`
   - set the message body to exactly `Please review the adjusted quotation within the remaining credit allowance.`
8. Send the quotation email.
9. Confirm the quotation.

**Rules:**
- Do not change any unit price, discount, or product
- Do not remove the billing recipient
- Do not add any recipient other than `creditdesk@atlas-field.example.com`
- Do not edit the quotation for **Atlas Fleet Services**
- The final Atlas Field Systems quotation must be confirmed
