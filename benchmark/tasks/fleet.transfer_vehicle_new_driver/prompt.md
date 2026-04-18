Transfer the seeded fleet vehicle to a new driver and update the assignation history.

1. Open the **Fleet** app.
2. Find and open the vehicle with license plate `BENCH-01` (named `TESLA Model 3 [BENCH-01]`).
3. The Driver field currently shows `Old Driver Bob`. Change the Driver to `New Driver Alice`.
4. Save the vehicle.
5. Open the `Drivers History` smart button on the vehicle form. Verify that there are at least two entries: one for `Old Driver Bob` (closed) and one for `New Driver Alice`.
6. Edit the assignation log entry for `New Driver Alice` so that its Start Date is `03/15/2026`. Save.

**Rules:**
- Keep the vehicle's final Driver as `New Driver Alice`.
- Do not delete the existing assignation log entry for `Old Driver Bob`.
- The assignation log entry for `New Driver Alice` must have Start Date = `2026-03-15`.
- Do not create more than one new vehicle, partner, or assignation log beyond what the task requires.
