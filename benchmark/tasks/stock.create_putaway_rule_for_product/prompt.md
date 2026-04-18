Open the **Inventory** app. The warehouse needs a new putaway rule so that
incoming units of **`Bench Putaway Product`** are automatically stored into the
sub-location **`WH/Stock/Bench Shelf A`** whenever they arrive in `WH/Stock`.

Do the following:

1. Go to **Configuration > Warehouse > Putaway Rules** and click **New**.
2. On the new inline row, set the fields to exactly these values:
   - **When product arrives in**: `WH/Stock`
   - **Product**: `Bench Putaway Product`
   - **Store to**: `WH/Stock/Bench Shelf A`
3. **Save** the putaway rule.

## Rules

- The **When product arrives in** location must be exactly `WH/Stock` (not
  `WH/Input`, not a warehouse, not any other location).
- The **Product** must be exactly `Bench Putaway Product`.
- The **Store to** location must be exactly `WH/Stock/Bench Shelf A`.
- Leave **Product Category** blank (the rule is per-product, not per-category).
- Do NOT create duplicate putaway rules for this product.
- Do NOT delete, rename, or archive any existing location, product, or
  putaway rule for other products.
