# Cookbook notes - hr.create_department_assign_manager_two_employees

## New / reinforced quirks

- **Department m2o autocomplete duplicate-create trap.** When an agent
  types a department name into `hr.employee.department_id` that matches
  an existing (just-created) `hr.department`, the Owl autocomplete shows
  BOTH the existing row AND a `Create "<name>"` quick-create item. If
  the agent clicks the quick-create item (or hits Enter before the
  existing row is highlighted), Odoo silently creates a second
  `hr.department` with the same name. Name uniqueness is NOT enforced
  on `hr.department`, so nothing flags the duplicate. Browser-use did
  exactly this on Worker 2 of our run: Worker 1 went into dept id=2
  (with manager), Worker 2 went into dept id=3 (no manager).
- **Seeding employees with `department_id=False`** is supported — no
  constraint forces employees into a department — so a clean "agent
  sets the department for the first time" task needs no seed
  pre-department; just omit the field (or pass `False`) and the form's
  Department field renders empty.
- The diff engine emits a `#dup1` entity-key suffix when two records
  share the same match_key values (here `name=Bench Ops`). Our
  `expected_state.json` still keys on the plain `["Bench Ops"]` and the
  primary dup carries those edits; the second dup's edits show up as
  Extras, hurting precision/F1 even though the expected edits all match.
- **check.py must assert member count**, not just "workers have a
  department named X". Without the count check, the duplicate-dept
  split would silently pass: Worker 1 is in a dept named Bench Ops,
  Worker 2 is in a (different) dept named Bench Ops — both satisfy
  a name-only invariant.

## Differentiation from row 321 (three_employees)

- 2 workers vs 3 engineers.
- Entity names: `Bench Dept Manager` / `Bench Dept Worker 1|2` /
  `Bench Ops` vs `Mike Manager` / `Eng One|Two|Three` /
  `Bench Engineering`.
- Seed creates NO pre-existing department for the employees (row 321
  seeds an `Operations` department); agent SETS the department on a
  fresh employee row rather than reassigning from one department to
  another. Same capability tested (multi-step create-then-edit nav),
  different surface.
- Can run back-to-back with row 321 in the same DB without seed
  collisions — all entity names are disjoint.

## Browser-use behavior

- BU completes the navigation sequence (department creation + 2
  employee form edits) but on the autocomplete for Worker 2's
  Department field it clicked `Create "Bench Ops"` instead of the
  existing `Bench Ops` row, forking into a second department.
  Wall clock 177s; steps counted as 0 because BU uses `agent.run` not
  the step-by-step BU stepper. No forbidden ops.
