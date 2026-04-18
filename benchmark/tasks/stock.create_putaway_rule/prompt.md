Go to the **Inventory** app.

Navigate to **Configuration → Putaway Rules**.

Create a new putaway rule so that whenever the product **"Storage Box Echo"** arrives in **WH/Stock**, it is automatically routed to the sub-location **WH/Stock/Shelf A1**.

Click **New** and set exactly these fields on the new rule:

1. **Product** = `Storage Box Echo`
2. **When product arrives in** = `WH/Stock`
3. **Store to sublocation** = `WH/Stock/Shelf A1`

Leave all other fields (Product Category, Storage Category, Package Type, Priority, Company) at their defaults.

Save the rule.

**Rules:**
- Fill the **Product** field (do NOT fill Product Category instead).
- The source location ("When product arrives in") must be **WH/Stock**, and the destination ("Store to sublocation") must be **WH/Stock/Shelf A1** — do not swap them.
- Do not create a putaway rule for any other product (e.g. "Storage Box Foxtrot" is a distractor — leave it alone).
- Do not leave a second blank/draft putaway rule behind.
- Do not modify or delete any existing putaway rules.
- Do not edit the products, locations, or warehouse configuration themselves.
