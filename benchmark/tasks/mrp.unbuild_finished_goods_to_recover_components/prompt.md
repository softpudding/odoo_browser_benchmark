# Unbuild a completed manufacturing order to recover components

You are in the Odoo 19 **Manufacturing** app logged in as
**Administrator**.

Manufacturing order **WH/MO/UNBLD-001** was completed (3 units of
**Benchmark Recoverable Widget** produced), but quality control rejected
all 3 units. You need to **unbuild** them so their components return to
stock.

## What to do

1. Open the **Manufacturing** app.
2. Go to **Products → Unbuild Orders** (or **Operations → Unbuild**,
   depending on menu layout).
3. Click **New** to create a new unbuild order with:
   - **Manufacturing Order**: `WH/MO/UNBLD-001`
   - **Product**: should auto-populate to `Benchmark Recoverable Widget`
   - **Quantity**: `3` (the full produced quantity)
4. Click **Save**, then **Unbuild** (the confirm/validate action).
5. The unbuild should move to **Done** state. The finished product
   quantity is consumed; the component quantities are returned to the
   stock location.

## Rules

- Create **exactly one** unbuild order, linked to MO
  **WH/MO/UNBLD-001**.
- The unbuild quantity must be exactly **3**.
- The unbuild must end in the **Done** state (validated).
- Do **not** cancel the original MO — it stays in the Done state.
- Do **not** create any other manufacturing orders, unbuild orders,
  or inventory adjustments.
