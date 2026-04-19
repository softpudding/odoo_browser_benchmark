# Bulk-archive three lost CRM leads

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

Three leads were marked as lost last week but never archived. The sales
manager has asked you to archive all three of them in one bulk action
from the **Leads** list so they stop cluttering the active pipeline.

Targets (all three must be archived):

| Name            | Contact         | Email                          |
|-----------------|-----------------|--------------------------------|
| Bench Lost 1    | Alice Lost      | alice.bench@example.com        |
| Bench Lost 2    | Bob Lost        | bob.bench@example.com          |
| Bench Lost 3    | Carol Lost      | carol.bench@example.com        |

A fourth active lead, **Bench Keep 4**, must remain active and must NOT
be archived.

## What to do

1. From the CRM top menu, open **Leads -> Leads** (the Leads list, not
   the Pipeline / Opportunities board).
2. Switch to **List view** if the page opens in Kanban so each row shows
   a checkbox in its leftmost cell.
3. **Clear any default filters** (for example the `To Process` or
   `Unassigned` chip) so all four seeded `Bench ...` leads are visible.
   You may type `Bench Lost` in the search box and press Enter to narrow
   the list to just the three targets.
4. Tick the row checkboxes on **exactly these three leads**:
   - `Bench Lost 1`
   - `Bench Lost 2`
   - `Bench Lost 3`

   Do NOT tick `Bench Keep 4`.
5. With the three rows selected, open the **Actions** menu (the gear /
   cog dropdown that appears in the control panel once at least one row
   is selected) and click **Archive**.
6. If a confirmation dialog appears, confirm it.

## Expected end state

- The three target leads `Bench Lost 1`, `Bench Lost 2`, and
  `Bench Lost 3` each have `active = False` (archived).
- `Bench Keep 4` remains active (`active = True`) and untouched.

## Rules

- Use the **list-view Actions menu** (multi-select bulk action) to
  archive — do NOT open each lead one at a time and use the form's
  Archive / Lost button. Archiving from inside individual forms does
  not satisfy the bulk-action requirement.
- Select **exactly 3** leads — no more, no fewer. Including
  `Bench Keep 4` in the selection is a failure.
- Do not delete any lead. Use **Archive** (not Delete / Unlink).
- Do not rename, duplicate, convert, or otherwise modify any lead.
- Do not create any new lead.
