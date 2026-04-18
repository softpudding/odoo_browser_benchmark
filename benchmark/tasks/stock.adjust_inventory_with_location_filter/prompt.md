Open the **Inventory** app and go to **Operations > Physical Inventory**.

Product **`Bench Multi Loc Product`** currently has stock in two sub-locations of **`WH/Stock`**:

- **`WH/Stock/Shelf A`** — 50 units on hand
- **`WH/Stock/Shelf B`** — 30 units on hand

The warehouse team recounted **Shelf A only** and discovered the real count is
**42 units**. Shelf B was NOT recounted and its quantity must stay at 30.

Do the following:

1. In **Physical Inventory**, filter the view so you see only the row for
   `Bench Multi Loc Product` at `WH/Stock/Shelf A`. Use the **Location** filter
   or the search bar (e.g., filter by Location = `Shelf A` and Product =
   `Bench Multi Loc Product`).
2. On that row, set **Counted Quantity** to **`42`**.
3. Click the per-row **Apply** action on the Shelf A row to post the
   inventory adjustment.

## Rules

- Only adjust the `Shelf A` quant for `Bench Multi Loc Product`.
- Do NOT change, apply, or touch the `Shelf B` quant in any way.
- Do NOT click **Apply All** — use the per-row **Apply** for the Shelf A row.
- Do NOT delete any quant, product, or location.
- After you finish, the Shelf A quantity must be `42` and the Shelf B quantity
  must still be `30`.
