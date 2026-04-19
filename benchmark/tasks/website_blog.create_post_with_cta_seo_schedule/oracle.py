"""Oracle for website_blog.create_post_with_cta_seo_schedule.

Pure Playwright UI flow (no JSON-RPC shortcuts):

  1. Open /odoo/blog-post-pages in debug mode so the SEO notebook
     tab on the backend blog.post form is visible.
  2. Click "New" — opens the website_new_content_form modal.
  3. Pick the existing blog "Bench Tech Blog" from the Blog dropdown
     and set the post Title.
  4. Save the modal — Odoo redirects to the freshly created post's
     /blog/<blog-slug>/<post-slug> URL. The last "-<digits>" segment
     of that path is the blog.post id.
  5. Open the website editor on that post
     (/odoo/action-website.website_preview?path=<post_url>&enable_editor=1),
     inject a paragraph containing the call-to-action, and save the
     editor.
  6. Navigate to /odoo/blog-post-pages/<id>?debug=1 to open the new
     post directly in the backend form view (bypassing the list's
     "open website" click behaviour) and:
        - set post_date (Publishing date, which is the inverse of
          published_date) to 05/20/2026 10:00:00,
        - open the SEO tab (only visible in debug mode) and fill
          website_meta_title / website_meta_description,
        - save the form.
  7. Never toggle publish — the post stays scheduled.
"""

import re
from urllib.parse import quote, unquote

from benchmark.oracle_helpers import (
    _wait_for_ready,
    _wait_no_loading,
    fill_field,
    fill_text_field,
    full_url,
    login,
    navigate,
    run_oracle,
)


BLOG_NAME = "Bench Tech Blog"
POST_NAME = "Bench New Feature Launch"
META_TITLE = "Bench New Feature"
META_DESCRIPTION = "Announcing our new bench feature"
CTA_TEXT = "Click here for details"
# post_date widget uses MM/DD/YYYY HH:MM:SS in the admin locale.
PUBLISHING_DATE = "05/20/2026 10:00:00"


# ---------------------------------------------------------------------------
# Modal / many2one helpers
# ---------------------------------------------------------------------------

def _modal(page):
    return page.locator(".modal:visible").last


def _set_modal_many2one(page, field_name, search_text):
    """Pick an existing record from a many2one dropdown inside a modal."""
    modal = _modal(page)
    inp = modal.locator(f".o_field_widget[name='{field_name}'] input").first
    inp.click()
    inp.fill("")
    inp.fill(search_text)
    page.wait_for_timeout(900)
    items = page.locator(
        ".o-autocomplete--dropdown-menu:visible .o-autocomplete--dropdown-item, "
        ".dropdown-menu:visible .dropdown-item, "
        ".ui-autocomplete:visible .ui-menu-item"
    )
    picked = False
    for i in range(items.count()):
        txt = items.nth(i).inner_text().strip()
        if "Create" in txt or "create" in txt:
            continue
        if search_text in txt:
            items.nth(i).click()
            picked = True
            break
    if not picked and items.count() > 0:
        items.first.click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)


def _fill_modal_field(page, field_name, value):
    modal = _modal(page)
    inp = modal.locator(f".o_field_widget[name='{field_name}'] input").first
    inp.click()
    inp.fill("")
    inp.fill(value)
    inp.press("Tab")
    page.wait_for_timeout(400)


# ---------------------------------------------------------------------------
# Create flow (modal)
# ---------------------------------------------------------------------------

def _create_post_via_new_button(page):
    """Click 'New' and fill the website_new_content_form modal."""
    new_btn = page.locator(
        "button.o_list_button_add:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first
    new_btn.click()
    page.wait_for_timeout(1500)
    page.wait_for_selector(".modal:visible", timeout=15000)

    _set_modal_many2one(page, "blog_id", BLOG_NAME)
    _fill_modal_field(page, "name", POST_NAME)

    # Save the modal — Odoo's website_new_content_form controller
    # redirects to the new post's website_url after saving.
    modal = _modal(page)
    save_btn = modal.locator(
        ".modal-footer button.o_form_button_save, "
        ".modal-footer button:has-text('Save'), "
        ".modal-footer button.btn-primary"
    ).first
    save_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)


def _extract_blog_post_path_and_id(page):
    """Return (post_path, post_id) from the current page URL or iframe."""
    url = page.url
    # Try ?path=/blog/<blog>/<post>
    m = re.search(r"[?&]path=([^&#]+)", url)
    if m:
        path = unquote(m.group(1))
    else:
        m = re.search(r"(/blog/[^?#]+)", url)
        path = m.group(1) if m else None

    if not path:
        # Fallback: dig into the iframe src
        try:
            src = page.locator("iframe").first.get_attribute("src")
            if src:
                m = re.search(r"(/blog/[^?#]+)", src)
                if m:
                    path = m.group(1)
        except Exception:
            pass

    if not path:
        raise RuntimeError(f"Could not find /blog/... path on {url!r}")

    # The path ends with the post slug (…/<post-slug>-<id>). Grab
    # the LAST "-<digits>" segment; /blog/<blog>-<blog_id>/<post>-<id>
    # also contains the blog id which we must not pick up.
    id_matches = re.findall(r"-(\d+)(?=/|$)", path)
    if not id_matches:
        raise RuntimeError(f"Could not extract post id from path {path!r}")
    return path, int(id_matches[-1])


# ---------------------------------------------------------------------------
# Website editor flow
# ---------------------------------------------------------------------------

def _open_editor_for_post(page, post_path):
    editor_url = (
        "/odoo/action-website.website_preview"
        f"?path={quote(post_path, safe='')}&enable_editor=1"
    )
    page.goto(full_url(editor_url))
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000)
    page.wait_for_selector("[data-action='save']", timeout=45000)
    page.wait_for_timeout(3000)


def _inject_cta_in_editor(page):
    """Append a paragraph with the CTA string inside the blog content."""
    iframe = page.frame_locator(
        "iframe.o_iframe, iframe[name='o_iframe'], iframe:not(.o_ignore_in_tour)"
    )
    body = iframe.locator(
        ".o_wblog_post_content_field, "
        "[data-oe-field='content'], "
        ".o_wblog_post_main"
    ).first
    body.click()
    page.wait_for_timeout(600)

    # Directly append a <p> with the CTA text; fire an input event so
    # the editor's mutation observer registers the change as dirty.
    iframe.locator("body").evaluate(
        """(body, cta) => {
            const root =
                body.querySelector('.o_wblog_post_content_field') ||
                body.querySelector("[data-oe-field='content']");
            if (!root) throw new Error('No content field found in editor');
            const p = document.createElement('p');
            p.textContent = cta;
            root.appendChild(p);
            root.dispatchEvent(new Event('input', { bubbles: true }));
        }""",
        CTA_TEXT,
    )
    page.wait_for_timeout(1000)


def _save_editor(page):
    page.locator("[data-action='save']").first.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(6000)
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Backend form flow
# ---------------------------------------------------------------------------

def _set_post_date(page, datetime_str):
    """Set the post_date datetime on the open blog.post form.

    In Odoo 19 a Datetime field that already has a value renders as
    a <button>; focusing it triggers the Owl component to swap it
    for an editable <input>. Once the input is present we clear and
    retype the desired value via keyboard — the Owl component listens
    to focus/blur/input to persist the value on the record.
    """
    widget = page.locator(".o_field_widget[name='post_date']").first
    widget.wait_for(state="attached", timeout=15000)
    widget.scroll_into_view_if_needed()
    page.wait_for_timeout(300)

    # Focus the widget's button (if present) so Owl swaps it for an
    # <input>. A plain focus event is enough — we don't click because
    # clicking also opens the datepicker popover which sometimes
    # steals focus.
    if widget.locator("input").count() == 0:
        target = widget.locator("button, input").first
        target.dispatch_event("focus")
        page.wait_for_timeout(400)

    # Poll until an input is attached (the Owl re-render is async).
    for _ in range(40):
        if widget.locator("input").count() > 0:
            break
        page.wait_for_timeout(100)
    else:
        raise RuntimeError("post_date input never appeared")

    # Drive the input via JS on the widget (not the input locator):
    # find the input fresh each time, focus, set value, dispatch
    # input + change. Then press Enter via keyboard to trigger
    # saveAndClose which parses the input and persists the value.
    # Using widget.evaluate avoids Playwright's locator visibility
    # waits on the input element (it may be briefly re-rendered).
    widget.evaluate(
        """(w, val) => {
            const inp = w.querySelector('input');
            if (!inp) throw new Error('post_date input not found');
            inp.focus();
            const setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            setter.call(inp, val);
            inp.dispatchEvent(new Event('input', { bubbles: true }));
            inp.dispatchEvent(new Event('change', { bubbles: true }));
        }""",
        datetime_str,
    )
    page.wait_for_timeout(300)
    # Press Enter on the focused input — the datetime service's
    # onInputKeydown handler calls saveAndClose() which closes the
    # picker popover and persists the input's value on the record.
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    # Close any datepicker popover that may still be open.
    if page.locator(".o_datetime_picker:visible, .o_date_picker:visible").count() > 0:
        page.keyboard.press("Escape")
        page.wait_for_timeout(200)
    _wait_no_loading(page)


def _set_seo_meta(page):
    """Switch to the SEO notebook tab and fill website_meta_* fields."""
    seo_tab = page.locator(".o_notebook .nav-link:has-text('SEO')").first
    seo_tab.wait_for(state="visible", timeout=10000)
    seo_tab.click()
    page.wait_for_timeout(500)
    fill_field(page, "website_meta_title", META_TITLE)
    fill_text_field(page, "website_meta_description", META_DESCRIPTION)


def _save_form_view(page):
    save_btn = page.locator(
        ".o_form_button_save:visible, "
        "button.o_form_button_save:visible, "
        ".o_control_panel button:has-text('Save'):visible"
    ).first
    save_btn.click()
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def oracle(page):
    login(page)

    # --- 1. Open the Blog Posts list in debug mode.
    navigate(page, "/odoo/blog-post-pages?debug=1")
    page.wait_for_timeout(1000)

    # --- 2. Click "New" and fill the small modal (Blog + Title).
    _create_post_via_new_button(page)

    # --- 3. Figure out which post we just created.
    post_path, post_id = _extract_blog_post_path_and_id(page)

    # --- 4. Open the website editor and add the CTA, then save.
    _open_editor_for_post(page, post_path)
    _inject_cta_in_editor(page)
    _save_editor(page)

    # --- 5. Open the backend form view for the post directly.
    #        Navigating to /odoo/action-<xmlid>/<resId> forces the
    #        form view (list / kanban cannot render a single resId),
    #        bypassing the website_pages_list "open_website_url"
    #        click behaviour.
    target = f"/odoo/action-website_blog.action_blog_post/{post_id}"
    navigate(page, target)
    page.wait_for_timeout(2000)
    page.wait_for_selector(
        ".o_form_view .o_field_widget[name='name']", timeout=30000
    )
    page.wait_for_timeout(800)

    # --- 6. Fill post_date + SEO meta.
    _set_post_date(page, PUBLISHING_DATE)
    _set_seo_meta(page)
    _save_form_view(page)


run_oracle(oracle)
