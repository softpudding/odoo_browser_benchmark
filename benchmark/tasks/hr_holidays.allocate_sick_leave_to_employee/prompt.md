# Allocate 15 days of Sick Time Off to an employee

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

The HR team needs you to give **Marc Demo** a fresh **15-day** allocation of
**Sick Time Off** for the rest of the year so he has leave available if needed.

## What to do

1. Open the **Time Off** app and go to **Management → Allocations**
   (the manager view listing allocations).
2. Click **New** to create a new allocation.
3. Fill in:
   - **Description** (the name/reason field): `2026 Sick leave pool`
   - **Employee**: `Marc Demo`
   - **Time Off Type**: `Sick Time Off`
   - **Allocation Type**: `Regular Allocation` (the default)
   - **Allocation**: `15 days`
4. Save the allocation and then click **Approve** (or **Validate**) so it is
   in the Approved state and the 15 days are credited to Marc Demo.

After completion the allocation must be in **Approved** state (backend
state `validate`).

## Rules

- Allocate to **Marc Demo only** — do not touch any other employee's
  allocations.
- The allocated number of days must be exactly **15** (not 10, not 20).
- Leave type must be **Sick Time Off** — do not pick any other type.
- Do **not** delete or modify other existing allocations.
- Do **not** create any time-off *requests* (this task is about allocations
  only — allocating leave balance, not requesting time off).
