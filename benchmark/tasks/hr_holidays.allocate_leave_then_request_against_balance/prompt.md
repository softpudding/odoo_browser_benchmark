# Allocate leave, then request time off against it

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

Marc Demo needs a fresh sick-leave balance and then an approved request that
uses part of that balance.

## What to do

1. Go to **Management → Allocations** and create a new allocation with:
   - **Description**: `Quarter-End Sick Leave Buffer`
   - **Employee**: `Marc Demo`
   - **Time Off Type**: `Sick Time Off`
   - **Allocation**: `4 days`
2. Save the allocation and approve it so it reaches the **Approved** state.
3. Then go to **Management → Time Off** and create a new time-off request with:
   - **Description**: `Warehouse flu recovery`
   - **Employee**: `Marc Demo`
   - **Time Off Type**: `Sick Time Off`
   - **Start Date**: `June 23, 2026`
   - **End Date**: `June 24, 2026`
4. Save that request and approve it so the request is also **Approved**.

After completion there must be one approved allocation and one approved leave
request for Marc Demo with the exact values above.

## Rules

- Work on **Marc Demo** only.
- Use **Sick Time Off** for both records.
- The allocation must be exactly **4 days**.
- The leave request must use the exact description and dates above.
- Do not refuse, cancel, or delete any records.
- Do not create extra allocations or extra time-off requests.
