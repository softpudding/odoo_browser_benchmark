# Publish the draft "About Us" page AND add it to the main menu

The primary website has a draft page titled **About Us** at URL `/about-us`.
It is currently **Unpublished** and has **no** menu entry in the top navigation.
Your job is to bring it live by doing BOTH of the following:

1. **Publish** the `About Us` page (flip it from Unpublished to Published).
2. **Add a new top-level menu entry** that points at `/about-us` so visitors can
   reach the page from the site's main navigation bar.

## Steps

1. Open the **Website** app (top-left app switcher → Website).
2. From the top bar, open **Site → Pages** (Odoo URL
   `/odoo/website-pages`). You will see a list of website pages.
3. Locate the row named **About Us** (URL `/about-us`). The **Published**
   column on that row is currently **off** — toggle it **on** by clicking the
   small boolean pill / switch in that row's Published cell. (Equivalently,
   you may open the page's form view and toggle the **Published** boolean
   there, or open the page in the website builder and use the
   **Unpublished / Published** switch in the builder's top systray.)
4. Now add a new menu entry for the page. Open **Site → Menu Editor**. In
   the dialog that opens, click **Add Menu Item** and fill in:
   - **Name**: `About Us`
   - **URL**: `/about-us`
5. The new entry must be a **top-level** menu (a direct child of the primary
   website's main menu, alongside `Home`, `Contact Us`, etc.).
6. Position the new `About Us` entry as the **second** top-level entry — it
   must sit directly after `Home` and before every other existing top-level
   item (`About`, `Contact Us`, `Shop`, etc.). You can drag the new row
   upward inside the Menu Editor list, or set its Sequence to a value
   between `Home`'s sequence (10) and the next entry's sequence.
7. Click **Save** in the Menu Editor so the new menu entry and the new
   ordering are persisted.

## Equivalent alternative for creating the menu entry

You may instead configure the menu via the page's **Properties** dialog:
open the page in the website builder, open the Page Properties panel
(gear icon or "Properties" action), flip the **In Menu** / **Add to Menu**
toggle to ON, then Save. The backend creates a `website.menu` entry for
you pointing at `/about-us` under the main menu. If you use this path you
still need to go to **Site → Menu Editor** afterwards and drag the
entry up to the 2nd position (right below `Home`).

## Rules

- The `About Us` page (URL `/about-us`) must end up **Published**
  (`is_published = True`).
- A `website.menu` row with `url = /about-us` MUST exist on the primary
  website (website id 1) after you save, and it must be a child of the
  primary website's main menu (NOT a child of some other menu, and NOT
  unparented).
- In the top-level menu order, the `About Us` entry must be in the
  **2nd** position: directly after `Home` and before every other
  existing top-level entry. Check by eyeballing the top nav on the
  live site — the order should read `Home → About Us → …`.
- The menu entry MUST be distinct from the existing distractor menu
  called `About` (which points at `/contactus`). **Do NOT** edit the
  distractor's URL to `/about-us` — leave the `About` distractor pointing
  at `/contactus`. Create a new entry instead.
- Do NOT change the page's `Name` (stays `About Us`) or `URL` (stays
  `/about-us`).
- Do NOT delete, duplicate, or rename any existing menu entries (Home,
  Contact Us, Shop, About, etc.). Exactly one new `website.menu` row
  should be added.
- Do NOT create additional website pages.
