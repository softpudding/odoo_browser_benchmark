Go to the **Manufacturing** app.

Open **Products → Bills of Materials** and click **New** to create a new
Bill of Materials for the product **`Bench Kit Finished`**.

Fill the form with **exactly** these values:

- **Product**: `Bench Kit Finished`
- **Quantity**: `1` (leave the default)
- **BoM Type**: **Kit** (this is the key field — the radio group offers
  three options: *Manufacture this Product* (default), **Kit**,
  *Subcontracting*. You **must** click the **Kit** radio option so the
  BoM is saved with `type='phantom'`. Do NOT leave it on the default
  "Manufacture this Product".)
- Under the **Components** tab, add **exactly two** lines via
  **Add a line**:
  - **`Bench Kit Comp A`** with quantity **`2`**
  - **`Bench Kit Comp B`** with quantity **`3`**

Save the Bill of Materials.

## Rules

- The BoM **must** have BoM Type = **Kit** (internal value `phantom`).
  A BoM saved with the default "Manufacture this Product" (internal
  value `normal`) is considered a failure.
- The BoM must have **exactly two** component lines — no more, no less,
  no empty/phantom rows.
- Do NOT create more than one Bill of Materials for
  `Bench Kit Finished`.
- Do NOT modify the three pre-seeded products (`Bench Kit Finished`,
  `Bench Kit Comp A`, `Bench Kit Comp B`).
- Do NOT create a Manufacturing Order — only the BoM is required.
