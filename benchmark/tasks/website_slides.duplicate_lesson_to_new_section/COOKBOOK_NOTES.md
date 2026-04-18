# website_slides cookbook notes

- `slide.slide.is_category=True` rows ARE the sections of a `slide.channel`;
  there is no separate section model.
- A lesson's `category_id` (its section) is **computed**, not directly writable.
  It is derived from the sequence ordering: a non-category slide belongs to
  the most recent prior `is_category=True` slide in sequence order on the
  same channel. To move a lesson to another section, change its `sequence`
  to fall after that section's marker (and before the next one).
- `slide.slide.copy_data()` deliberately resets `sequence=0` on the duplicate
  so the copy lands at the very top as an uncategorized slide. The agent
  must then re-sequence it (or pick a section) to assign it.
- New `is_category` slides created via JSON-RPC default to
  `slide_category='document'` (the field's default) and `website_published=True`,
  even though the section row is conceptually neither. Oracle diff
  expectations should account for this.
- Browser-use failure mode observed: when asked to "duplicate the lesson
  via Actions menu", the agent tends to land on the COURSE form's cog menu
  and duplicate the whole `slide.channel` (sometimes multiple times),
  rather than navigating into the slide.slide form first.
