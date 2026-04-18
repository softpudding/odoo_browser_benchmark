# contacts.merge_three_duplicates_keep_email — RESULT

| Field | Value |
|---|---|
| ROW | 319 |
| TASK_ID | contacts.merge_three_duplicates_keep_email |
| DIFFICULTY | hard |
| SUMMARY | Merge 3 "John Doe" duplicate contacts (1 empty / 1 email-only / 1 phone-only) via Actions→Merge from list view, picking the email-bearing record as Destination Contact so the surviving ref is BENCH-JD-02. A 4th "John Doe" under Acme Corp is a decoy that must NOT be merged. |
| ORACLE | PASS |
| BROWSER_USE | FAIL (421.5s, picked wrong master BENCH-JD-01 instead of BENCH-JD-02) |
| F1 | 0.0 |
| CALIBRATION | matches hard |

## DETAIL_SECTION

## contacts.merge_three_duplicates_keep_email

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Contacts |
| **Workflow** | Seed four res.partner rows named "John Doe" (refs BENCH-JD-01 empty, JD-02 email=john@x.com, JD-03 phone=555-1234) plus a decoy JD-DECOY under Acme Corp. In /odoo/contacts list view, select only the three refs without a parent company, Actions > Merge, set Destination Contact = the JD with email john@x.com (BENCH-JD-02) via the partner_show_db_id-tagged dropdown, click Merge Contacts. Final survivor must be BENCH-JD-02 with email=john@x.com AND phone=555-1234. |
| **Capability tested** | 3-way merge with explicit master selection. Agent must read the prompt's master-selection rule and pick the non-default dst_partner_id, and must NOT include the Acme Corp decoy in the selection. |
| **Notes** | Well-calibrated hard. BU completed the Actions>Merge flow and called `action_merge`, but left the default dst_partner_id (BENCH-JD-01, the first partner by id) instead of switching to the email-bearing BENCH-JD-02 — exactly the non-default wizard trap. The merge did preserve email+phone, but check.py asserts the survivor ref so the wrong master fails. Task also verifies the decoy (JD-DECOY under Acme Corp) is untouched. Note: the base Odoo 19 merge wizard does NOT have per-field source tabs; field preservation is deterministic via `_update_values` (src_partners, dst last) — since the 3 duplicates have disjoint email/phone, any master produces the same email+phone on the survivor, so the distinguishing difficulty is picking the right *survivor ref* and excluding the decoy. |
