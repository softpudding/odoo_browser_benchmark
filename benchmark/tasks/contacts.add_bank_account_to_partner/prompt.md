# Add a bank account to a contact

You are in the Odoo 19 **Contacts** app logged in as **Administrator**.

The supplier **Benchmark IBAN Supplier Ltd** has sent you a new bank
account number for payments. Record it on their contact record.

## What to do

1. Open the **Contacts** app.
2. Find and open the contact **Benchmark IBAN Supplier Ltd**.
3. Go to the **Invoicing** tab on the contact form.
4. In the **Bank Accounts** field, type the IBAN
   `GB82 WEST 1234 5698 7654 32` into the add input. Confirm the
   **Create …** suggestion in the autocomplete dropdown, then
   Save the bank record in the dialog that appears.
5. Save the contact.

## Rules

- Exactly **one** bank account should exist on this partner after the
  task.
- The IBAN must be the exact value above (spaces optional — Odoo
  normalises them).
- Do **not** modify any other field on the contact (name, email, etc.).
- Do **not** create additional contacts or bank accounts on other
  partners.
