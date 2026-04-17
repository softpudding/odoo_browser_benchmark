# Resolve a duplicate partner by transferring fields then archiving

You are in the Odoo 19 **Contacts** app logged in as **Administrator**.
Two company contacts share the same name: **Ridgeway Global Services**.
Each record has part of the correct data; you need to consolidate
them.

Their distinguishing reference numbers are on the **Sales & Purchase**
tab under **Reference**:

- `RGS-PRIMARY` — this is the **primary** record to KEEP. It has the
  correct **street** and **city** but is MISSING its **phone** and
  **email**.
- `RGS-DUPLICATE` — this is the **duplicate** record to ARCHIVE. It
  has the correct **phone** and **email** but no address.

## What to do

1. Open the **Contacts** app.
2. Locate the record with Reference **RGS-DUPLICATE**. Copy its
   **Phone** and **Email** values (`+1 415 555 0188` and
   `contact@ridgeway-global.example`) — you will need them in a
   moment.
3. Open the record with Reference **RGS-PRIMARY** and set:
   - **Phone** → `+1 415 555 0188`
   - **Email** → `contact@ridgeway-global.example`

   Save the form.
4. Go back to the **RGS-DUPLICATE** record.
5. Open the **Actions** menu (the ⚙ gear icon at the top of the form)
   and choose **Archive**. Do NOT delete the record — it must remain
   in the database as archived (active=False).

After you finish:

- **RGS-PRIMARY** should have the correct address (kept from before),
  plus phone `+1 415 555 0188` and email
  `contact@ridgeway-global.example`.
- **RGS-DUPLICATE** should be **archived** (toggle its filter to
  include "Archived" to verify) but still exist in the database.

## Rules

- Do **not** delete either partner — the duplicate must be archived,
  not deleted.
- Do **not** modify any partners other than these two.
- Do **not** change the **Reference** field on either record.
- Do **not** change the street, city, or name on the primary record.
