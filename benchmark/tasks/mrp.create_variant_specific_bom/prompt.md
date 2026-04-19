# Create a Bill of Materials that applies to only one product variant

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

A product template **Bench T-Shirt** already exists with a **Bench Color**
attribute that produces two variants: **Bench T-Shirt (Red)** and
**Bench T-Shirt (Blue)**. A component product **Bench Fabric** also exists.

No Bill of Materials exists yet for Bench T-Shirt. You must create one that
is specific to the **Red variant only** — it must not apply to the Blue
variant.

## What to do

1. Open the **Manufacturing** app and go to **Products → Bills of Materials**.
2. Click **New** to create a new Bill of Materials.
3. Fill in the form:
   - **Product**: `Bench T-Shirt` (select the product template in the
     Product field).
   - **Apply on Variants**: `Bench Color: Red` (this field is
     labeled **Apply on Variants** on the BoM form and determines which
     variant the BoM applies to). It must be set so that the BoM applies
     to the **Red** variant only, not to all variants.
   - **Quantity**: `1`
   - Leave **BoM Type** at its default (**Manufacture this Product**).
4. Under the **Components** tab, click **Add a line** and add exactly one
   component:
   - **Component**: `Bench Fabric`
   - **Quantity**: `1`
5. Save the record.

After you finish:

- Exactly **one** `mrp.bom` record exists for the **Bench T-Shirt** product
  template.
- That BoM's **Apply on Variants** is set to **Bench T-Shirt (Red)** — it
  must NOT be left blank (blank means "applies to all variants").
- The BoM has exactly one component line: **Bench Fabric**, quantity **1**.

## Rules

- Do **not** create a BoM that applies to all variants (Apply on Variants
  left blank). The BoM must be Red-variant-specific.
- Do **not** create a BoM for the Blue variant.
- Do **not** create more than one Bill of Materials for Bench T-Shirt.
- Do **not** add more than one component line; the BoM must have exactly
  one line.
- Do **not** modify the Bench T-Shirt product template, its attributes, or
  its existing variants.
- Do **not** create a manufacturing order — only the BoM is required.
