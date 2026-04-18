Open the public webshop at **`/shop`**.

The shop has been pre-seeded with two Website Product Categories and five products:

- **Gadgets**
  - `Bench Gadget Mini` - $30
  - `Bench Gadget Plus` - $80
  - `Bench Gadget Pro` - $150
- **Widgets**
  - `Bench Widget Tiny` - $20
  - `Bench Widget Max` - $120

Starting from **`/shop`**:

1. In the left **Categories** sidebar, click **`Gadgets`** to filter the shop to the Gadgets category. The URL should change to a path like `/shop/category/gadgets-<id>` and only the three Gadget products should be listed.
2. Apply a **Price Range** filter with a **maximum price of 100**. The easiest way is to click the right-hand price value on the price slider and type `100` into the input (or drag the right-hand slider handle to 100). After applying, the URL should include `max_price=100` and only `Bench Gadget Mini` and `Bench Gadget Plus` should be listed.
3. Now **clear the Gadgets category** filter (but keep the price filter). The cleanest way is to click the **`All Products`** link at the top of the Categories sidebar. After clicking it, the URL should drop the `/category/...` segment but still include `max_price=100`, and you should now see three products listed: `Bench Gadget Mini`, `Bench Gadget Plus`, and `Bench Widget Tiny`.
4. Open the product page for **`Bench Widget Tiny`** and click **`Add to Cart`** (qty 1). If an optional-product upsell modal appears, dismiss it without adding anything extra.

When you are done, the admin cart (the underlying draft `sale.order`) must contain **exactly one line** for `Bench Widget Tiny`, with quantity `1`.

## Rules

- Do **not** add any other product to the cart.
- Do **not** confirm, checkout, or pay the order - leave it in **draft**.
- Do **not** edit product prices or rename any product.
- Do **not** archive or unpublish any seeded product.
- Do **not** change the quantity (leave it at 1).
