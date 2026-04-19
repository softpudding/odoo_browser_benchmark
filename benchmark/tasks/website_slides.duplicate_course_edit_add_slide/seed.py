"""Seed for website_slides.duplicate_course_edit_add_slide.

Creates a published training course `Bench Course Original` with a single
published video slide `Bench Intro Video`. The agent must:

  1. Open the course form,
  2. Duplicate the slide.channel via cog / Actions `Duplicate`,
  3. Rename the copy to `Bench Course Spring`,
  4. Add a new article/document slide titled `Welcome slide` on the copy.

Note: `slide.channel.user_id` defaults to `self.env.uid`. Seeds run under
SUPERUSER_ID (OdooBot), so a `create()` without explicit `user_id=admin.id`
auto-adds OdooBot as an attendee via `_action_add_members`. We pin user_id to
admin and explicitly wipe any auto-created `slide.channel.partner` residue.
"""


def setup(env):
    Channel = env["slide.channel"].with_context(active_test=False)
    Slide = env["slide.slide"].with_context(active_test=False)
    ChannelPartner = env["slide.channel.partner"].with_context(active_test=False)

    # --- Cleanup prior runs (original + any renamed copies / stale slides) ---
    stale_slides = Slide.search([
        ("name", "in", ["Bench Intro Video", "Welcome slide"]),
    ])
    if stale_slides:
        stale_slides.unlink()

    stale_channels = Channel.search([
        "|",
        ("name", "in", ["Bench Course Original", "Bench Course Spring"]),
        ("name", "=like", "Bench Course Original%"),
    ])
    if stale_channels:
        ChannelPartner.search([("channel_id", "in", stale_channels.ids)]).unlink()
        Slide.search([("channel_id", "in", stale_channels.ids)]).unlink()
        stale_channels.unlink()

    admin = env.ref("base.user_admin")

    # --- Create the original course ---------------------------------------
    original = env["slide.channel"].create({
        "name": "Bench Course Original",
        "description_short": "<p>Original Bench training course used as the template to be duplicated.</p>",
        "channel_type": "training",
        "visibility": "public",
        "enroll": "public",
        "is_published": True,
        "user_id": admin.id,
    })
    # Drop the OdooBot/admin auto-enrolled `slide.channel.partner` rows so
    # check.py's attendee-less expectation on the duplicated copy stays clean.
    ChannelPartner.search([("channel_id", "=", original.id)]).unlink()

    # --- One existing video slide on the original course -------------------
    env["slide.slide"].create({
        "name": "Bench Intro Video",
        "channel_id": original.id,
        "slide_category": "video",
        "video_source_type": "youtube",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "is_published": True,
        "completion_time": 0.05,  # ~3 minutes
        "sequence": 10,
    })
