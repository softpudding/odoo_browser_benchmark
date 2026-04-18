Open the public webshop at **`/shop`**.

Find the product **`Bench Camera`** and click into its product page. The shop has been pre-configured so that **`Bench Tripod`** is an optional accessory of the camera.

Click **`Add to Cart`** on `Bench Camera`. When the optional-product modal appears (offering `Bench Tripod` as an upsell), **add `Bench Tripod` to the same cart** as well so both products end up in your cart together. Then continue to the cart page (**`/shop/cart`**).

On the cart page you should now see two lines:

- `Bench Camera` (qty 1)
- `Bench Tripod` (qty 1)

Now you must orphan the optional. On the cart page, find the **`Bench Camera`** line and click its **delete / trash icon** (the per-line remove button) so that **only `Bench Camera` is removed**. Do **not** touch the `Bench Tripod` line — it must remain in the cart by itself.

When you are done, the cart must contain exactly one line: `Bench Tripod` (qty 1). The cart (the underlying draft sale order) must still exist and remain in draft state.

## Rules

- Do **not** empty the entire cart (do not click any "empty cart" or "clear cart" button if one is offered).
- Do **not** remove the `Bench Tripod` line.
- Do **not** confirm / checkout / pay the order — leave it in draft.
- Do **not** change quantities. Just delete the `Bench Camera` line.
- Do **not** create extra products or new sale orders.
- Do **not** rename either product.
