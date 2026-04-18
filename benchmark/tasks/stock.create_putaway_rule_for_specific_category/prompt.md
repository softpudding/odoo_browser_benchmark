Go to the **Inventory** app.

Navigate to **Configuration → Putaway Rules**.

Create a new putaway rule so that whenever **any product belonging to the product category "Bench Cold Items"** arrives in **WH/Stock**, it is automatically routed to the sub-location **WH/Stock/Refrigerator**.

Click **New** and set exactly these fields on the new rule:

1. **When product arrives in** = `WH/Stock`
2. **Product Category** = `Bench Cold Items` (this is the *Product Category* column — NOT the *Product* column).
3. **Store to** (sublocation) = `WH/Stock/Refrigerator`

Leave **Product** empty — the rule must trigger by category, not by a single product. Leave Storage Category, Package Type, Priority and Company at their defaults.

Save the rule.

**Rules:**
- Fill the **Product Category** field. Do NOT fill the **Product** field — that would create a product-level rule, which is not what we want.
- The source location ("When product arrives in") must be **WH/Stock**, and the destination ("Store to") must be **WH/Stock/Refrigerator** — do not swap them.
- Do not create a putaway rule for any specific product (e.g. "Bench Frozen Salmon" is a category member that you should leave alone — only create the *category-level* rule).
- Do not leave a second blank/draft putaway rule behind.
- Do not modify or delete any existing putaway rules.
- Do not edit the products, categories, locations, or warehouse configuration themselves.
