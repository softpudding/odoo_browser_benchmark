Add a new top-level menu entry to the primary website and then reorder it so
it sits in the **second position** of the top-level navigation (just after
`Home` and before `Bench Contact`).

1. Open the **Website** app.
2. From the top bar, open **Site > Menu Editor** (the dialog that lets you
   add, edit, and reorder website menu entries).
3. In the Menu Editor, click **Add Menu Item** to create a new entry with:
   - **Name**: `Bench Menu`
   - **URL**: `/bench-menu-target`
   (The page at `/bench-menu-target` has already been created for you; do
   NOT create another website page.)
4. The new entry will initially appear at the bottom of the top-level menu
   list. **Drag it upwards** so that it is in position 2 — directly below
   `Home` and directly above `Bench Contact`. Other top-level entries
   (`Bench Contact`, plus any default ones like `Shop`, `Contact Us`, etc.)
   must remain present and keep their relative order.
5. Click **Save** in the Menu Editor so the new menu entry and the new
   ordering are persisted.

**Rules:**
- Use the exact name `Bench Menu` and URL `/bench-menu-target`.
- The entry must be a top-level menu (child of the primary website's main
  menu, alongside `Home` and `Bench Contact`), not a sub-item of another
  entry.
- The entry must belong to the primary website (website id 1).
- After saving, the top-level menu order must be: `Home` first,
  `Bench Menu` second, `Bench Contact` third.
- Do not rename, delete, or change the URL of `Home`, `Bench Contact`, or
  any other existing menu entry.
- Do not create extra `Bench Menu` duplicates.
- Do not create a new website page; the page `/bench-menu-target` already
  exists.
