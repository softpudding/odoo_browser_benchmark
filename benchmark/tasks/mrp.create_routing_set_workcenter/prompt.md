Create a new work center and link it as an operation on an existing Bill of Materials.

1. Go to **Manufacturing** → **Configuration** → **Work Centers**. Click **New**.
   Set **Name** = `Benchmark Assembly Station`. Save.
2. Go to **Manufacturing** → **Products** → **Bills of Materials**. Open the
   BOM for product **Benchmark Frame Assembly**.
3. Click the **Operations** tab. Add a new operation with:
   - **Operation** = `Final Assembly`
   - **Work Center** = `Benchmark Assembly Station`
   - **Default Duration** = `30` minutes
4. Save the BOM.

**Rules:**
- Do NOT create a new BOM; use the seeded one.
- Do NOT modify or delete the existing component lines.
- Do NOT rename the BOM's product.
