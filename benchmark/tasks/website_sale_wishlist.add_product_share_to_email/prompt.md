You are logged in as the Administrator. The webshop has been pre-seeded with a single published product:

- **`Bench Wishlist Item`** — consumable, `list_price` 25.00, published in the shop.

The wishlist module (`website_sale_wishlist`) is installed so a heart-shaped "Add to wishlist" button is available on product pages.

Starting from **`/shop`**:

1. From the webshop listing, open the product **`Bench Wishlist Item`** (click its tile).
2. On the product page, click the **"Add to wishlist"** button (the heart icon, labelled *Add to wishlist*). After the click the button should flip to *In your wishlist* and the heart icon should fill in (`fa-heart` instead of `fa-heart-o`). The header wishlist icon's counter should also increment to `1`.
3. Navigate to **`/shop/wishlist`** (or click the heart icon in the website header). Confirm that `Bench Wishlist Item` now appears on the My Wishlist page.

When you are done, the database must contain **exactly one** `product.wishlist` row for the admin partner, referencing the `Bench Wishlist Item` product, on the currently-published website.

## Rules

- Do **not** change the product's list price, name, category, or availability.
- Do **not** remove the product from the wishlist (do not click the small close "x" on the wishlist card).
- Do **not** add any other product to the wishlist.
- Do **not** archive or unpublish the product.
- Do **not** add the product to the cart or checkout — this is a wishlist-only task.
- Do **not** log out. The wishlist record must be attached to the Administrator's partner, not to an anonymous session.
