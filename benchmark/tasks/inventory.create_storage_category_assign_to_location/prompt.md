Go to the **Inventory** app.

**Step 1 — Enable Storage Categories in Settings.**

In Odoo 19, the Storage Categories feature is gated by the **Storage Locations** setting. Open **Configuration → Settings**, scroll to the **Warehouse** block, and turn ON the toggle labeled **"Storage Locations"** (full label is "Storage Locations / Track product location in your warehouse"). Click **Save** at the top of the settings page so the new menu items appear.

**Step 2 — Create the storage category.**

Go to **Configuration → Storage Categories** (this menu only appears after Step 1).

Click **New** and create exactly one storage category with these values:

- **Storage Category** (name) = `Cold Chain`
- **Max Weight** = `500` (the unit is kg, shown next to the field)

Leave **Allow New Product** at its default (`Allow mixed products`) and leave the **Capacity by Package** and **Capacity by Product** tables empty.

**Save** the new category.

**Step 3 — Assign the category to WH/Stock.**

Go to **Configuration → Locations**. In the list, click the row for **WH/Stock** (the internal location whose Full Location Name is exactly `WH/Stock`).

On the location form, in the **Logistics** section, set the **Storage Category** field to `Cold Chain` (use the autocomplete dropdown).

**Save** the location.

**Rules:**

- You MUST enable the Storage Locations setting first; without it, both the Storage Categories menu and the Storage Category field on locations are hidden.
- Set **Max Weight = 500** on the Cold Chain category itself — do NOT add a row to the Capacity by Product table (those are per-product quantities, not the max weight).
- Assign the category to the existing **WH/Stock** location only — do not create a new location, do not modify any other location.
- Do not create extra storage categories or rename "Cold Chain".
- Do not change anything else in the Inventory settings.
