Go to the **Inventory** app (URL `/odoo/inventory`).

A validated receipt with reference **`BENCH-RCV-SCRAP-01`** already exists. It received **10 units** of the product **`Bench Scrap Product`** from the supplier into `WH/Stock`. The receipt is already in **Done** state.

Two of those received units are damaged and need to be scrapped.

## Steps

1. From the Inventory dashboard, open **Receipts** (the Incoming Transfers tile).
2. Open the validated receipt with the source document **`BENCH-RCV-SCRAP-01`**. (It is in the **Done** state, so you may need to clear default filters or switch to the Done filter to see it.)
3. From the receipt form, open the **Actions** (cog / gear) menu and click **Scrap** (or use the Scrap button if available on the form). A Scrap Products dialog will open.
4. In the Scrap dialog, fill:
   - **Product:** `Bench Scrap Product`
   - **Quantity:** `2`
   - Leave **Source Location** at the default (`WH/Stock`).
   - Leave **Scrap Location** at the default (`Virtual Locations/Scrap`).
5. Click **Scrap Products** in the dialog to confirm. The scrap record will be created and validated in one step (status **Done**).

## Rules

- The scrap must be linked to the seeded receipt `BENCH-RCV-SCRAP-01` (use the Scrap action from the receipt, not a standalone scrap from Operations > Scrap).
- The scrapped product must be exactly **`Bench Scrap Product`** and the quantity must be exactly **`2`**.
- The scrap record must end up in the **Done** state (you must click **Validate**).
- Do NOT cancel, delete, or modify the original receipt. It must stay in **Done** state with the original received quantity of 10.
- Do NOT create more than one stock.scrap record.
- Do NOT touch other products or other receipts.
