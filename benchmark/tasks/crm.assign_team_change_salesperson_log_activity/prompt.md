# Reassign opportunity to Channel team and schedule a Call

You are in the Odoo 19 **CRM** app logged in as **Administrator**.

The opportunity **Bench Big Deal** has just been handed off from Direct Sales
to the Channel team, with **Sara Sales** as the new owner. You also need to
log a Discovery Call so the new owner has a follow-up on the calendar.

## What to do

1. Open the **CRM** app's pipeline.
2. Find the opportunity **Bench Big Deal** and open its form.
3. Change the **Salesperson** from **Mitchell Admin** to **Sara Sales** (the
   field with the small avatar near the top right of the form).
4. Open the **Contacts** notebook tab (at the bottom of the form, after
   "Notes"). Inside the **Ownership** group, change the **Sales Team** from
   **Direct Sales** to **Channel**.
5. **Save** the form (cloud icon or breadcrumb save).
6. In the chatter at the bottom, click **Activities** (or the **Activity**
   button) and schedule a new activity with:
   - **Activity Type**: Call
   - **Due Date**: 06/10/2026 (June 10, 2026)
   - **Summary**: `Discovery call`
7. Click **Schedule** (the primary modal button) to save the activity.

After the task:
- The opportunity's **Sales Team** should be **Channel**.
- The opportunity's **Salesperson** should be **Sara Sales**.
- A scheduled **Call** activity should exist on the opportunity with due
  date **2026-06-10** and summary **Discovery call**.

## Rules

- Do not change the opportunity's name, partner, or revenue.
- Do not change the stage.
- Do not delete the opportunity or convert it to a lead.
- Do not create any other opportunities.
