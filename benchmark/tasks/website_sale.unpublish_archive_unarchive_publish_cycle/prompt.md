Go to the **eCommerce Products** page.

The seeded product **`Bench Cycle Gadget`** is currently published on the website
and active. Take it through the following 5-step state cycle, in this exact
order, on the same product:

1. **Unpublish** the product (open the **Sales** tab and toggle the
   *Is Published* switch off in the *Ecommerce Shop* group so the product
   is no longer published).
2. Open the **Actions** (cog) menu and click **Archive**. The product becomes
   inactive and disappears from the default product list.
3. In the eCommerce Products list, open the **Filters** menu and enable the
   **Archived** filter so archived products appear. Open
   **`Bench Cycle Gadget`** again, open the **Actions** (cog) menu and click
   **Unarchive**. The product becomes active again.
4. **Publish** the product back to the website (open the **Sales** tab and
   toggle the *Is Published* switch on again in the *Ecommerce Shop* group).
5. Set the product's **Internal Reference** to `BCG-RESTORED` and save.

Final expected state on **`Bench Cycle Gadget`**:

- `Active = True`
- `Published on Website = True`
- `Internal Reference = BCG-RESTORED`

**Rules:**
- Operate only on the product `Bench Cycle Gadget`. Do not edit any other
  product.
- Do **not** delete the product. Only toggle published/active and set the
  internal reference.
- Do **not** duplicate the product or create a new product.
- Do **not** rename the product or change its sales price.
- The transitions must be performed in order: unpublish first, then archive,
  then unarchive, then publish, then set the internal reference.
