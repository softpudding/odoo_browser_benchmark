# Schedule a service activity on a fleet vehicle

You are in the Odoo 19 **Fleet** app logged in as **Administrator**.

Vehicle **SVC-8812** is due for its annual inspection. You need to
schedule an activity on the vehicle record so the operations team sees
it as a follow-up.

## What to do

1. Open the **Fleet** app and navigate to the Vehicles list.
2. Open the vehicle with licence plate **SVC-8812**.
3. On the vehicle form, open the **chatter** (right side / bottom) and
   click the **Activities** / **⏰ Schedule activity** button.
4. In the activity dialog, fill in:
   - **Activity Type**: `To Do`  (plain to-do; pick the default one
     called "To-Do" if multiple exist)
   - **Due Date**: `June 30, 2026`
   - **Summary**: `Annual inspection and service`
5. Click **Schedule** (not **Mark as done**). The activity should now be
   listed on the vehicle.

## Rules

- The activity must be attached to the vehicle record **SVC-8812** only.
- The due date must be exactly **2026-06-30**.
- The summary must be the exact text above.
- Do **not** immediately mark the activity as done — it must remain
  open/pending.
- Do **not** modify any other fields on the vehicle.
