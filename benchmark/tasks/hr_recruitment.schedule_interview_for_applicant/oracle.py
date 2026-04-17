"""Oracle for hr_recruitment.schedule_interview_for_applicant."""

from benchmark.oracle_helpers import (
    click_kanban_card,
    login,
    navigate,
    run_oracle,
    schedule_activity,
    _wait_no_loading,
    _wait_for_ready,
)


def _click_exact_kanban_card(page, exact_text: str) -> None:
    cards = page.locator(".o_kanban_view .o_kanban_record")
    for idx in range(cards.count()):
        card = cards.nth(idx)
        lines = [
            " ".join(line.split())
            for line in card.inner_text().splitlines()
            if line.strip()
        ]
        if exact_text in lines or " ".join(lines) == exact_text:
            card.click()
            page.wait_for_load_state("load")
            _wait_for_ready(page)
            return
    raise RuntimeError(f"Could not find exact kanban card {exact_text!r}")


def oracle(page):
    login(page)
    navigate(page, "/odoo/recruitment")
    _wait_no_loading(page)

    click_kanban_card(page, "Operations Analyst")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    _click_exact_kanban_card(page, "Riley Mercer")
    _wait_for_ready(page)
    page.wait_for_timeout(500)

    schedule_activity(
        page,
        activity_type="Call",
        summary="Schedule first interview",
        due_date="06/17/2026",
    )
    page.wait_for_timeout(1200)
    _wait_no_loading(page)


run_oracle(oracle)
