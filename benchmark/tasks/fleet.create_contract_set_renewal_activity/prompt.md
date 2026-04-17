Create a vehicle, contract, and renewal activity in Odoo Fleet.

1. Open the Fleet app.
2. Create a vehicle with:
   Model: `Cargo EV`
   License Plate: `FLE-6124`
   Driver: `Avery Collins`
   Registration Date: `04/18/2026`
3. Save the vehicle.
4. Open the Contracts menu.
5. Create a contract with:
   Reference: `RENEW-6124`
   Vendor: `Northwind Leasing`
   Vehicle: `Cargo EV / FLE-6124`
   Responsible: `Administrator`
   Start Date: `04/20/2026`
   Expiration Date: `11/20/2026`
6. Save the contract.
7. Schedule a **Contract to Renew** activity on that contract for **11/20/2026** assigned to **Administrator**.

Rules:
- Do not create any extra vehicles or extra contracts with the same reference.
- Keep the driver on the created vehicle as `Avery Collins`.
- Keep the contract linked to the created vehicle.
- Do not add any activity type other than `Contract to Renew`.
