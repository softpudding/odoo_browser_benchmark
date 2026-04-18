You are logged in as the Administrator. The webshop has been pre-seeded with a single storable product:

- **`Bench Limited Stock`** — storable, `list_price` 40.00, published in the shop.
  - On-hand quantity at **WH/Stock**: **5 units**.
  - Product form has **Show availability Qty** enabled with **Show Threshold = 100**, so the remaining-stock banner is displayed on the product page.

Starting from **`/shop`**:

1. From the webshop listing, open the product **`Bench Limited Stock`** (click its tile to reach `/shop/bench-limited-stock-<id>`).
2. On the product page, confirm that the availability banner is visible. It reads something like **"5.0 Units in stock"** (a yellow badge under the price — this is rendered because `show_availability=True` and the free quantity is under the threshold).
3. Change the **Quantity** input on the product page from `1` to **`3`** (you can type `3` or use the `+` button). Stay within the 5-unit limit.
4. Click **`Add to cart`**. If an optional-product / cross-sell modal pops up, dismiss it (do not add any extra product).
5. You can optionally open `/shop/cart` to verify that one line for `Bench Limited Stock` with **Quantity 3** is in the draft cart.

When you are done, the admin cart (the underlying draft `sale.order`) must contain **exactly one order line** for `Bench Limited Stock`, with `product_uom_qty = 3`.

## Rules

- Do **not** add any other product to the cart.
- Do **not** change the product's list price, name, category, or availability settings.
- Do **not** confirm, checkout, or pay the order — leave it in **draft**.
- Do **not** archive or unpublish the product.
- Do **not** adjust the on-hand inventory.
