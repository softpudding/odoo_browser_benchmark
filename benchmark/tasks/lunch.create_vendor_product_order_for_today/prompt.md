# Set Up Bench Cafe and Order Today's Lunch

You need to onboard a new lunch vendor, add one product for it, then
place a lunch order for yourself using the Lunch dashboard.

## Step 1 - Create the vendor

1. Open the **Lunch** app (its icon is in the main app switcher).
2. From the top-level menu, open **Configuration -> Vendors**, then click
   **New** to create a vendor.
3. Fill the form:
   - **Vendor** (name): `Bench Cafe`
   - **Vendor** (partner `partner_id`): pick any existing contact from
     the autocomplete (e.g. the default demo partner). If no contact
     exists, create one with the name `Bench Cafe Partner`.
   - **Phone**: `+1 555 0199`
   - In the **Orders** group, set **Delivery** to `Delivery` (not
     "No Delivery").
4. In the **Availability** group, make sure ALL SEVEN weekday toggles
   (Mon, Tue, Wed, Thu, Fri, Sat, Sun) are ON -- click any that are
   currently off so Bench Cafe is available every day of the week.
   Keep **Send Order By** at the default value `Phone`.
5. **Save** the vendor.

## Step 2 - Create the product

1. Still inside the Lunch app, open **Configuration -> Products**, then
   click **New**.
2. Fill the form:
   - **Product Name**: `Veggie Wrap`
   - **Product Category**: `Sandwich` (pick from autocomplete)
   - **Vendor**: `Bench Cafe` (the vendor you just created)
   - **Price**: `8.00`
3. **Save** the product.

## Step 3 - Order it for today

1. In the Lunch app, open **My Lunch -> New Order** (or navigate to
   `/odoo/lunch`).
2. On the Lunch products kanban, click the **Veggie Wrap** card. A
   product detail dialog will open.
3. In the **Notes** field (labelled "Notes"), type: `no onions`
4. Click **Add To Cart** in the dialog footer.
5. The dialog closes and **Veggie Wrap** appears in the right-hand
   sidebar under **Your Order** with quantity 1.
6. Click the **Order Now** button at the bottom of the sidebar to
   submit the order.

## Rules

- The vendor name must be exactly `Bench Cafe`.
- The vendor must be available every day (Mon-Sun all on) so it
  accepts today's order.
- The product name must be exactly `Veggie Wrap`, price 8.00,
  linked to `Bench Cafe`.
- The lunch order must be for today's date, owned by the admin user,
  with product `Veggie Wrap`, quantity 1, note `no onions`.
- The order must be submitted (state must NOT remain "To Order" /
  `new`) - you must click **Order Now** after adding to cart.
- Do not change the vendor's Send Order By setting (leave it on
  `Phone`).
- Do not archive or delete any existing lunch records.
