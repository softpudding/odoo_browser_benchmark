# Log a fuel refill against a fleet vehicle

You are in the Odoo 19 **Fleet** app logged in as **Administrator**.

The company car **FUEL-9001** was refuelled at a station. You need to
log this refuelling as a **Service** record on the vehicle so the cost
goes on the vehicle's running tally.

## What to do

1. Open the **Fleet** app and find the vehicle with licence plate
   **FUEL-9001** (model "Benchmark Fleet Hybrid").
2. Open the vehicle, and from its form click the **Services** stat
   button.
3. Click **New** to create a new service record.
4. Fill in exactly these fields:
   - **Service Type**: `Refueling`  (create the service type on the fly
     if it is not offered by the dropdown).
   - **Vendor**: `BP Express Holloway`
   - **Cost**: `87.50`
   - **Date**: `2026-05-20`
   - **Notes** (description/notes field): `42 L unleaded at £2.08/L`
5. Save the service record. It should be listed as one more service
   under the vehicle.

## Rules

- The service record must be linked to vehicle **FUEL-9001** only.
- The service record's fields must be **exactly** the values above —
  do not round, abbreviate, or change.
- Do **not** modify the vehicle itself. After the task, the vehicle's
  driver, model, and licence plate must be unchanged.
- Do **not** create more than one service record.
- Do **not** create a contract or odometer entry.
