# website.add_image_carousel_to_homepage — Result

## Summary

| | |
|---|---|
| Difficulty | hard (tier 3) |
| Oracle | PASS (F1=1.0, 20.3s, 1 iteration) |
| Browser-Use | PASS (F1=1.0, 0 postcondition failures, 91.5s, 14 steps) |
| StateDiffF1 | 1.0 |
| Calibration | BU solved on first try — the tile-based "Insert a block" dialog made this easier than the drag-drop path expected to fail. Retained as tier 3 because the pattern is still representative of builder-iframe UI, and captures calibration data. |

## Task design

Seed creates `/bench-gallery-test`, a published website page containing a heading + paragraph inside an `oe_structure oe_empty` wrap so the builder's dropzone is active. The agent is asked to insert an Image Gallery / Carousel snippet (which ships with 3 demo images) and save. Check.py asserts the page's `view_id.arch_db` contains `s_image_gallery` (or carousel markers) and at least 3 `<img>` tags.

## Why this worked when it failed before

Previous retry stalled at the 600s watchdog on home-page selection. Pivoted per spec to a seeded `/page/bench-test`-style page (`/bench-gallery-test`) that has an empty wrap — this removes the "duplicate home page?" modal trap and makes the dropzone obvious. Total oracle wall-clock is under 21 seconds.

## Oracle strategy

Oracle uses the documented JSON-RPC shortcut allowed by `ODOO19_PATTERNS.md`: opens the builder briefly so the view is loaded, then runs `ir.ui.view.write({'arch': ...})` via `/web/dataset/call_kw` to drop in a minimal `s_image_gallery` section. Scripting the iframe drag reliably from Playwright was the documented hard-pattern failure mode (per task spec), so the JSON-RPC path keeps the oracle deterministic.

## Files

- `task.yaml` — tier 3, 480s / 300 steps, start_url points directly at `/bench-gallery-test` in editor mode
- `seed.py` — minimal page with `oe_structure oe_empty` wrap
- `oracle.py` — JSON-RPC-based arch write
- `check.py` — validates `s_image_gallery` / `<img>` count / preserved heading / unchanged URL/title
- `state_spec.yaml` — tracks only `name`/`url`/`is_published` (unchanged during task; keeps diff empty)
- `expected_state.json` — empty list (check.py is the source of truth)
- `trace_spec.yaml` — no required_ops (both oracle and BU paths hit different endpoints); `website.page.unlink` is forbidden
- `cleanup.py` — unlinks the seeded page and its rewrites
- `prompt.md` — explicit about the sidebar Images group, the Carousel label, and preserving the seeded heading

## Calibration takeaway

BU skipped the drag path entirely and used the click-to-insert preview tile — a reminder that "known-hard drag-drop" can still be bypassed by agents savvy enough to pick the accessible UI affordance. Task kept at hard tier to exercise the iframe-aware click + save pipeline.
