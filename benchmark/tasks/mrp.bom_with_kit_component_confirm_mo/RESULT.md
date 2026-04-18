# mrp.bom_with_kit_component_confirm_mo — Result

**Difficulty:** hard
**Tier:** 3
**Row:** 377
**time_limit_sec:** 480, **step_limit:** 300

## Oracle (PASS)
- wall_clock: 21.8s, steps: 0 (JSON-RPC oracle)
- StateDiffF1: 1.0 (P=1.0, R=1.0)
- RequiredOpRecall: 1.0 (`mrp.production.action_confirm`)
- HarmfulWriteRate: 0.0, StrictClean: True
- Expected=3 create edits on `M-BENCH-KIT-001` (name / state=confirmed / product_qty=1.0), Matching=3, Missing=0, Extra=0
- Kit expansion verified: 3 raw moves (Bench Sub-A=1, Bench Sub-B=2, Bench Frame=1), zero reference to `Bench Kit` in raw moves.

## Browser-use (FAIL — calibration: correctly hard)
- wall_clock: 90.5s, 10 agent steps
- StateDiffF1: 0.0 (P=0.0, R=0.0)
- Expected=3 edits on entity_key `M-BENCH-KIT-001`; BU produced 3 edits on entity_key `WH/MO/00001` (the auto-generated sequence)
- RequiredOpRecall: 1.0 (BU did hit `action_confirm`)
- Postcondition failure: `Manufacturing order 'M-BENCH-KIT-001' not found`

**Trap hit:** BU typed `M-BENCH-KIT-001` into the **Source** field (in the Miscellaneous tab) instead of setting the MO reference. The "Reference" field on the draft MO form in Odoo 19 is actually the auto-generated `name` field (labelled in the breadcrumb as `WH/MO/00001`). There is NO editable "Reference" input in the visible form header — only the `origin` Char (Source) in the Miscellaneous tab. BU was tricked by the prompt wording "Reference field" into writing the value into the only Char input that looked like a reference — Source/Origin.

BU DID successfully:
- Select Bench Assembly product
- Auto-populate the Bench Assembly BoM
- Confirm the MO (state='confirmed')
- Phantom BoM auto-expanded into 3 raw components (Sub-A + Sub-B + Frame)

BU's final report also hallucinated success: the text "Reference: M-BENCH-KIT-001" in its summary does NOT correspond to the actual DB state — `mrp.production.name = 'WH/MO/00001'`.

## Task design
Hard deep-UI-interaction task with two combined traps:
1. **Phantom/kit BoM auto-expansion** — agent must trust that Confirm alone expands the kit, not manually edit the Components tab.
2. **"Reference" vs "Source" UI ambiguity** — Odoo 19 draft MO has no editable name input on the form; the only Char that looks like a reference is `origin` (Source). To set `name` the user must **type in the breadcrumb** (click the `WH/MO/00001` text in the top bar and overwrite it).

The check.py enforces `name == 'M-BENCH-KIT-001'` exactly, so any failure to retype the breadcrumb == FAIL. This produces the desired hard-tier behavior on BU.

## Calibration
Browser-use single-shot: FAIL with F1=0.0 on the first run. Genuine failure (BU hallucinated success but the DB state diverged). Task is hard enough for tier 3.
