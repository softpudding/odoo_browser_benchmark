# Merge three duplicate 'John Doe' contacts, keep email and phone

You are in the Odoo 19 **Contacts** app logged in as **Administrator**.

Four contacts named **"John Doe"** exist in the system:

| Internal Reference | Name       | Email          | Phone      | Company (parent) |
|--------------------|------------|----------------|------------|------------------|
| BENCH-JD-01        | John Doe   | (none)         | (none)     | (none)           |
| BENCH-JD-02        | John Doe   | john@x.com     | (none)     | (none)           |
| BENCH-JD-03        | John Doe   | (none)         | 555-1234   | (none)           |
| BENCH-JD-DECOY     | John Doe   | jdoe@acme.com  | (none)     | Acme Corp        |

The first three (BENCH-JD-01, BENCH-JD-02, BENCH-JD-03) are the **same
real-world person** and must be merged into a single record. The fourth
(BENCH-JD-DECOY, whose parent company is **Acme Corp**) is a different
John Doe and must **NOT** be merged.

## What to do

1. Open **Contacts** and switch to **List view** (so checkboxes appear on
   each row).
2. Filter/search so you can see all four "John Doe" records.
3. Tick the checkboxes on **only the three duplicates** — the three
   "John Doe" rows that have **no parent company** shown. Do **NOT** tick
   the "John Doe" whose Company column shows **Acme Corp**.
4. Open the **Actions** menu (the ⚙/"Actions" dropdown at the top of the
   list) and click **Merge**.
5. A merge wizard opens listing the three selected partners. Set the
   **Destination Contact** (dst_partner_id) to the "John Doe" whose email
   is **john@x.com** — this is the record that should survive. (You can
   disambiguate in the wizard's dropdown by the trailing database id; the
   wizard lists all three partners with their ids so you can pick the
   right one.)
6. Click **Merge Contacts**.
7. Close any confirmation dialog that appears.

## Expected end state

- Exactly **one** contact named "John Doe" (not the Acme Corp one) remains
  after the merge.
- That surviving record carries **both** `email = john@x.com` **and**
  `phone = 555-1234`. (The merge combines non-empty values from all three
  duplicates onto the destination record.)
- The other two duplicate records (the one with no email/phone, and the
  phone-only one) are gone.
- The **Acme Corp / John Doe** distractor is untouched: still active,
  still has email `jdoe@acme.com`, still a child of Acme Corp.

## Rules

- Merge exactly the three "John Doe" duplicates — no more, no fewer.
- The Acme Corp "John Doe" must remain active and unchanged.
- The surviving merged record must have BOTH email `john@x.com` AND phone
  `555-1234`. Picking the wrong master loses one of these.
- Do not archive, rename, or delete any contact instead of merging.
- Do not create any new contact.
