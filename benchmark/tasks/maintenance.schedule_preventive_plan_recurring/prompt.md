Schedule a recurring preventive maintenance plan for an existing equipment.

Context:
- Equipment "Conveyor Belt CB-7" already exists in the "Warehouse Gear" category and is assigned to the "Bench Maintenance" team.

Steps:

1. Open the Maintenance app and go to Equipments.
2. Open the equipment "Conveyor Belt CB-7".
3. Click the "Maintenance" tab on the equipment form.
4. Set "Expected Mean Time Between Failure" to `120` days.
5. Save the equipment.
6. Go to Maintenance Requests and create a new request with:
   - Request title: `Monthly Belt Inspection`
   - Equipment: `Conveyor Belt CB-7`
   - Maintenance Type: `Preventive` (this is a radio button, default is `Corrective` — you must change it)
   - Maintenance Team: `Bench Maintenance`
   - Scheduled Date: `05/15/2026 08:00:00`
   - After choosing Preventive, enable the "Recurrent" toggle and set the recurrence to repeat every `30` days.
7. Save the request.

Rules:
- Use the exact request title above.
- Maintenance Type must be Preventive (not Corrective).
- Do not archive or delete any record.
- Do not change the existing equipment's name, category, or team.
