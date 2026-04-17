# Merge two duplicate Globex Corporation contacts

You are in the Odoo 19 **Contacts** app logged in as **Administrator**.

Four company contacts with "Globex" in the name exist:

| Name                  | Email                | VAT            | Phone           |
|-----------------------|----------------------|----------------|-----------------|
| Globex Corporation    | contact@globex-old.com | (none)       | +1 415 555 0188 |
| Globex Corporation    | billing@globex.io    | BE0477472701   | (none)          |
| Globex plc            | info@globex-plc.co.uk| GB123456789    | +44 20 7946 0958|
| Globex Labs           | research@globex-labs.io| (none)       | +1 650 555 0147 |

The two **Globex Corporation** records are the same real-world company and
must be merged. **Globex plc** and **Globex Labs** are separate companies —
do not merge them.

## What to do

1. Open **Contacts** and switch to **List view**.
2. Filter / search so you can see all four Globex records.
3. Select **only** the two records named exactly **"Globex Corporation"**
   (tick their checkboxes). Do not include Globex plc or Globex Labs.
4. Open the **Actions** menu (⚙ / "Actions") and click **Merge**.
5. In the merge wizard, set the **Destination Contact** to the Globex
   Corporation that has VAT number **BE0477472701** (it's the record with
   email `billing@globex.io`). This record should be the master.
6. Click **Merge Contacts**.
7. Confirm any dialog that appears.

## Rules

- Merge exactly the two "Globex Corporation" records — no more, no fewer.
- **Globex plc** and **Globex Labs** must remain untouched in the system.
- The surviving merged record must keep the VAT **BE0477472701**.
- Do not archive, rename, or delete any record instead of merging.
- Do not create any new contact.
