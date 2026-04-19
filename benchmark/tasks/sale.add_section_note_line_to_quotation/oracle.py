"""Oracle for sale.add_section_note_line_to_quotation.

Open the seeded draft quotation SO-BENCH-STRUCT for Bench Struct Co and
append two non-product lines using the **Add a section** and
**Add a note** footer controls on the Order Lines list (the default
control is **Add a product**, which is NOT what we want). Save the
quotation, do not confirm.
"""

from benchmark.oracle_helpers import (
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_no_loading,
    _wait_for_ready,
)


SECTION_TEXT = "Phase 1"
NOTE_TEXT = "Delivery by end of month"


def _open_quotation(page):
    """Resolve the seeded SO id via JSON-RPC and navigate to the form."""
    so_id = page.evaluate(
        """async () => {
            const res = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'sale.order',
                        method: 'search_read',
                        args: [[['name', '=', 'SO-BENCH-STRUCT']], ['id']],
                        kwargs: {},
                    },
                }),
            });
            const json = await res.json();
            if (json.error) throw new Error(json.error.data?.message || json.error.message);
            return json.result.length ? json.result[0].id : null;
        }"""
    )
    if not so_id:
        raise RuntimeError("Seeded SO-BENCH-STRUCT sale.order not found")
    navigate(page, f"/odoo/sales/{so_id}")
    _wait_for_ready(page)
    page.wait_for_selector(".o_form_view, .o_form_sheet", timeout=15000)
    page.wait_for_timeout(500)


def _click_footer_control(page, label):
    """Click one of the Order Lines footer controls ("Add a section",
    "Add a note", "Add a product") — each renders as an <a> inside
    td.o_field_x2many_list_row_add.

    First, make sure any currently-edited row has left edit mode by
    pressing Escape / clicking outside; otherwise the footer <a>'s
    pointer events get swallowed by the form's blur handler.
    """
    # Commit any pending edit by clicking on an inert area of the sheet
    try:
        page.locator(".o_form_sheet_bg, .o_form_sheet").first.click(
            position={"x": 5, "y": 5}
        )
    except Exception:
        pass
    page.wait_for_timeout(200)

    footer = page.locator(
        ".o_form_view .o_list_renderer td.o_field_x2many_list_row_add"
    ).first
    footer.wait_for(state="visible", timeout=10000)
    # Use get_by_role with exact name to avoid substring hits in the
    # chatter or elsewhere on the page.
    link = footer.get_by_role("button", name=label, exact=True)
    if link.count() == 0:
        # Fallback: role=link (actual <a> with role="button" should match
        # get_by_role("button"), but try link too).
        link = footer.get_by_role("link", name=label, exact=True)
    if link.count() == 0:
        # Last resort: find by inner text exactly among <a> children
        link = footer.locator("a").filter(has_text=label)
    link.first.wait_for(state="visible", timeout=5000)
    link.first.click()
    page.wait_for_timeout(700)
    _wait_no_loading(page)


def _fill_section_or_note_name(page, text):
    """In a freshly opened section/note row, the renderer auto-focuses
    the `name` cell (SectionAndNoteListRenderer.focusToName). The
    `name` cell renders as either a CharField (input, line_section) or
    a TextField (textarea, line_note) inside the row.

    Try multiple locator flavours: td[name='name'], the o_selected_row
    scoped field widget, or simply the focused element.
    """
    # Strategy 1: the selected row's td[name='name']
    row = page.locator(
        ".o_form_view .o_list_renderer .o_data_row.o_selected_row"
    ).first
    row.wait_for(state="visible", timeout=8000)

    # Try to find an editable input/textarea in that row.
    editor = row.locator("td[name='name'] input, td[name='name'] textarea")
    if editor.count() == 0:
        # Fallback: any input/textarea in the row (section-only rows
        # usually have a single wide editor)
        editor = row.locator("input, textarea")
    if editor.count() == 0:
        # Last resort: type into whatever is focused (the renderer
        # focuses the name field automatically on new section/note rows)
        page.keyboard.type(text, delay=15)
        page.keyboard.press("Tab")
        page.wait_for_timeout(500)
        _wait_no_loading(page)
        return

    ed = editor.first
    ed.wait_for(state="visible", timeout=5000)
    ed.click()
    try:
        ed.fill("")
    except Exception:
        # Some editors (contenteditable) don't support fill; clear via keyboard.
        ed.press("Control+a")
        ed.press("Delete")
    ed.type(text, delay=15)
    page.keyboard.press("Tab")
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def oracle(page):
    login(page)
    navigate(page, "/odoo/sales")
    _wait_no_loading(page)
    _open_quotation(page)
    page.wait_for_timeout(500)

    # The Order Lines tab is usually the default-open tab on the SO form.
    # Defensively click it so we are certainly there.
    ol_tab = page.locator(
        ".o_notebook .nav-link:has-text('Order Lines')"
    )
    if ol_tab.count() > 0 and ol_tab.first.is_visible():
        try:
            ol_tab.first.click()
            page.wait_for_timeout(400)
        except Exception:
            pass
    _wait_no_loading(page)

    # Scroll the notebook / list into view to make sure the footer
    # controls are in the viewport.
    try:
        page.locator(
            ".o_form_view .o_list_renderer"
        ).first.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
    except Exception:
        pass

    # --- Add a section ---
    _click_footer_control(page, "Add a section")
    _fill_section_or_note_name(page, SECTION_TEXT)

    # --- Add a note ---
    _click_footer_control(page, "Add a note")
    _fill_section_or_note_name(page, NOTE_TEXT)

    # --- Save (do not confirm) ---
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    save_form(page)
    page.wait_for_timeout(1000)
    _wait_no_loading(page)


run_oracle(oracle)
