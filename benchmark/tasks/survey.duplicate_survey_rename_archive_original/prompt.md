Go to the **Surveys** app (URL `/odoo/surveys`).

Find the existing survey titled **`Quarterly Pulse Q1 Template`** and open it.

Do BOTH of the following on this template survey:

1. **Duplicate** the survey:
   - Click the **cog / Actions (⚙)** menu in the form's top control panel.
   - Click **Duplicate**.
   - Odoo opens the duplicate in form view. Its title will be `Quarterly Pulse Q1 Template (copy)`.
   - **Rename** the title to exactly: `Quarterly Pulse Q2 2026`
   - **Save** the renamed copy (cloud icon or Save action).

2. **Archive the original** template:
   - Navigate back to the original `Quarterly Pulse Q1 Template` (use the breadcrumbs / list view).
   - On its form, open the **cog / Actions (⚙)** menu and click **Archive**.
   - Confirm any archive dialog if prompted.
   - The original should now be archived (active = False) and disappear from the default Surveys list.

## Rules

- Do **NOT** rename, delete, or archive the new copy `Quarterly Pulse Q2 2026`. Only the original is archived.
- Do **NOT** modify any questions on either survey.
- Do **NOT** create a third survey from scratch — you must use **Duplicate** on the original.
- The renamed copy must have the EXACT title `Quarterly Pulse Q2 2026` (no `(copy)` suffix and no trailing whitespace).
- The original must keep its title `Quarterly Pulse Q1 Template` — only its archived state changes.
