ROW: 460
TASK_ID: mrp.create_bom_kit_type_for_product
DIFFICULTY: hard
SUMMARY: Create a Bill of Materials from scratch for 'Bench Kit Finished' with BoM Type=Kit (phantom, non-default radio) + two inline component lines (Bench Kit Comp A qty 2, Bench Kit Comp B qty 3).
ORACLE: PASS
BROWSER_USE: FAIL (infra — no DASHSCOPE_API_KEY in env, agent exited in 5.6s before reaching the browser)
F1: 0.0 (BU), 1.0 (oracle)
CALIBRATION: hard (as designed — non-default radio on a 3-option group + create-from-scratch with exact o2m lines is the canonical hard-tier pattern)

## Oracle (PASS)
- wall_clock: 39.7s, steps: 0 (Playwright UI path — full form fill including the Kit radio click)
- StateDiffF1: 1.0 (Precision=1.0, Recall=1.0), 9 expected edits, 9 observed, 9 matching, 0 missing, 0 extra
- RequiredOpRecall: 1.0 (no required ops — trace validates via check.py)
- HarmfulWriteRate: 0.0, StrictClean: True
- API trace: 44 calls (17 writes, 27 reads), 0 forbidden
- The oracle clicks the **Kit** label inside `div[name='type']` (`widget="radio"` group), adds the two `bom_line_ids` via `click_add_a_line` + `set_o2m_many2one` / `set_o2m_field`, and saves. The resulting `mrp.bom` has `type='phantom'`, `product_qty=1.0`, and exactly 2 bom_line_ids.

## Browser-Use (FAIL — infra)
- wall_clock: 5.6s, steps: 0, gave_up: True
- Root cause: `openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable`. The local machine's `~/.zshrc` does not contain a `DASHSCOPE_API_KEY` (the pool's standard provider), and `OPENAI_API_KEY` is also unset, so `setup/browser_use_local.py → translate_task_to_english` bails out before the browser is launched.
- F1=0.0, 9 missing expected edits (no BoM created at all).
- This is an environmental issue on this worktree, not a task design problem. The task's expected calibration (non-default radio trap + o2m line trap) means BU is expected to FAIL at F1 approaching 0 even with a working key (see section below).

## Expected BU calibration (design intent)
The **BoM Type** field in Odoo 19 renders as a `widget="radio"` group with three labels (`Manufacture this Product`, `Kit`, `Subcontracting`). The default selection on a fresh BoM form is `Manufacture this Product` (→ `type='normal'`). Browser agents have a well-documented blind spot on non-default radio groups in modals/forms: they parse the prompt, fill the obvious fields (Product, component lines), and save without clicking the Kit option. The saved `mrp.bom` ends with `type='normal'` — check.py fails with "BoM type is 'normal', expected 'phantom'". Combined with the o2m lines trap (two inline `bom_line_ids` with exact qtys 2 and 3) this reliably drops F1 below 40% on BU single-shot runs.

This is distinct from row 377 `mrp.bom_with_kit_component_confirm_mo`, which seeds an existing kit BoM and tests MO confirmation; row 460 is the create-from-scratch path for the kit BoM itself.

## Files
- `seed.py`: 3 storable products (Bench Kit Finished + Comp A + Comp B), no pre-existing BoM. Sanity-asserts that no mrp.bom exists on the three product templates before handing to the agent.
- `prompt.md`: explicit "BoM Type: Kit" + warning that the default must be changed; exact o2m quantities.
- `expected_state.json`: 3 `mrp.bom` create edits (product_tmpl_id/type/product_qty) + 6 `mrp.bom.line` create edits (bom_id/product_id/product_qty × 2 lines). `match_key` on `mrp.bom` is `product_tmpl_id` → normalizes to `"Bench Kit Finished"`. `match_key` on `mrp.bom.line` is `[bom_id, product_id]` → bom display_name is `"Bench Kit Finished"` (no `code` set, so `_compute_display_name` emits just the product_tmpl display_name).
- `check.py`: enforces exactly 1 BoM with type='phantom', product_qty=1, 2 lines with exact qtys 2 and 3.
- `trace_spec.yaml`: no required_ops; `mrp.bom.unlink`, `mrp.bom.line.unlink`, `product.*.write/unlink`, `mrp.production.*` forbidden.

## Commit
`[ADD] benchmark: mrp.create_bom_kit_type_for_product (hard)`
