You are on the Odoo 19 CRM app pipeline view. You need to create a new opportunity, then create a linked quotation from it and send the quotation by email.

## Step 1 — Create the opportunity

1. Create a new opportunity in the CRM pipeline.
2. Fill in the following fields:
   - **Organization**: `Pinnacle Logistics Group`
   - **Contact Name**: `Derek Voss`
   - **Email**: `derek.voss@pinnacle-logistics.example.com`
   - **Expected Revenue**: `45000`
3. Move the opportunity to the **Qualified** stage (drag it or use the status bar).
4. Save the opportunity.

## Step 2 — Create a linked quotation

5. On the saved opportunity, click the **New Quotation** button to create a quotation linked to this opportunity.
6. On the new quotation form, fill in:

| Product                      | Qty | Unit Price |
|------------------------------|-----|------------|
| Warehouse Management Module  | 3   | 8500       |
| Implementation Service       | 1   | 12000      |

7. Set the **Customer Reference** field to `PLG-Q2-2026`.
8. Set the **Expiration** date to **07/01/2026** (July 1, 2026).
9. Save the quotation.

## Step 3 — Send the quotation by email

10. Click **Send by Email** on the quotation.
11. In the email compose wizard:
    - Set the **Subject** to exactly: `Pinnacle Logistics - Warehouse Management Proposal`
    - Click **Send**.

## Rules

- Do **not** change product prices from 8,500 and 12,000.
- Do **not** add extra product lines beyond the two specified.
- The quotation must remain linked to the opportunity (created via "New Quotation" from the opportunity).
- Do **not** confirm the quotation — only send it by email.
- Do **not** modify or delete the existing opportunity named "Pinnacle Logistics Solutions - Fleet GPS".
