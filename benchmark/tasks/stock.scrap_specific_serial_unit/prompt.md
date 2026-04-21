Go to the **Inventory** app (URL `/odoo/inventory`).

The product **`Bench Sensor Module`** is serial-tracked and currently has **three units** in stock at `WH/Stock`, with the following serial numbers:

- `SN-A001`
- `SN-A002`  ← scrap **only** this one
- `SN-A003`

You must scrap **only the middle unit `SN-A002`** and leave SN-A001 and SN-A003 untouched.

Steps:

1. From the Inventory app, open **Operations → Scrap** in the left navigation.
2. Click **New** to open the scrap form.
3. Fill the form:
   - **Product:** `Bench Sensor Module`
   - **Lot/Serial Number:** `SN-A002` (this MUST be the middle serial — not SN-A001, not SN-A003)
   - **Quantity:** `1`
   - Leave Source Location at the default (`WH/Stock`).
4. Click **Validate** to confirm the scrap.

## Rules

- The Lot/Serial Number must be **exactly `SN-A002`**. Picking `SN-A001` (the first one in the dropdown) or `SN-A003` is wrong and will fail.
- Quantity must be exactly `1`.
- Do NOT scrap more than one serial.
- Do NOT modify on-hand quantities directly via Inventory Adjustments — only the Scrap workflow.
- Do NOT delete or rename any of the three serials.
- Create exactly **one** stock.scrap record.
