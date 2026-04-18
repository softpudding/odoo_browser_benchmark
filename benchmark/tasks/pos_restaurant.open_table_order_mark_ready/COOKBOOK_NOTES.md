# pos_restaurant.open_table_order_mark_ready — Odoo 19 quirks

## pos_restaurant is NOT in the base snapshot — install on demand

`pos_restaurant` is a separate module (depends on `point_of_sale`) and is
NOT listed in `benchmark/base_modules.txt`. Seeds must install it before
using `restaurant.floor` / `restaurant.table` / `restaurant.order.course`
or setting `pos.config.module_pos_restaurant=True`:

```python
mod = env["ir.module.module"].search([("name", "=", "pos_restaurant")], limit=1)
if mod and mod.state != "installed":
    mod.button_immediate_install()
```

## pos.config auto-spawns a default floor + table when restaurant flag is set

`pos_restaurant/models/pos_config.py::_setup_default_floor` fires on both
`create` and `write` when `module_pos_restaurant=True`. It creates a
`restaurant.floor` named after the company and a single `restaurant.table`
with `table_number=1`. To control the deterministic floor/table identity
used as a state-diff match_key, the seed must:

1. Create the `pos.config` with `module_pos_restaurant=True`.
2. Capture `config.floor_ids` (the auto-created default floor).
3. Write `floor_ids=[(5, 0, 0)]` on the config to detach the defaults.
4. Unlink the auto-created tables and floors.
5. Create the deterministic `restaurant.floor` + `restaurant.table`.

Order matters: the floor has an `ondelete` guard
(`_unlink_except_active_pos_session`) that raises if any of the floor's
`pos_config_ids` has a non-closed session. As long as `pos.session` has
not been created yet, and the config has been detached (`floor_ids` on
the config is empty), the auto-floor is unlinkable.

## restaurant.order.course.fired = True is the "mark ready / kitchen-fire" signal

Odoo 19 Community does not have an explicit `kitchen_done` flag on
`pos.order`. The per-course ready state is:

- `restaurant.order.course.fired` (Boolean, default False)
- `restaurant.order.course.fired_date` (Datetime, auto-set on write when
  `fired` flips True and no date is set yet)

In the kiosk UI:

- Clicking the **primary action-pad Send/Order button** (class
  `.submit-order`, labelled with a per-category count summary) calls
  `sendOrderInPreparationUpdateLastChange`, which sets
  `firstCourse.fired = true` for the first non-fired course on the
  order (see `pos_restaurant/static/src/app/services/pos_store.js`).
- The separate **Fire Course <N>** button (class `.fire-btn`) also sets
  `course.fired = true` for the currently selected course; appears only
  when there are no unsent lines AND the selected course is ready to fire
  (`displayFireCourseBtn`).
- The `Fired` badge (`rounded text-bg-info fs-6 px-2`) on the course
  header is the visual confirmation.

Courses are NOT auto-created when lines are added. They only exist after
the user clicks the **Course** control button (`this.pos.addCourse()`),
which wraps existing lines into Course 1 + creates an empty Course 2.
If a course does not exist when Send is clicked, `firstCourse` is
undefined and the side effect is skipped. Tasks that want the
`fired=True` signal must arrange for at least one course to exist before
the Send click — typically by instructing the agent to click Course
between two product additions.

## pos.order.pos_reference is auto-generated per-run — do NOT use as match_key

The oracle-set `pos_reference` string and browser-use's auto-generated
`<pos_config_id>-<pos_session_id>-<nnnnnn>` pattern diverge across runs.
Using `pos_reference` as a state-diff match_key in `state_spec.yaml`
yields F1=0 for any successful browser-use run that solves the task
independently. Use `table_id` (which normalises to the
`<floor_name>, <table_number>` display — e.g. `Main Floor, 1`) or the
combination of `table_id` + stable seeded entity references.

## restaurant.table display_name = "<floor.name>, <table_number>"

`restaurant.table._compute_display_name` concatenates
`floor.name`, `, `, `table_number` (not "T<n>", not `f"{name}-T{n}"`).
A table with `table_number=1` on `Main Floor` yields display
`Main Floor, 1`. The kiosk label shown on the floor-plan tile is just
`1` (or whatever `table_number` is) — the prompt can say "T1" as a
human-readable tag but the UI selector hits the numeric label.

## Browser-use calibration notes

Single-shot BU run: 102.7s, check.py PASS. The kiosk UI is clearly
labelled ("Course" button, "Fire Course N" button, "Send" big primary).
BU does get momentarily confused between "Fire Course N" and
"Send/Order", clicking "Fire Course 2" first and then "Fire Course 1"
to correct — both actions together still land the order with at least
one fired course on the correct table. This means the task is
**doable** for BU and we should grade on check.py, not on the
sometimes noisy state_diff order name.
