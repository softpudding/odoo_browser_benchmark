"""Cleanup for documents.upload_document_tag_assign_to_folder.

BLOCKED TASK — `documents` addon is not installed in this Community
checkout, so there is nothing to clean up. The guard below turns this
into a no-op that stays safe if the module ever becomes available
without the rest of the task being fleshed out.
"""


def cleanup(env):
    module = env["ir.module.module"].search(
        [("name", "=", "documents")], limit=1
    )
    if not module or module.state != "installed":
        return

    # Once the enterprise addon is vendored, cleanup would look like:
    #
    # folder = env["documents.folder"].with_context(
    #     active_test=False
    # ).search([("name", "=", "Bench Folder")], limit=1)
    # if folder:
    #     docs = env["documents.document"].with_context(
    #         active_test=False
    #     ).search([("folder_id", "=", folder.id)])
    #     if docs:
    #         attachments = docs.mapped("attachment_id")
    #         docs.sudo().unlink()
    #         attachments.sudo().unlink()
    #     tags = env["documents.tag"].search([
    #         ("facet_id.folder_id", "=", folder.id),
    #         ("name", "=", "invoice"),
    #     ])
    #     tags.sudo().unlink()
    #     facets = env["documents.facet"].search([
    #         ("folder_id", "=", folder.id),
    #     ])
    #     facets.sudo().unlink()
    #     folder.sudo().unlink()
    #
    # import os
    # sample_path = "/tmp/bench_documents_sample.pdf"
    # if os.path.exists(sample_path):
    #     try:
    #         os.remove(sample_path)
    #     except OSError:
    #         pass
