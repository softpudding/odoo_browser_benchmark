Open the **Website** app.

In the top menu, click **Site** and choose **Pages** to open the list of website pages.

Find the page named **Bench Source Page** in the list (url `/bench-source-page`). It is currently **Published**.

Duplicate this page:

1. Tick the checkbox on the row for **Bench Source Page** (or open the row so it is selected).
2. Open the **Actions** (cog / gear) menu at the top of the list and click **Duplicate**.
3. This creates a copy of the page. Odoo will typically name the new row something like `Bench Source Page (copy)`.

Open the newly created copy and:

- Change its **Name** to `Bench Duplicate Page`.
- Make sure its **Page URL** becomes `/bench-duplicate-page` (Odoo usually re-slugs the URL automatically when you change the name; if it does not, edit the URL field manually to `/bench-duplicate-page`).
- Make sure the **Published** toggle on the copy is **off** (unpublished).

Save the copy.

**Rules:**
- Do NOT delete the original `Bench Source Page`. It must stay at `/bench-source-page` and remain **Published**.
- The new copy must be named exactly `Bench Duplicate Page` with url `/bench-duplicate-page`, and it must be **unpublished**.
- Do not create any other website pages.
