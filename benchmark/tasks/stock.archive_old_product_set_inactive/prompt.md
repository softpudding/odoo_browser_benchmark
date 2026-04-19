# Archive the old product "Bench Archive Me"

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

A storable product named **"Bench Archive Me"** has been seeded in the
catalog. It represents a discontinued item and must be archived so it no
longer appears in default product lists.

## What to do

1. In the Inventory app, open the **Products** menu and go to
   **Products** (the product list).
2. Find and open the product named **"Bench Archive Me"**.
3. On the product form, open the **Actions** menu by clicking the cog
   icon (⚙️) in the top control panel (next to the breadcrumb / buttons).
4. Click **Archive** in the dropdown.
5. If a confirmation dialog appears, confirm it.

## Expected end state

- The product **"Bench Archive Me"** is archived:
  - `product.product.active = False`
  - `product.template.active = False`
- No other products are modified or deleted.

## Rules

- Archive exactly the product **"Bench Archive Me"** — do not touch any
  other product.
- Do not delete the product. Use the **Archive** action from the cog
  Actions menu, not Delete/Unlink.
- Do not rename, duplicate, or otherwise modify the product.
