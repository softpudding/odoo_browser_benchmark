Add a new vehicle to Fleet, then log an odometer reading for it.

1. Open the **Fleet** app.
2. Click **New** to create a new vehicle with exactly these values:
   - **Model**: `Model 3` (select the existing model under the `Tesla Motors` brand — do not create a new brand or model)
   - **License Plate**: `FLEET-ADD-01`
3. **Save** the vehicle.
4. From the Fleet menu, open **Vehicles > Odometer** (the Odometers list).
5. Click **New** and add an odometer log for the vehicle you just created:
   - **Vehicle**: `Tesla Motors/Model 3/FLEET-ADD-01` (the vehicle you just created)
   - **Date**: `2026-04-15`
   - **Odometer Value**: `15000`
6. **Save** the odometer log.

**Rules:**
- Create exactly one new vehicle with license plate `FLEET-ADD-01`.
- Do not modify any existing vehicle.
- The odometer reading must be exactly `15000` (in kilometers, the default unit).
- The odometer log date must be `2026-04-15`.
- Do not create extra odometer logs for this vehicle.
- Do not archive or delete the vehicle.
