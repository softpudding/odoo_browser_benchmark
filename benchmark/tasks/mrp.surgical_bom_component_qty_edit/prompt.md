# Update a single component quantity on a BOM

You are in the Odoo 19 **Manufacturing** app logged in as
**Administrator**.

The Bill of Materials for **Benchmark Assembly Gamma** has 5 component
lines. Engineering asked you to update **only one line** — the
quantity of **Gamma Bolt M6** needs to go from **4** to **6** because
two extra bolts are required in the new revision.

## What to do

1. Open the **Manufacturing** app and go to **Products → Bills of
   Materials**.
2. Open the BOM for **Benchmark Assembly Gamma** (there is only one).
3. On the **Components** tab, find the line for **Gamma Bolt M6**
   (its current quantity is **4**).
4. Change **only that line's quantity** from **4** to **6**.
5. Save the BOM.

The BOM should now have:
- Gamma Frame × 1  (unchanged)
- Gamma Panel × 2  (unchanged)
- **Gamma Bolt M6 × 6**  (was 4)
- Gamma Cable × 3  (unchanged)
- Gamma Sticker × 1  (unchanged)

## Rules

- Change **exactly** the Gamma Bolt M6 quantity to **6**. Do not change
  any other line's quantity, product, or unit.
- Do **not** add or remove any component lines — there must still be
  exactly **five** components after the edit.
- Do **not** modify the finished product's fields (name, BOM type,
  finished qty).
- Do **not** create another BOM.
