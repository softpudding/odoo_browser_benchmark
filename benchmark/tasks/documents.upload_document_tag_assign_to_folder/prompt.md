# Upload a document to a folder, tag it, assign owner (BLOCKED)

> **Note**: This task is BLOCKED because the `documents` addon is an
> **Odoo Enterprise** module that is NOT vendored in this Odoo 19
> Community checkout. The Documents app (Kanban of folders + Workspaces
> tree, the `Upload` header button, the per-document inspector side
> panel with Folder / Tags / Owner fields, and the `documents.document`,
> `documents.folder`, `documents.tag` models) all ship exclusively in
> the Enterprise `documents` addon.
>
> What is present in Community:
> - `addons/mail/` and `ir.attachment` provide generic file upload on
>   chatter threads, but not the Documents workspace UI.
> - `addons/website_slides/` mentions the word "documents" in the
>   context of course content (unrelated).
> - `addons/spreadsheet/` and `addons/cloud_storage/` reference
>   `documents.document` as a soft dependency but ship no model.
>
> There is no `addons/documents/` directory, no `documents.document`
> model, no `documents.folder` / `documents.tag` models, no
> `/odoo/documents` client action, and no `documents_kanban` view in
> this codebase. `ls addons/documents/` returns
> "No such file or directory".
>
> The original task intent is preserved below for future re-scoping
> when the enterprise addon is vendored.

You will upload a file to the Documents app, place it in a named
folder, tag it, and set the owner.

## Phase 1 — Open the Bench Folder

1. Open **Documents** from the main app grid.
2. In the left **Workspaces** tree, click **Bench Folder**.

## Phase 2 — Upload the file

3. Click the **Upload** header button.
4. In the native file picker, select the seeded file (path provided by
   the harness as `/tmp/bench_documents_sample.pdf`).
5. Wait for the upload progress indicator to finish.

## Phase 3 — Tag and assign owner

6. Click the uploaded card to open the right-hand inspector panel.
7. In the **Tags** many-to-many, pick `invoice` (one of the seeded
   tags on Bench Folder).
8. In the **Owner** field, pick `Administrator`.
9. Save (Documents auto-saves on blur; click outside the panel or
   press Tab to commit).

## Rules

- Final state: one `documents.document` record whose
  `folder_id.name == 'Bench Folder'`, `tag_ids` contains the tag named
  `invoice`, `owner_id` is the admin user, and whose attached
  `ir.attachment.name` matches the uploaded file.
- The seeded folder `Bench Folder` and tag `invoice` must remain
  unchanged (do NOT rename or delete them).
- No other documents should be created by this task.
