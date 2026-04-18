"""Postcondition checks for website.set_page_seo_fields."""


PAGE_URL = "/bench-product"
PAGE_NAME = "Bench Product Landing"
EXPECTED_TITLE = "Bench Product - Premium Quality | Bench Co"
EXPECTED_DESCRIPTION = (
    "Discover our flagship Bench Product with premium materials and lifetime warranty. "
    "Order today for free shipping."
)
EXPECTED_KEYWORDS = {"bench product", "premium bench", "quality furniture"}


def _normalize_keywords(raw):
    if not raw:
        return set()
    return {kw.strip().lower() for kw in raw.split(",") if kw.strip()}


def check(env):
    failures = []

    pages = env["website.page"].search([("url", "=", PAGE_URL)])
    if len(pages) != 1:
        return [f"Expected exactly 1 website.page at {PAGE_URL!r}, found {len(pages)}"]

    page = pages[0]

    if page.name != PAGE_NAME:
        failures.append(f"Page name is {page.name!r}, expected {PAGE_NAME!r}")

    if not page.is_published:
        failures.append("Page was unpublished; it must stay published")

    if (page.website_meta_title or "").strip() != EXPECTED_TITLE:
        failures.append(
            f"website_meta_title is {page.website_meta_title!r}, expected {EXPECTED_TITLE!r}"
        )

    if (page.website_meta_description or "").strip() != EXPECTED_DESCRIPTION:
        failures.append(
            f"website_meta_description is {page.website_meta_description!r}, "
            f"expected {EXPECTED_DESCRIPTION!r}"
        )

    actual_keywords = _normalize_keywords(page.website_meta_keywords or "")
    if actual_keywords != EXPECTED_KEYWORDS:
        failures.append(
            f"website_meta_keywords is {page.website_meta_keywords!r}; "
            f"expected keywords {sorted(EXPECTED_KEYWORDS)!r}"
        )

    return failures
