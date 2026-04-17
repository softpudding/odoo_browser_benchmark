"""Oracle for website.create_blog_post_publish."""

from benchmark.oracle_helpers import login, navigate, run_oracle, set_many2one, _wait_no_loading


BODY = (
    "Warehouse leaders are prioritizing slotting accuracy, cycle-count automation, "
    "and exception-driven replenishment before larger robotics projects."
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages?debug=1")
    _wait_no_loading(page)

    page.get_by_role("button", name="New").click()
    page.wait_for_timeout(500)
    _wait_no_loading(page)

    set_many2one(page, "blog_id", "Operations Insights")
    title = page.locator("[name='name'] input, input[name='name']").first
    title.fill("Warehouse Automation Trends 2026")
    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)

    page.get_by_role("button", name="Edit").click()
    page.wait_for_timeout(2500)
    _wait_no_loading(page)

    content_frame = page.frames[1]
    content_frame.locator(".o_wblog_post_subtitle").first.fill(
        "What operations teams should automate first"
    )
    content_frame.locator(".o_wblog_post_content_field").first.fill(BODY)

    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(5000)
    _wait_no_loading(page)

    page.locator(".o_website_publish_container a").first.click()
    page.wait_for_timeout(1500)
    _wait_no_loading(page)


run_oracle(oracle)
