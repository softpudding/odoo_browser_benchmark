# Difficulty Category Design

This document describes the five difficulty categories used to construct
benchmark tasks that reliably expose browser-agent weaknesses beyond simple
find-select-act patterns.

## Category 1: Closed-loop cross-module workflow

**Goal.** Force the agent to leave a module, complete work in a second module,
and return to finish the original workflow.  Most agents lose context when
navigating away and either forget to return or repeat steps.

**Design principle.** The task is only complete when *both* modules show correct
final state.  A partial completion in either module alone is scored as failure.

**Example.** `purchase_stock.receive_and_complete_backorder` — Confirm a
purchase order, do a partial receipt, create a backorder for the remaining qty,
then complete the backorder receipt.  The agent must navigate between Purchase
and Inventory, handle the backorder wizard, and ensure both receipts are marked
done.

---

## Category 2: Policy trap (tempting forbidden shortcut)

**Goal.** Present a situation where the naive/direct action *appears to work*
at the UI level but violates a business constraint.  The correct path requires
an extra preparatory step.

**Design principle.** The "wrong" path succeeds visually (button is clickable,
no hard error) but leaves the backend in a policy-invalid state.  The agent
must recognise the constraint and take the longer correct path.

**Example.** `sale.confirm_order_within_credit_limit` — A customer has a
credit limit.  The draft quotation exceeds it.  The agent must reduce qty on
the problematic line to bring the total within the limit, *then* confirm.
Simply clicking Confirm may succeed (warning only) but the expected_state
checks that the total is within the credit limit.

---

## Category 3: Side-effect trap (surgical edit)

**Goal.** Require a precise single-field change in a record that has many
interdependent fields.  The agent must avoid accidentally changing, recomputing,
or corrupting adjacent data.

**Design principle.** Seed the record with specific known values on every line.
The expected_state checks *all* lines, not just the edited one.  Any
unintended recomputation or accidental click on another line causes failure.

**Example.** `account.change_one_line_preserve_others` — A posted invoice must
be reset to draft, one specific line's quantity updated, then re-posted.  The
other three lines must remain byte-identical.

---

## Category 4: Recovery and rollback

**Goal.** Start from a *broken or wrong* state that the agent must first undo
before it can proceed.  This tests the ability to use cancel/reset workflows
rather than trying to edit locked records.

**Design principle.** The seed creates a confirmed/locked record with an
obvious error.  The agent cannot just edit it — it must first transition it
back (cancel, reset to draft) and then make the correction.

**Example.** `purchase.cancel_reissue_wrong_vendor` — A confirmed PO was sent
to the wrong vendor.  The agent must cancel it and create a new PO with the
correct vendor and identical lines.

---

## Category 5: Deep UI interaction

**Goal.** Stress the agent's ability to interact with complex, scrollable,
dynamically-loaded UI widgets — nested one2many tables, pagination, and
conditional controls.

**Design principle.** The target data is not visible on the initial viewport.
The agent must scroll within a nested widget (not the page) to find and edit
the correct row.  Distractors with similar names are placed near the target.

**Example.** `sale.edit_nested_line_in_long_order` — A sales order with 20
product lines.  The agent must scroll to a specific product deep in the list,
edit its quantity and discount, and confirm the order.
