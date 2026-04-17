# Allocate sick leave to an employee

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

An employee named **Benchmark Allocatee** needs 15 days of sick leave
allocated to them for the upcoming year.

## What to do

1. In the **Time Off** app, open **Management > Allocations**.
2. Click **New** to create a new allocation.
3. Fill in the allocation:
   - **Employee**: `Benchmark Allocatee`
   - **Time Off Type**: `Sick Time Off`
   - **Allocation** (days / number of days): `15`
   - **Validity Start Date**: `04/17/2026` (today)
   - Leave the **Validity End Date** blank (no expiration)
4. **Save** the allocation.
5. Click **Validate** (or **Approve**) to approve it, so its status
   becomes **Approved**.

## Rules

- Allocate exactly **15 days** — not more, not fewer.
- Use the **Sick Time Off** leave type exactly — not Paid Time Off or any
  other type.
- The allocation must end in the **Approved** state (not left in To Approve
  or Refused).
- Do **not** modify or delete any other allocations.
- Create **exactly one** allocation for this employee.
