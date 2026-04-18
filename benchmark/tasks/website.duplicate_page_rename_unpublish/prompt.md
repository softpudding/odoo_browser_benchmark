Open the **Website** app.

In the top menu, click **Site** and choose **Pages** to open the list of website pages.

Find the page named **Bench Original** in the list (url `/bench-original`).

Duplicate this page:

1. Tick the checkbox on the row for **Bench Original** (or open the row so it is selected).
2. Open the **Actions** (cog / gear) menu at the top of the list and click **Duplicate**.
3. This creates a copy of the page. Odoo will typically name the new row something like `Bench Original (copy)`.

Open the newly created copy and:

- Change its **Name** to `Bench Original Draft`.
- Make sure its **Page URL** becomes `/bench-original-draft` (Odoo usually re-slugs the URL automatically when you change the name; if it does not, edit the URL field manually to `/bench-original-draft`).
- Make sure the **Published** toggle on the copy is **off** (unpublished).

Save the copy.

**Rules:**
- Do NOT delete the original `Bench Original` page. It must stay at `/bench-original` and remain **Published**.
- The new copy must be named exactly `Bench Original Draft` with url `/bench-original-draft`, and it must be **unpublished**.
- Do not create any other website pages.
