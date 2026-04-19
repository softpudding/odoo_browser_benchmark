# Enable the MTO stock route on `Bench MTO Item`

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

A storable product **`Bench MTO Item`** has been added to the catalog with
**no routes selected**. To make the system trigger procurement each time this
item is sold, it must carry the **Replenish on Order (MTO)** route.

## What to do

1. Open the **Inventory** app.
2. Go to **Products > Products** and open the product **`Bench MTO Item`**.
3. On the product form, switch to the **Inventory** tab (the page where the
   Logistics / Operations groups are rendered, alongside weight, volume,
   customer lead time, etc.).
4. In the **Operations** group, locate the **Routes** field. It renders as a
   list of checkboxes (one per applicable route).
5. Tick the checkbox labelled **`Replenish on Order (MTO)`** and leave every
   other checkbox in that Routes group unchecked.
6. **Save** the product.

## Expected end state

- The product **`Bench MTO Item`** has its `route_ids` set to a single route:
  the **Replenish on Order (MTO)** route
  (`stock.route_warehouse0_mto`).

## Rules

- Enable ONLY the **Replenish on Order (MTO)** route. Do NOT additionally
  enable Buy, Manufacture, Dropship, or any other route in that checkbox
  group.
- Do NOT change any other field on the product (keep the name, type,
  storable flag, prices, category, etc. untouched).
- Do NOT archive, duplicate, or delete the product.
- Do NOT create a new route — the MTO route is already available, you only
  need to tick its checkbox.
