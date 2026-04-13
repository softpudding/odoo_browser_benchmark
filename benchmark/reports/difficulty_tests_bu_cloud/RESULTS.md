# Browser-Use Cloud vs DashScope Comparison

Date: 2026-04-13
Agents: browser-use 0.12.6 cloud (bu-latest) vs DashScope (qwen-vl-max)
Odoo: 19.0, database=benchmark_validate

## Results Summary

| # | Task | DashScope @50 steps | BU Cloud @50 steps | BU Cloud @200 steps |
|---|------|--------------------|--------------------|---------------------|
| 1 | Simple SO (1 product) | **PASS** (19) | **PASS** (13) | — |
| 2 | Multi-line SO (3 products + confirm) | **PASS** (22) | **FAIL** (50 max) | **PASS** (94) |
| 3 | Project + milestones + tasks + stage | **FAIL** (60 max) | **FAIL** (60 max) | **PASS** (74) |
| 4 | SO inline edit + discount + tabs | **FAIL** (50 max) | **FAIL** (50 max) | **PASS** (74) |
| 5 | Website page rename | **FAIL** (40 max) | **PASS** (17) | — |

## Key Findings

### 1. Step budget is the critical variable
- Tests 2, 3, 4 all PASS with 200-step budget but FAIL with 50-60
- This means the tasks ARE solvable, but agents need many retries/recovery cycles
- **Implication for benchmark:** step_limit should be a scored metric, not just a hard cutoff. An agent that completes in 20 steps is strictly better than one that takes 94.

### 2. Different providers have different strengths
- **BU Cloud** is faster on simple tasks (13 vs 19 steps for Test 1)
- **DashScope** handles multi-line autocomplete better (22 steps for Test 2 vs BU Cloud's 94)
- **BU Cloud** handles non-standard UI better (passed Test 5 website rename; DashScope failed)
- Both fail equally on feature discovery (Test 3) and inline editing (Test 4) at low step budgets

### 3. Recovery from loops is the main differentiator
- BU Cloud hit loop detection 8+ times on Test 2 before eventually recovering
- DashScope rarely loops but sometimes gets permanently stuck
- The ability to recover from a wrong action is more important than avoiding the wrong action

### 4. Autocomplete interaction is the hardest common pattern
- Both agents struggle with Odoo's Many2one search dropdowns
- The sequence: click field → type → wait for dropdown → select → blur is fragile
- Adding multiple products multiplies this fragility (Test 2: 3 products = 3x autocomplete)

## Failure Mode Details (BU Cloud)

### Test 2 @50 steps: Autocomplete field committing
- Successfully added Large Desk and Office Chair
- Failed on Whiteboard: autocomplete didn't commit properly
- Attempted "Confirm" with incomplete 3rd line → "Missing required fields" error
- Spent remaining steps trying to fix the error

### Test 3 @60 steps: Milestone creation discovery
- Created project, enabled milestones in settings
- Found milestone creation eventually but struggled with date picker
- Couldn't complete all milestones + tasks within budget

### Test 4 @50 steps: Inline editing + tab navigation
- Created SO, added product
- Struggled to click into description cell for inline editing
- Eventually figured it out but ran out of steps before reaching tab navigation

## Implications for Benchmark Design

1. **Use tiered step limits:**
   - Easy tasks: 50 steps
   - Medium tasks: 100 steps  
   - Hard tasks: 200 steps

2. **Step efficiency is a first-class metric:**
   - Two agents that both succeed should be ranked by step count
   - This naturally separates good UI understanding from brute-force retry

3. **Report pass@k:**
   - pass@50, pass@100, pass@200 gives a step-efficiency curve
   - More informative than a single pass/fail

4. **Both providers are valid baselines:**
   - Different failure profiles make the benchmark more interesting
   - Neither dominates the other across all tasks
