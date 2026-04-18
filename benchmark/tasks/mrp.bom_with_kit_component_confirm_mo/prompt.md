Go to the **Manufacturing** app.

The database already contains these products:

- **Bench Kit** — a kit product whose Bill of Materials has **BoM Type = Kit (phantom)**
  and contains two sub-components: **Bench Sub-A** (1 unit) and **Bench Sub-B** (2 units).
- **Bench Frame** — an ordinary storable component.
- **Bench Assembly** — a finished product with a **normal** Bill of Materials
  that consumes **1x Bench Kit** and **1x Bench Frame** per unit produced.

Your job is to create and confirm a new Manufacturing Order:

1. From the Manufacturing app, open **Operations > Manufacturing Orders**
   (or click the **New** button from the MO list).
2. Click **New** to create a new manufacturing order.
3. In the **Reference** field, type the exact name: `M-BENCH-KIT-001`.
4. In the **Product** field, pick **Bench Assembly**.
5. Leave the **Quantity** at **1** (do NOT change it).
6. In the **Bill of Material** field, pick the pre-seeded BoM for **Bench Assembly**
   (it is the only BoM matching that product — select it from the autocomplete).
7. Save the record (cloud icon or Ctrl+S) so the MO is written in the **Draft** state.
8. Click the **Confirm** button in the form status bar so the MO moves to the
   **Confirmed** state.

That is all — do NOT click Produce All / Mark as Done, and do NOT close the MO.

After Confirm, the **Components** tab on the MO must show **three** rows (one each for
**Bench Sub-A**, **Bench Sub-B**, and **Bench Frame**) — NOT two rows showing Bench Kit
and Bench Frame. This is because Bench Kit is a phantom/kit BoM and Odoo automatically
expands it into its own sub-components on confirm; you do **not** need to edit the
Components tab, modify the BoM, or add anything manually — the expansion is automatic.

**Rules:**
- Do NOT modify any BoM (neither Bench Kit's nor Bench Assembly's).
- Do NOT manually add, delete, or edit any rows on the Components tab.
- Do NOT change the quantity away from 1.
- Do NOT click Produce All, Mark as Done, or Cancel.
- The MO must end in the **Confirmed** state (not Draft, not In Progress, not Done).
