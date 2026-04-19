Open the Invoicing (Accounting) app. There is one **posted miscellaneous journal entry** with two balanced lines:

| Reference       | Journal                     | Line 1                                  | Line 2                                   |
|-----------------|-----------------------------|-----------------------------------------|------------------------------------------|
| BENCH-GL-REV    | Miscellaneous Operations    | Account `Rent` — **Debit 100.00**       | Account `Bank` — **Credit 100.00**       |

The accountant wants this entry **reversed** (a mirrored journal entry posted today that swaps the debits and credits, leaving both entries linked). You must find it through the Miscellaneous Journal Items report (not through the regular Journal Entries list) and reverse it.

Your job:

1. In the Invoicing/Accounting top menu, go to **Accounting → Miscellaneous Operations** (the Miscellaneous journal items report — rows are grouped by journal entry).
2. The list is grouped. Expand the group whose entry reference is `BENCH-GL-REV` by clicking the group-header row. You will see its two journal items (Rent debit 100, Bank credit 100).
3. Click the entry reference (`BENCH-GL-REV`) to open the **`account.move` form** for the entry.
4. On the entry form header, click the **Reverse Entry** statusbar button. This is a header button on posted misc entries (it is NOT the `Credit Note` button, which only appears on customer/vendor invoices, and it is NOT in the cog Actions menu for form view). Clicking it opens the `Reverse Journal Entry` wizard (`account.move.reversal`).
5. In the wizard:
   - Leave **Journal** at its default value (the same Miscellaneous journal).
   - Leave **Reversal date** at today's default date (do not change it).
6. Click the primary **Reverse** button in the wizard footer (NOT **Discard**). This creates and **automatically posts** a new `account.move` with `move_type='entry'`, `reversed_entry_id=<BENCH-GL-REV id>`, `state='posted'`, and two journal items with the debit/credit swapped (Rent credit 100, Bank debit 100).

**Rules:**
- The original entry `BENCH-GL-REV` must remain `Posted` (do NOT reset it to draft or cancel it).
- Exactly **one** new `account.move` with `reversed_entry_id` equal to the `BENCH-GL-REV` entry id must exist, with `move_type='entry'` and `state='posted'`.
- The reversal entry's two journal items must swap the debit/credit compared to the source (Rent: credit 100, debit 0; Bank: debit 100, credit 0).
- Do NOT create any other account.move, credit note, or payment.
- Do NOT click **Reverse and Create Invoice** (that button is hidden for `move_type='entry'` anyway).
- Use the **Reverse Entry** header button, not cog Actions.
