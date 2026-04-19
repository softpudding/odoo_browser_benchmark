"""Oracle for im_livechat.send_message_to_operator.

Deterministic Playwright solution:

 1. Log in as admin (separate context) and look up the Bench Help channel id
    via JSON-RPC. The prompt tells the agent to discover the id from the
    back-office.
 2. Open a **second, cookie-free** browser context (incognito-style) so the
    visitor on the livechat support page is genuinely anonymous — otherwise
    admin would be both operator AND visitor which short-circuits the public
    get_session flow.
 3. Navigate that visitor tab to `/im_livechat/support/<channel_id>`.
 4. Interact with the widget. Playwright's CSS engine automatically pierces
    OPEN shadow DOM, so `.o-livechat-LivechatButton` / `.o-mail-Composer-input`
    work directly even though they live inside `.o-livechat-root`'s shadow
    root.
 5. Type 'Hello, I need help' into `.o-mail-Composer-input` and press Enter.
 6. Wait for the sent message bubble, then give the server a moment to
    persist the new `discuss.channel` + first `mail.message`.
"""

import os
import sys

from playwright.sync_api import sync_playwright

from benchmark.oracle_helpers import full_url, login, navigate


def _lookup_channel_id(page):
    """Use JSON-RPC as the logged-in admin to fetch the Bench Help id."""
    res = page.evaluate(
        """async () => {
            const r = await fetch('/web/dataset/call_kw', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: {
                        model: 'im_livechat.channel',
                        method: 'search_read',
                        args: [[['name', '=', 'Bench Help']], ['id']],
                        kwargs: {},
                    },
                }),
            });
            const json = await r.json();
            if (json.error) {
                throw new Error(json.error.data?.message || json.error.message);
            }
            return json.result;
        }"""
    )
    if not res:
        raise RuntimeError("Bench Help channel not found via JSON-RPC")
    return res[0]["id"]


def oracle(page_admin):
    # Step 1 — discover the channel id as admin.
    login(page_admin)
    navigate(page_admin, "/odoo/livechat")
    channel_id = _lookup_channel_id(page_admin)

    # Step 2 — open a second, anonymous browser context for the visitor.
    browser = page_admin.context.browser
    visitor_ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    visitor_ctx.set_default_timeout(60_000)
    visitor = visitor_ctx.new_page()

    try:
        # Step 3 — visit the support page as anonymous visitor.
        visitor.goto(full_url(f"/im_livechat/support/{channel_id}"))
        visitor.wait_for_load_state("load")

        # The livechat loader is async: mount takes time for the boot
        # helpers + service workers + store init. The shadow-host element
        # itself is display:contents/hidden, so wait for attachment (not
        # visibility) and then for the button inside the shadow root.
        visitor.wait_for_selector(".o-livechat-root", timeout=30_000, state="attached")
        visitor.wait_for_timeout(2000)

        # Step 4 — click the floating livechat button.
        livechat_btn = visitor.locator(".o-livechat-LivechatButton")
        livechat_btn.wait_for(state="visible", timeout=30_000)
        livechat_btn.click()

        # Wait for the chat window + composer input to render.
        visitor.locator(".o-mail-ChatWindow").wait_for(state="visible", timeout=30_000)
        composer = visitor.locator(".o-mail-Composer-input")
        composer.wait_for(state="visible", timeout=20_000)
        composer.click()
        composer.fill("Hello, I need help")
        visitor.wait_for_timeout(400)
        composer.press("Enter")

        # Step 5 — wait for the sent message bubble.
        visitor.locator(
            ".o-mail-Message:has-text('Hello, I need help')"
        ).first.wait_for(state="visible", timeout=30_000)

        # Give the server a beat to persist the discuss.channel + message.
        visitor.wait_for_timeout(2000)

    finally:
        try:
            visitor_ctx.close()
        except Exception:
            pass


def main():
    headed = bool(os.environ.get("BENCHMARK_HEADED", "1"))
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        ctx.set_default_timeout(60_000)
        page = ctx.new_page()
        try:
            oracle(page)
            print("Oracle: PASS")
            sys.exit(0)
        except Exception as exc:
            print(f"Oracle: FAIL - {exc}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            ctx.close()
            browser.close()


if __name__ == "__main__":
    main()
