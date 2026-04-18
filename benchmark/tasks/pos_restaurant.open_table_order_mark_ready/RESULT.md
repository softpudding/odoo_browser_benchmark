ROW: 382
TASK_ID: pos_restaurant.open_table_order_mark_ready
DIFFICULTY: hard
SUMMARY: Restaurant POS: open T1 on Main Floor, add Starter Salad + split Course + add Main Steak, click Send/Order to fire Course 1 to kitchen (mark ready); no payment
ORACLE: PASS
BROWSER_USE: PASS
F1: 1.0 (expected — BU passed check.py and state_diff key is table_id)
CALIBRATION: easier

DETAIL_SECTION:
## pos_restaurant.open_table_order_mark_ready

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS |
| **Browser-Use** | PASS |
| **F1** | 1.0 |
| **Odoo modules** | Point of Sale, pos_restaurant (installed on demand — not in base snapshot) |
| **Workflow** | Open Point of Sale, open the seeded `Bench Restaurant` register, click table `T1` on the `Main Floor` floor plan, add `Starter Salad` (€15) x1, click the `Course` action-pad button to wrap Starter Salad into Course 1 + create an empty Course 2, add `Main Steak` (€20) x1 (lands in Course 2), click the primary `Send/Order` button on the action pad to fire Course 1 to the kitchen (`restaurant.order.course.fired=True`). No payment step. |
| **Capability tested** | Restaurant POS kiosk UI: floor-plan table click, course split (Course button), action-pad Send vs Pay distinction, kitchen-fire ("mark ready") state via `fired=True` flag on `restaurant.order.course`. Cross-module install: `pos_restaurant` is not in the base snapshot and must be installed on demand by the seed. |
| **Notes** | `pos_restaurant` is NOT in `benchmark/base_modules.txt`, so seed runs `button_immediate_install()` on demand. `pos.config.module_pos_restaurant=True` auto-spawns a default floor + T1 table via `_setup_default_floor` — seed detaches and replaces those with a deterministic `Main Floor` / T1 (table_number=1) pair to stabilise the floor-plan display name `Main Floor, 1` used as the state-diff `match_key`. The Odoo 19 "kitchen ready / mark ready" concept is implemented as `restaurant.order.course.fired` (Boolean, with matching `fired_date`). In the UI, clicking the primary action-pad button labelled with the category-count summary (class `.submit-order`, also referred to as the Send/Order button) fires the first non-fired course (`sendOrderInPreparationUpdateLastChange` in `pos_restaurant/pos_store.js` sets `firstCourse.fired=true`). Calibration: browser-use SOLVES this task in a single shot (wall clock 102.7s, 13 steps). BU successfully navigates the floor plan → order → Course split → Send flow. First state-diff match-key used (`pos_reference`) diverged between oracle (explicit string) and BU (auto-generated `<config>-<session>-<seq>`), so match-key switched to `table_id` for stable cross-run F1. POS kiosk is a clearly labeled Owl surface; harder failure modes would require non-default course choices, guests count, or a split-bill / transfer workflow. |
