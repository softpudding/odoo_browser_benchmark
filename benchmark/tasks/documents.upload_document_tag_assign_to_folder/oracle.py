"""Oracle for documents.upload_document_tag_assign_to_folder.

BLOCKED TASK — the Documents app / Workspaces UI is shipped by the
Enterprise-only `documents` addon, which is NOT vendored in this
Odoo 19 Community checkout. The oracle exits with a clear error so
the harness records the blocker instead of producing spurious results.

To flesh out once the enterprise documents addon is vendored:
  1. Navigate to `/odoo/documents`.
  2. Expect the Documents Kanban with a left Workspaces tree. Click
     the `Bench Folder` node.
  3. Click the header **Upload** button. A `<input type='file'>` is
     triggered; the harness's `page.expect_file_chooser()` should be
     set up BEFORE the click. Supply `/tmp/bench_documents_sample.pdf`.
  4. Wait for the uploaded card to appear in the Kanban (polling for
     its presence is safer than a fixed sleep — Odoo fires an RPC and
     re-renders).
  5. Click the uploaded card; the right-hand inspector panel opens.
  6. In the `tag_ids` many-to-many field, type `invoice` and pick the
     suggestion.
  7. In the `owner_id` many2one field, type `Administrator` and pick
     the suggestion.
  8. Click outside the panel (or press Escape then Tab) to commit the
     write — Documents auto-saves on blur.

Typical selectors on the Enterprise Documents client:
  - `.o_documents_view` — Kanban root container.
  - `.o_search_panel` / `.o_documents_folder_section` — Workspaces tree.
  - `.o_control_panel_main_buttons button:has-text("Upload")` — the
    header Upload action (triggers a hidden `<input type='file'>`).
  - `.o_documents_inspector` — the right-hand side-panel on card click.
  - `.o_documents_inspector [name='tag_ids']` — tag autocomplete.
  - `.o_documents_inspector [name='owner_id']` — owner many2one.

Selector names have shifted between Odoo versions — confirm against
the current enterprise source before writing selectors.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: the Documents app (/odoo/documents) is not "
        "available in this Odoo 19 Community checkout "
        "(Enterprise-only). Oracle body intentionally short-circuits. "
        "See STATUS.md row 411."
    )


run_oracle(oracle)
