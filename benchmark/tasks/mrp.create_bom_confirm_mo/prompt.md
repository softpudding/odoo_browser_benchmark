# Create a Bill of Materials and confirm a Manufacturing Order

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

## Step 1 — Create a Bill of Materials

1. Go to **Manufacturing → Bills of Materials** and click **New**.
2. Set the **Product** to **Bench Assembly Table** (it already exists).
3. In the **Components** tab, add the following three lines:

   | Component            | Quantity |
   |----------------------|----------|
   | Table Leg            | 4        |
   | Table Top Panel      | 1        |
   | Assembly Screw Pack  | 2        |

4. **Save** the Bill of Materials.

## Step 2 — Create and confirm a Manufacturing Order

1. Go to **Manufacturing → Manufacturing Orders** and click **New**.
2. Set the **Product** to **Bench Assembly Table**.
   The BOM you just created should auto-fill.
3. Set the **Quantity** to **10**.
4. Click **Confirm**.

After confirmation the Manufacturing Order should be in **Confirmed** status.

## Rules

- Use exactly the product and component names listed above.
- Do **not** change the BOM type — keep it as **Manufacture this product**.
- Do **not** mark the Manufacturing Order as done.
- Do **not** delete any existing records.
