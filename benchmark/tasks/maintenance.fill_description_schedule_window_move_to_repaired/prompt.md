Go to the **Maintenance** app (URL `/odoo/maintenance`).

Find and open the existing **In Progress** maintenance request titled **`Replace Conveyor Drive Belt`** (on equipment **`Conveyor CV-22`**).

On that request form, do **all three** of the following:

1. **Fill the Description** field (the `Internal Notes` textbox in the form body) with exactly:

   ```
   Belt cracked at the splice. Replaced with new spare from inventory. Tensioner re-aligned and idler bearings greased.
   ```

2. **Set the schedule window** so that a 2-hour repair duration is logged:
   - **Scheduled Date** (start): `04/15/2026 09:00:00`
   - **End Date**: `04/15/2026 11:00:00`

3. **Move the request to the `Repaired` stage** by clicking the **Repaired** stage in the status bar at the top of the form (the breadcrumb-style stage selector). Confirm any dialog if prompted.

## Rules

- Do **NOT** archive or delete the request.
- Do **NOT** modify the request title, equipment, or assigned technician.
- Do **NOT** create a new maintenance request.
- The Description must contain the exact text above (a single paragraph).
- The final stage must be **Repaired** (a stage where the request is considered done).
- Do **NOT** click "Set as Blocked" or "Set as Ready for next stage" on the kanban state — only move the stage forward via the status bar.
