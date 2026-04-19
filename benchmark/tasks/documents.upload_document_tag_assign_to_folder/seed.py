"""Seed for documents.upload_document_tag_assign_to_folder.

BLOCKED TASK — the `documents` addon is NOT present in this Odoo 19
Community checkout. The Documents app (Kanban of Workspaces + Upload
header button + per-document inspector with Folder / Tags / Owner
fields) is shipped exclusively in the Enterprise `documents` module.

Inspected the `odoo_benchmark` branch:
  - `addons/documents/` does NOT exist (`ls addons/documents/`
    → "No such file or directory").
  - `grep -rn "documents.document" addons/` returns only 5 files, all
    soft references from orthogonal modules:
      - `addons/spreadsheet/static/tests/helpers/data.js` (mock record
        factory that doesn't depend on the real model)
      - `addons/cloud_storage/models/ir_attachment.py` and
        `addons/cloud_storage_migration/models/ir_attachment.py`
        (migration helpers guarded by `env.get("documents.document")`)
      - `addons/account/tests/test_audit_trail.py` and
        `addons/account/models/ir_attachment.py` (same guarded
        handling).
    None of these register the `documents.document` model or any of
    the supporting `documents.folder` / `documents.tag` models.
  - No `/odoo/documents` client action, no `documents_kanban` view,
    no `documents_inspector` Owl component exist in this codebase.

Attempting to proceed would mean the agent navigates to `/odoo/documents`
and gets a 404 / "Action not found" error, so there is no value in
seeding folders / tags / files that can never be consumed through the
intended UI. This seed raises a clear error so the eval pipeline
records the blocker instead of silently creating orphan records.
"""


def setup(env):
    # Detect whether the Enterprise-only documents addon has been
    # vendored. If it ever becomes available, flip the branch below to
    # run the real seed.
    module = env["ir.module.module"].search(
        [("name", "=", "documents")], limit=1
    )
    has_documents = bool(module) and module.state == "installed"
    if not has_documents:
        raise RuntimeError(
            "BLOCKED: the `documents` addon is not installed "
            "(Enterprise-only). The Documents app / Workspaces UI is "
            "not reachable in this Odoo 19 Community checkout. See "
            "STATUS.md row 411 and RESULT.md for the re-enabling "
            "procedure."
        )

    # --- If / when enterprise addon is vendored, fill in the real seed ---
    # The sketch below documents what the real seed would do, kept as a
    # comment so future agents can flesh it out without rediscovering the
    # requirements.
    #
    # import base64
    # import os
    #
    # # 1. Ensure the Bench Folder workspace exists.
    # folder = env["documents.folder"].with_context(
    #     active_test=False
    # ).search([("name", "=", "Bench Folder")], limit=1)
    # if not folder:
    #     folder = env["documents.folder"].create({
    #         "name": "Bench Folder",
    #         "company_id": env.company.id,
    #     })
    # elif not folder.active:
    #     folder.active = True
    #
    # # 2. Ensure the 'invoice' tag exists and is scoped to the folder.
    # # In Enterprise Odoo 19, documents.tag is organized under
    # # documents.facet (tag categories) with folder_id on the facet.
    # facet = env["documents.facet"].search([
    #     ("folder_id", "=", folder.id),
    #     ("name", "=", "Type"),
    # ], limit=1) or env["documents.facet"].create({
    #     "name": "Type",
    #     "folder_id": folder.id,
    # })
    # tag = env["documents.tag"].search([
    #     ("facet_id", "=", facet.id),
    #     ("name", "=", "invoice"),
    # ], limit=1) or env["documents.tag"].create({
    #     "name": "invoice",
    #     "facet_id": facet.id,
    # })
    #
    # # 3. Drop a tiny sample file on disk so the browser file-picker can
    # # pick it up. Use a deterministic path so the oracle can reference it.
    # sample_path = "/tmp/bench_documents_sample.pdf"
    # if not os.path.exists(sample_path):
    #     # Minimal valid PDF header, good enough for Odoo's preview.
    #     with open(sample_path, "wb") as fh:
    #         fh.write(
    #             b"%PDF-1.4\n"
    #             b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    #             b"2 0 obj<</Type/Pages/Count 0>>endobj\n"
    #             b"xref\n0 3\n0000000000 65535 f\n"
    #             b"0000000009 00000 n\n0000000053 00000 n\n"
    #             b"trailer<</Size 3/Root 1 0 R>>\nstartxref\n91\n%%EOF\n"
    #         )
    #
    # # 4. Cleanup: remove any stale documents.document from prior runs
    # # so the per-folder uniqueness check (tag_ids contains invoice) is
    # # deterministic.
    # stale = env["documents.document"].with_context(
    #     active_test=False
    # ).search([
    #     ("folder_id", "=", folder.id),
    #     ("name", "like", "bench_documents_sample"),
    # ])
    # if stale:
    #     stale.sudo().unlink()
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "documents is vendored into addons/."
    )
