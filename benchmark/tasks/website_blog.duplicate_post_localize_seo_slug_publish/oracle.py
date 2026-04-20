"""Oracle for website_blog.duplicate_post_localize_seo_slug_publish."""
from benchmark.oracle_helpers import (
    click_tab,
    ensure_list_view,
    fill_field,
    fill_text_field,
    login,
    navigate,
    run_oracle,
    save_form,
    search_for,
)

def oracle(page):
    login(page)
    navigate(page, "/odoo/blog-post-pages?debug=1")
    ensure_list_view(page)
    search_for(page, "Warehouse Safety Primer")
    page.locator(
        ".o_list_view .o_data_row:has-text('Warehouse Safety Primer') .o_list_record_selector input"
    ).first.check()
    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    print("MENU_ITEMS", page.locator(".dropdown-menu:visible .dropdown-item, .dropdown-menu:visible .o_menu_item").all_inner_texts())
    page.locator(".dropdown-menu:visible .dropdown-item, .dropdown-menu:visible .o_menu_item").filter(
        has_text="Duplicate"
    ).first.click()
    page.wait_for_timeout(1000)
    row = page.locator(".o_list_view .o_data_row:has-text('Warehouse Safety Primer (copy)')").first
    website_url = row.locator("td[name='website_url']").inner_text().strip()
    copy_id = website_url.rsplit("-", 1)[-1]
    navigate(page, f"/odoo/action-website_blog.action_blog_post/{copy_id}?debug=1")
    fill_field(page, "name", "Warehouse Safety Primer EU")
    click_tab(page, "SEO")
    fill_field(page, "website_meta_title", "Warehouse Safety Primer for EU Teams")
    fill_text_field(
        page,
        "website_meta_description",
        "Safety baseline for EU warehouse operations and dock checks.",
    )
    save_form(page)
    navigate(page, "/odoo/blog-post-pages?debug=1")
    ensure_list_view(page)
    search_for(page, "Warehouse Safety Primer EU")
    page.locator(
        ".o_list_view .o_data_row:has-text('Warehouse Safety Primer EU') .o_list_record_selector input"
    ).first.check()
    page.locator(".o_cp_action_menus .dropdown-toggle").first.click()
    page.wait_for_timeout(500)
    page.locator(".dropdown-menu:visible .dropdown-item, .dropdown-menu:visible .o_menu_item").filter(
        has_text="Publish"
    ).first.click()
    page.wait_for_timeout(500)
    if page.locator(".modal:visible").count() > 0:
        page.locator(".modal:visible button.btn-primary:visible, .modal:visible button:has-text('Confirm')").first.click()
        page.wait_for_timeout(500)

run_oracle(oracle)
