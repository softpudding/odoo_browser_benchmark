Go to the **Manufacturing** app and open **Manufacturing Orders**.

1. Find the draft manufacturing order **WH/MO/BENCH-DESK-001** for
   **Office Desk** (10 units) and open it.
2. The order is in the **Draft** state. Click the **Confirm** button
   in the form header so the state moves to **Confirmed** and the
   component requirements (Desk Top, Desk Leg, Cable Tray) become
   visible.
3. Click the **Produce All** button in the form header to record
   production of the full quantity (10 units).
4. If a confirmation / consumption / backorder dialog appears,
   accept the default **Apply** / **Validate** option so the MO
   is closed with the full quantity produced.

The order should end in the **Done** state with 10 Office Desks
produced.

**Rules:**
- Do NOT reduce the quantity to produce below 10.
- Do NOT modify the BoM or any component quantities.
- Do NOT cancel the manufacturing order or unlink any records.
- Do NOT create a backorder — produce the full 10 units in one go.
