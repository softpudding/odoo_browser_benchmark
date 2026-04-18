# Cookbook notes — website_sale /shop filter quirks

New entries for `benchmark/ODOO19_PATTERNS.md` under a `### Website /
website_sale` subsection:

1. **Category filter is a URL PATH, not a query param.** Clicking a
   category link on `/shop` redirects to `/shop/category/<slug-id>`
   (see `website_sale.categorie_link` template + `_get_shop_path`
   in `website_sale/controllers/main.py`). There is no "x on category
   facet" chip — removing the category filter is done by clicking the
   **All Products** link at the top of the Categories sidebar, which
   navigates back to plain `/shop` while preserving existing query
   params like `min_price` / `max_price` via `keep(...)`.
2. **Price filter is a dual-handle multirange slider (`form-range
   range-with-input`).** It is deeply fragile under Playwright drag
   automation. The library however renders a hidden pair of
   `<input type="number">` counters (see
   `addons/website/static/lib/multirange/multirange_custom.js` around
   line 103). **Clicking the `$<value>` counter span toggles the hidden
   number input visible**; typing a number + Enter fires the
   `newRangeValue` JS handler which redirects to
   `window.location.pathname?max_price=<typed>`. The only reliable
   oracle pattern is **direct URL navigation**
   (`/shop/category/<id>?max_price=100`) — the dual-handle drag path
   times out intermittently.
3. **`/shop/cart/add` is a `type='jsonrpc'`, `auth='public'` route.**
   The request body is `{product_template_id, product_id (variant),
   quantity, ...}` wrapped in the standard JSON-RPC envelope. Same
   credentials as the browser session: if the session cookie is for
   admin, the cart is owned by admin; if the agent never logged in,
   the cart is owned by the public user. **Postcondition checks for
   public-shop tasks should find the cart by line content, not by
   `partner_id`** — otherwise a BU run that doesn't bother logging in
   will silently fail the assertion while behaviorally passing.
4. **`product.public.category` is the correct model name** for a
   website (eCommerce) product category — `website.sale.category` is
   a common backlog-prompt misspelling. The m2m on `product.template`
   is `public_categ_ids`.
