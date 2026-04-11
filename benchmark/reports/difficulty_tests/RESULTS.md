# Browser-Use Difficulty Calibration Results

Date: 2026-04-11
Agent: browser-use 0.12.6, provider=dashscope, model=qwen-vl-max
Odoo: 19.0 (branch), database=benchmark_validate

## Summary

| # | Task | Difficulty | Steps | Result | Key Failure Mode |
|---|------|-----------|-------|--------|-----------------|
| 1 | Create SO, pick customer + 1 product | Medium | 19 | **PASS** | Minor loop on "Add a product" (5 retries before recovery) |
| 2 | Create SO, 3 products + custom prices + confirm | Medium-Hard | 22 | **PASS** | Clean execution |
| 3 | Project + milestones + tasks + kanban stage change | Hard | 60 (max) | **FAIL** | Could not find milestone creation UI |
| 4 | SO + inline description edit + discount + tab navigation | Hard | 50 (max) | **FAIL** | Could not edit inline cells or navigate form tabs |
| 5 | Website page rename via website editor | Hard | 40 (max) | **FAIL** | Lost in website builder, could not find page name field |

## Detailed Failure Analysis

### Test 3: Project + Milestones (FAIL)

**Task:** Create project "Website Redesign", enable milestones, create 2 milestones with deadlines, create 3 tasks assigned to milestones, move one task to "Done" stage.

**What succeeded:**
- Created the project
- Enabled milestones in project settings

**Where it failed:**
- Could not discover that milestones are created from the project settings form, not via the main "New" button
- Repeatedly clicked "New" (which creates tasks, not milestones) and got stuck in a 20+ step loop
- Never reached task creation or kanban manipulation

**Root cause:** Feature discovery failure. The agent doesn't understand that different Odoo features have different creation paths — milestones are managed from project settings, not from the main list/kanban view.

### Test 4: SO Inline Editing + Tabs (FAIL)

**Task:** Create quotation, add product, edit product description inline, set 10% discount, add second product, navigate to "Other Info" tab, set payment terms, save.

**What succeeded:**
- Created quotation, selected customer
- Added first product "Large Desk"
- Attempted to edit description (partially)

**Where it failed:**
- Could not click into the product description cell for inline editing
- Could not find/interact with the discount field on order lines
- Could not add second product after failing on the first line's details
- Never found or clicked the "Other Info" tab
- Never saved

**Root cause:** Inline tree editing failure. Odoo's one2many list views require precise click targeting (click cell → enters edit mode → type → blur). The agent couldn't transition cells into edit mode. Tab navigation also failed — the agent didn't recognize `.o_notebook .nav-link` tabs as clickable navigation.

### Test 5: Website Page Rename (FAIL)

**Task:** Navigate to Website > Site > Pages, find "Home" page, change its name to "Welcome".

**What succeeded:**
- Logged in, navigated to Website app
- Found Site > Pages menu
- Located the "Home" page
- Opened the page in edit mode

**Where it failed:**
- Spent 20+ steps searching for the page name field in the website editor
- Tried scrolling, clicking "Style" tab, "Blocks" tab, repeatedly
- Never found that page properties are accessed via a different mechanism (the page manager or URL-based rename)
- Stuck in a loop: "look for settings panel" → fail → repeat

**Root cause:** Non-standard UI. The Odoo website builder has its own editor chrome (snippets, blocks, styles) that doesn't follow the standard backend form pattern. The page "name" isn't editable in the visual editor — it's a property accessible elsewhere. The agent has no mental model for this divergence.

## Identified Failure Pattern Categories

### Category 1: Feature Discovery
Tasks where the correct UI path is non-obvious. The agent tries the most visible action (e.g. "New" button) and doesn't explore alternative paths.

**Examples:** Milestone creation, accessing page properties, finding hidden settings.

### Category 2: Inline Cell Editing
Tasks requiring interaction with Odoo's one2many inline editable trees. Clicking a cell to enter edit mode, then typing, then bluring to save.

**Examples:** Editing SO line descriptions, setting discounts, modifying quantities in nested lists.

### Category 3: Form Tab Navigation
Tasks requiring switching between tabs on Odoo backend forms (`.o_notebook`). The agent doesn't recognize these as navigation elements.

**Examples:** "Other Info" tab on SO, "Inventory" tab on products, "Accounting" tab on invoices.

### Category 4: Non-Standard Editor UI
Tasks involving Odoo's website builder, which has completely different interaction patterns from the backend.

**Examples:** Page renaming, snippet editing, theme customization.

### Category 5: Multi-Step State Dependencies
Tasks where step N depends on step N-1 being in a specific state. When the agent fails at one step, all subsequent steps are impossible.

**Examples:** Create milestone → assign task to milestone, set product → edit its inline details.

## Implications for Benchmark Design

1. **The benchmark has clear discriminative power.** Easy tasks (public forms, simple SO creation) pass. Hard tasks (inline editing, feature discovery, non-standard UI) fail consistently.

2. **Difficulty tiers are real.** The spec's easy/medium/hard buckets map cleanly to observed pass/fail patterns.

3. **Recommended difficulty distribution for 50 tasks:**
   - Easy (10): Public website forms, simple record creation
   - Medium (20): Backend CRUD with many2one search, basic workflows
   - Hard (20): Inline editing, tab navigation, multi-step workflows, settings discovery

4. **Most diagnostic failure modes for the paper:**
   - Inline tree editing (Category 2) — precise, reproducible, measurable
   - Feature discovery (Category 1) — tests agent planning/exploration
   - Tab navigation (Category 3) — tests UI understanding
