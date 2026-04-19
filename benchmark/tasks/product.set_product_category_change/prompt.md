# Change the product category of "Bench Cat Item"

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

A product named **"Bench Cat Item"** has been seeded in the catalog. Its
**Product Category** is currently **All**, and it needs to be reclassified
as **Office Supplies**.

## What to do

1. In the Inventory app, open the **Products** menu and go to
   **Products** (the product list).
2. Find and open the product named **"Bench Cat Item"**.
3. On the product form, locate the **Product Category** field
   (many2one, currently set to **All**).
4. Clear the field (or click it) and type `Office Supplies`, then
   select **Office Supplies** from the autocomplete dropdown.
5. **Save** the product form.

## Expected end state

- The product **"Bench Cat Item"** has its Product Category set to
  the `product.category` named **"Office Supplies"**
  (i.e. `product.template.categ_id` points at Office Supplies).

## Rules

- Change only the **Product Category** (`categ_id`) — do not modify
  any other field on the product.
- Do not rename the product.
- Do not create a new category. The **Office Supplies** category
  has already been seeded for you — select it from the autocomplete.
- Do not archive, delete, or duplicate the product.
