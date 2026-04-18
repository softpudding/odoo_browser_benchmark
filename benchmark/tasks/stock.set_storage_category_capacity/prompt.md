Open the **Inventory** app. The warehouse team has a new sub-location
**`WH/Stock/Bench Small Bin Area`** and wants to limit what can go there. You
must first define a storage category with a capacity rule, then assign that
storage category to the existing sub-location.

Do the following:

1. Go to **Configuration > Warehouse > Storage Categories** and click **New**.
2. Create a storage category with these exact values:
   - **Storage Category** (name): `Bench Small Bin`
   - **Max Weight**: `50`
   - **Allow New Product**: `If all products are same`
3. **Save** the new storage category.
4. Go to **Configuration > Warehouse > Locations**, open the internal location
   **`WH/Stock/Bench Small Bin Area`**.
5. Set the **Storage Category** field on that location to `Bench Small Bin`.
6. **Save** the location.

## Rules

- Use exactly the name `Bench Small Bin` (no extra spaces, no trailing words).
- `Max Weight` must be `50` (in kg).
- `Allow New Product` must be set to **`If all products are same`** — not the
  default "Allow mixed products".
- Do NOT delete, rename, or archive any existing location, product, or
  storage category.
- Do NOT assign `Bench Small Bin` to any other location besides
  `WH/Stock/Bench Small Bin Area`.
