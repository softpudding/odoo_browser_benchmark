# Cookbook notes — website_sale_stock stock-availability banner

New entries for `benchmark/ODOO19_PATTERNS.md` under a
`### Website / website_sale_stock` subsection:

1. **`website_sale_stock` is NOT in the base snapshot**, and neither
   are its hard deps `sale_stock` and `stock_delivery`. It is marked
   `auto_install=True`, but auto-install only fires when ALL deps are
   already installed. Seed must walk the chain explicitly:

   ```python
   for mod_name in ("sale_stock", "stock_delivery", "website_sale_stock"):
       mod = env["ir.module.module"].search([("name", "=", mod_name)], limit=1)
       if mod and mod.state != "installed":
           mod.button_immediate_install()
   ```

2. **The "X in stock" badge on the product page is the `threshold_message`
   block** (QWeb template `website_sale_stock.product_availability`,
   file `addons/website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml`).
   Render conditions:
     - `product.is_storable == True` AND
     - `product.show_availability == True` AND
     - `free_qty <= product.available_threshold` AND
     - `free_qty > 0` (otherwise the out-of-stock / notify-me branch
       fires instead).

   Defaults on `product.template`: `show_availability=False`,
   `available_threshold=5.0`, `allow_out_of_stock_order=True`. The
   prompt / seed therefore must flip `show_availability=True` AND
   set the threshold high enough to cover the seeded on-hand qty, else
   the badge silently disappears.

3. **`product.template.is_storable=True` is the Odoo-19 storable flag
   for a `type='consu'` product.** The legacy `type='product'`
   selection value is gone; every "storable" product is a consu with
   `is_storable=True`. Seed must set both:

   ```python
   env["product.template"].create({
       "type": "consu",
       "is_storable": True,
       ...
   })
   ```

4. **Website cart (`/shop/cart/add`) does NOT enforce the on-hand cap
   while `allow_out_of_stock_order=True` (the default).** Even if the
   banner advertises "5 Units in stock", a JSON-RPC POST of
   `quantity=999` succeeds and the cart line carries 999. If a task
   needs a hard UI cap it must flip `allow_out_of_stock_order=False`
   AND set `out_of_stock_message` / threshold combos — otherwise the
   prompt can only describe the cap narratively, not rely on the
   server to enforce it. This matters for calibration: tasks that
   want to "test that the agent respects the displayed stock limit"
   need the non-default flag; tasks that just want the banner
   visible can keep the default.

5. **BU is trivially good at product-detail quantity + Add-to-cart.**
   The `input[name="add_qty"]` sits directly adjacent to
   `#add_to_cart`; no modal, no dual-handle slider, no wizard. Do NOT
   build a medium-difficulty task around the quantity bump alone —
   combine with filter/category navigation, optional-product modal
   dismissal, or a cart-level edit to escalate.
