Assign a new leasing contract to an existing fleet vehicle and activate it.

1. Open the **Fleet** app.
2. In **Vehicles**, open the vehicle whose license plate is `BENCH-VAN-01` (display name starts with "Bench Van 01").
3. Click the **Contracts** smart button in the button box at the top of the vehicle form.
4. Click **New** to create a new contract record and fill these fields:
   - **Type** (the `cost_subtype_id` field labeled "Type"): `Leasing`
   - **Vendor**: `Bench Lease Co`
   - **Contract Start Date**: `04/20/2026`
   - **Recurring Cost**: `200.00`
   - **Recurring Cost Frequency**: `Monthly` (should already be the default)
   - Leave **Reference**, **Activation Cost**, **Terms and Conditions**, and the **Included Services** tags empty.
5. **Save** the contract record.
6. On the saved contract, look at the clickable **status bar** at the top of the form. The contract's final state must be **Running**. If the status bar shows a different stage (e.g. New / Expired / Cancelled), click the **Running** step to activate the contract. If **Running** is already the highlighted current stage, leave it as-is.

**Rules:**
- Do not modify the vehicle itself (model, driver, license plate, brand).
- Create exactly one contract record linked to `Bench Van 01`.
- The Vendor for the contract must be `Bench Lease Co` (already seeded as a vendor partner — select it from the autocomplete dropdown, do not create a new one).
- Leave the contract's final state at **Running** — do not move it to Expired or Cancelled.
- Do not create extra contracts, extra vendors, or extra vehicles.
