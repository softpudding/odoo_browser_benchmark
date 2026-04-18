You are already on the page `/bench-image-page` in the website builder (edit mode).

Add an **Image** snippet to this page, then swap its source image to a specific library image:

1. In the left-hand "Add Blocks" / snippets sidebar, locate the **Image** block (under the "Content" category, labelled simply "Image"). It inserts a single image placeholder into the page.
2. Drop the **Image** snippet onto the page body (below the seeded heading section).
3. Once the snippet is on the page, **swap its source image** so that it points to the library image `library_image_10`:
   - Double-click the inserted image (or click it, then use the "Replace" action in the right-hand options panel) to open the **media dialog**.
   - Switch to the **Images** tab (the library tab in the media dialog) and pick the image whose source is `/web/image/website.library_image_10`. If you cannot find it by preview, you can also confirm it via its technical path in the dialog.
4. Click **Save** in the top-right of the website editor to persist the changes.

The page must end up containing at least one `<img>` tag whose `src` is exactly `/web/image/website.library_image_10`, and the seeded heading `Our Image Showcase` must still be present.

**Rules:**
- Do NOT delete the seeded heading section.
- Do NOT change the page name (`Bench Image Page`) or URL (`/bench-image-page`).
- Do NOT unpublish the page.
