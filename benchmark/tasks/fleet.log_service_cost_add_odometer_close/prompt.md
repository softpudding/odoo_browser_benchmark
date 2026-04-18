Log a service cost on a fleet vehicle, record the odometer reading at the time of service, and close out the service record.

1. Open the **Fleet** app.
2. In **Vehicles**, open the vehicle whose license plate is `BENCH-TRUCK-01`.
3. Click the **Services** smart button in the button box at the top of the vehicle form.
4. Click **New** to create a new service record and fill these fields:
   - **Service Type**: `Oil Change` (create it on the fly if the dropdown does not offer it)
   - **Date**: `04/15/2026`
   - **Cost**: `120.00` (the currency is EUR)
   - **Vendor**: `Bench Garage`
   - **Odometer Value**: `25000` (in kilometers)
   - Leave **Description** and **Notes** empty.
5. **Save** the service record.
6. On the saved service record, use the **status bar** at the top of the form to move the stage from **New** to **Done**.

**Rules:**
- Do not modify the vehicle itself (model, driver, license plate, brand).
- Create exactly one service record linked to `BENCH-TRUCK-01`.
- The odometer value must be recorded as a new `Odometer` entry on the vehicle (value `25000`). The simplest way is to fill the **Odometer Value** field directly on the service form — Odoo automatically creates an odometer log when the service is saved.
- Do not create extra service records, extra odometer logs, or a new vehicle.
- Leave the service record's **state/stage** at **Done** after saving — do not move it to Running, Cancelled, or back to New.
