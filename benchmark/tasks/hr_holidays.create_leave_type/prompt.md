# Create a new Time Off Type with manager approval

You are in the Odoo 19 **Time Off** app logged in as **Administrator**.

HR wants a new dedicated leave category for conference attendance.
Create a new **Time Off Type** with manager-level approval.

## What to do

1. Open the **Time Off** app.
2. Go to **Configuration → Time Off Types** in the app's menu.
3. Click **New** to create a new type.
4. Fill in exactly these fields:
   - **Time Off Type Name**: `Conference Attendance`
   - **Approval**: `By Time Off Officer` (so `leave_validation_type`
     becomes `manager` in the backend — this matches the
     "By Time Off Officer" label in the Approval radio selector).
   - **Requires allocation**: `No Limit` (so the type does not require
     a pre-allocation; backend `requires_allocation = 'no'`).
5. Save the record.

## Rules

- Create exactly **one** new Time Off Type.
- The name must be exactly `Conference Attendance` (case-sensitive).
- Backend `leave_validation_type` must be `'manager'`.
- Do **not** modify any existing leave type.
- Do **not** create any leave requests or allocations.
