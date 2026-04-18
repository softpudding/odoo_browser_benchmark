"""Oracle for event.add_track_with_speaker_publish."""

from benchmark.oracle_helpers import (
    click_list_row,
    click_stat_button,
    click_tab,
    clear_search_filters,
    fill_field,
    login,
    navigate,
    run_oracle,
    save_form,
    _wait_for_ready,
    _wait_no_loading,
)


EVENT_NAME = "Bench Spring Summit"
TRACK_NAME = "Keynote: Future of Bench"
SPEAKER_NAME = "Dr. Smith"
SPEAKER_EMAIL = "dr.smith@example.com"


def oracle(page):
    login(page)
    navigate(page, "/odoo/events")
    _wait_no_loading(page)

    # Clear any default filter (e.g. "Upcoming") so the seeded event is visible.
    clear_search_filters(page)
    click_list_row(page, EVENT_NAME)
    _wait_for_ready(page)

    # Open Tracks smart button.
    click_stat_button(page, "Tracks")
    _wait_for_ready(page)

    # Create a new track.
    page.locator(
        "button.o_list_button_add:visible, "
        ".o-kanban-button-new:visible, "
        ".o_control_panel button:has-text('New'):visible"
    ).first.click()
    _wait_no_loading(page)

    # Some kanban views open a quick-create inline dialog. If so, we need the
    # full form — click the 'Edit' / expand link. Otherwise we're already on
    # the full form.
    # Check whether we're on the full form (has the Speaker notebook tab).
    page.wait_for_timeout(600)
    if page.locator(".o_notebook .nav-link:has-text('Speaker')").count() == 0:
        # We are likely in a quick-create modal. Fill name + date there, save,
        # then re-open the record to set speaker fields.
        qc_name = page.locator(
            ".modal .o_field_widget[name='name'] input:visible, "
            ".o_kanban_quick_create .o_field_widget[name='name'] input:visible"
        ).first
        qc_name.click()
        qc_name.fill(TRACK_NAME)
        page.wait_for_timeout(300)
        # Try to save the quick create first (Add or Save).
        save_btn = page.locator(
            ".o_kanban_quick_create .o_kanban_add:visible, "
            ".o_kanban_quick_create button:has-text('Add'):visible, "
            ".modal .modal-footer button:has-text('Save'):visible"
        )
        if save_btn.count() > 0:
            save_btn.first.click()
            _wait_no_loading(page)
        # Re-open the newly-created track from the view.
        page.wait_for_timeout(500)
        card = page.locator(f".o_kanban_record:has-text('{TRACK_NAME}')").first
        if card.count() > 0:
            card.click()
            _wait_for_ready(page)
        else:
            row = page.locator(f".o_list_view .o_data_row:has-text('{TRACK_NAME}')").first
            if row.count() > 0:
                row.click()
                _wait_for_ready(page)

    # On the full form: fill name if not already filled.
    name_widget = page.locator(
        ".o_field_widget[name='name'] textarea:visible, "
        ".o_field_widget[name='name'] input:visible"
    ).first
    current = ""
    try:
        current = (name_widget.input_value() or "").strip()
    except Exception:
        current = ""
    if current != TRACK_NAME:
        name_widget.click()
        name_widget.fill(TRACK_NAME)
        page.wait_for_timeout(300)

    # Fill the date field. "date" is a datetime widget on the main form.
    date_widget = page.locator(".o_field_widget[name='date']").first
    date_input = date_widget.locator("input:visible")
    if date_input.count() == 0:
        # Click the field to reveal the input.
        date_widget.click()
        page.wait_for_timeout(400)
        date_input = date_widget.locator("input:visible")
    date_input.first.click()
    date_input.first.fill("")
    date_input.first.type("05/15/2026 10:00:00")
    date_input.first.press("Escape")  # close date picker popover
    page.wait_for_timeout(300)
    _wait_no_loading(page)

    # Speaker tab.
    click_tab(page, "Speaker")
    page.wait_for_timeout(300)

    fill_field(page, "partner_name", SPEAKER_NAME)
    fill_field(page, "partner_email", SPEAKER_EMAIL)

    save_form(page)
    _wait_no_loading(page)

    # Publish by clicking the 'Published' stage on the status bar.
    published_btn = page.locator(
        ".o_statusbar_status button:has-text('Published'):visible, "
        ".o_statusbar_status .o_arrow_button:has-text('Published'):visible"
    ).first
    published_btn.click()
    _wait_no_loading(page)
    # Give the inverse _synchronize_with_stage a moment to flip is_published.
    page.wait_for_timeout(800)
    save_form(page)
    _wait_no_loading(page)


run_oracle(oracle)
