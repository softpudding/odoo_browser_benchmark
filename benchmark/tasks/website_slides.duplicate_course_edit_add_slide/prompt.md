Duplicate an existing eLearning course, rename the copy, and add a new slide to it.

Background: A course named `Bench Course Original` already exists in the eLearning
app. It is a published training course with one existing video slide named
`Bench Intro Video`. Leave the `Bench Course Original` course and its existing
slide untouched.

Steps to perform:

1. Open the eLearning app.
2. Open the `Bench Course Original` course form (click the course tile / row).
3. On the course form, open the cog / Actions menu and click `Duplicate` to
   create a copy of the slide.channel. The form will navigate to the new copy
   (its initial name is `Bench Course Original (copy)` or similar — the exact
   default copy suffix does not matter because you are about to rename it).
4. On the duplicated course, rename it to `Bench Course Spring`.
5. Save the duplicated course.
6. Open the `Content` tab of `Bench Course Spring` and click `Add Slide` (or
   `Add Content`) to add a new slide with these fields:
   - Title: `Welcome slide`
   - Category / Type: `Article` (if Article is not available in this release,
     use `Document` — either is accepted)
   - Article / Description body: any short non-empty text (for example
     `Welcome to the spring session of the Bench course.`)
7. Save the new slide.

End state to achieve:

- Exactly two `slide.channel` records whose name starts with `Bench Course`:
  `Bench Course Original` (unchanged) and `Bench Course Spring` (the
  duplicated + renamed copy).
- `Bench Course Spring` has exactly one `slide.slide` content row whose name
  is `Welcome slide` and whose `slide_category` is `article` (or `document`).
  No other slides on the Spring course.
- `Bench Course Original` is unchanged: its name must still be
  `Bench Course Original`, and it must still have exactly its one original
  slide `Bench Intro Video`.

Rules:

- Use the EXACT spellings `Bench Course Original`, `Bench Course Spring`,
  and `Welcome slide`.
- You MUST use the course form's cog / Actions `Duplicate` menu to create the
  new course — do NOT create `Bench Course Spring` from scratch via the
  `New` button on the eLearning kanban.
- Do NOT rename `Bench Course Original`. Do NOT delete it. Do NOT add extra
  slides to it.
- Do NOT add more than one new slide to `Bench Course Spring`. The new slide
  must be named `Welcome slide` (no extra trailing whitespace, exact case).
- Do NOT add the new slide to the original course.
