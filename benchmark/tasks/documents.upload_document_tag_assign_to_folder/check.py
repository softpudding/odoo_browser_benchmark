"""Postcondition checks for documents.upload_document_tag_assign_to_folder.

BLOCKED TASK — `documents` addon is not vendored in this Odoo 19
Community checkout, so the task cannot run end-to-end. The check
below returns a clear failure string so the eval pipeline flags it
rather than appearing as a spurious PASS.
"""


def check(env):
    module = env["ir.module.module"].search(
        [("name", "=", "documents")], limit=1
    )
    if not module or module.state != "installed":
        return [
            "BLOCKED: `documents` addon is not available in this "
            "Odoo Community checkout (Enterprise-only). Task cannot "
            "be validated end-to-end. See STATUS.md row 411 for "
            "re-enabling notes."
        ]

    # Concrete validation to add once the addon is vendored:
    #   - exactly one `documents.folder` named 'Bench Folder' exists.
    #   - exactly one `documents.tag` named 'invoice' exists under
    #     that folder's facet.
    #   - at least one `documents.document` exists with
    #     folder_id == Bench Folder,
    #     tag_ids includes the 'invoice' tag,
    #     owner_id == the admin user (ref("base.user_admin")),
    #     and a non-empty linked ir.attachment with a matching name.
    #   - no other `documents.document` records were created in
    #     Bench Folder during this run (avoid side-effects).
    return [
        "BLOCKED: documents addon became available but check body "
        "not yet implemented. See STATUS.md row 411 for context."
    ]
