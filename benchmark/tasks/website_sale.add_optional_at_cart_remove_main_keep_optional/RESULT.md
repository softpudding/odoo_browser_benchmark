ROW: 315
TASK_ID: website_sale.add_optional_at_cart_remove_main_keep_optional
DIFFICULTY: hard
SUMMARY: From /shop add Bench Camera with Bench Tripod optional, then on cart remove only Camera leaving Tripod orphaned.
ORACLE: PASS
BROWSER_USE: FAIL
F1: 0.0
CALIBRATION: matches

DETAIL_SECTION:
## website_sale.add_optional_at_cart_remove_main_keep_optional

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | FAIL |
| **F1** | 0.0 |
| **Odoo modules** | Website (eCommerce) / website_sale |
| **Workflow** | From `/shop`, agent opens `Bench Camera`, clicks Add to Cart, accepts the optional-product modal upsell to add `Bench Tripod` to the same cart. Then on `/shop/cart` clicks the per-line trash icon on the `Bench Camera` row only, leaving `Bench Tripod` as an orphaned optional in the same draft sale order. |
| **Capability tested** | Per-line cart manipulation on the public webshop combined with the cognitive twist of selectively removing the *main* product while preserving its dependent *optional* upsell. |
| **Notes** | Browser-use timed out at 480s without ever placing a `Bench Tripod` line into a website cart for admin -- it never reliably drove the optional-products modal on `/shop`. Postcondition: "No website cart for admin contains a 'Bench Tripod' line." StateDiff is empty by design (only `product.template.is_published / website_published` are tracked, both unchanged from seed), so F1 mechanically scores 0.0 on the failed run because there are 0 expected and 0 observed edits and no matching edits. The hard pattern is the non-intuitive "remove main but keep optional" UI manipulation, which combines (a) the optional-products modal on add-to-cart and (b) the per-line trash icon on the public cart page. |
