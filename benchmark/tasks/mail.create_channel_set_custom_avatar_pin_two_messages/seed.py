"""Seed data for mail.create_channel_set_custom_avatar_pin_two_messages.

Difficulty: medium (Category: deep_ui_interaction).
The agent must:
  - Create a public Discuss channel `engineering-hub` with a description.
  - Upload a custom avatar via the file picker (image_128).
  - Post three exact messages, in order.
  - Pin only the first and the third message; leave the middle PR message
    unpinned.

Seed responsibilities:
  - Wipe any prior `engineering-hub` channel from earlier runs.
  - Ensure the avatar PNG used for upload is present on disk at
    seed_artifacts/avatar.png. The file is committed in the repo so it
    is normally already on disk; this just re-creates it as a safety net
    if it ever went missing.

Note: this script is exec()'d as a string by the eval harness, so
`__file__` is NOT defined. Resolve the artifact path relative to the
benchmark package instead.
"""

import base64
import os


CHANNEL_NAME = "engineering-hub"
TASK_ID = "mail.create_channel_set_custom_avatar_pin_two_messages"

# 4x4 RGB blue PNG, 77 bytes; produced by PIL so Odoo's image
# processing (PIL.Image.open) accepts it.
AVATAR_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAFElEQVR4nGM0SjnBAANMDEgANwcARMoBZnEvszMAAAAASUVORK5CYII="
)


def _ensure_avatar_on_disk():
    """Make sure the avatar artifact exists on disk."""
    # The eval harness execs seed.py without setting __file__, so we
    # cannot use it. Resolve via the benchmark package layout instead.
    try:
        import benchmark
        bench_dir = os.path.dirname(os.path.abspath(benchmark.__file__))
    except Exception:
        # Fallback: assume CWD is the repo root.
        bench_dir = os.path.join(os.getcwd(), "benchmark")
    artifact_dir = os.path.join(bench_dir, "tasks", TASK_ID, "seed_artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    avatar_path = os.path.join(artifact_dir, "avatar.png")
    if not os.path.exists(avatar_path) or os.path.getsize(avatar_path) == 0:
        with open(avatar_path, "wb") as f:
            f.write(AVATAR_PNG_BYTES)


def setup(env):
    # 1. Cleanup any leftover channel(s) from previous runs.
    channels = env["discuss.channel"].search([("name", "=", CHANNEL_NAME)])
    if channels:
        msgs = env["mail.message"].search([
            ("model", "=", "discuss.channel"),
            ("res_id", "in", channels.ids),
        ])
        if msgs:
            msgs.unlink()
        channels.unlink()

    # 2. Make sure the avatar artifact exists on disk for the agent.
    _ensure_avatar_on_disk()
