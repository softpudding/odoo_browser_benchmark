"""Oracle for website_sale.edit_product_image_gallery.

Uses a JSON-RPC bypass to create a new product.image record attached to
the seeded product.template. The browser-use agent must still solve via
the UI (Sales tab > eCommerce Media > Add Media), but the oracle takes
the deterministic path.
"""

from benchmark.oracle_helpers import login, navigate, run_oracle


# A 4x4 RGB blue PNG produced by PIL (77 bytes). Small enough to be a
# valid image the Odoo image pipeline (PIL.Image.open) accepts.
PLACEHOLDER_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAFElEQVR4nGM0SjnB"
    "AANMDEgANwcARMoBZnEvszMAAAAASUVORK5CYII="
)


def oracle(page):
    login(page)
    navigate(page, "/odoo/inventory/products")

    response = page.evaluate(
        """async (imgB64) => {
            const callKw = async (payload) => {
                const res = await fetch('/web/dataset/call_kw', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'same-origin',
                    body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: payload }),
                });
                const json = await res.json();
                if (json.error) {
                    throw new Error(json.error.data?.message || json.error.message);
                }
                return json.result;
            };

            const hits = await callKw({
                model: 'product.template',
                method: 'search_read',
                args: [[['name', '=', 'Bench Gallery Mug']], ['id']],
                kwargs: { limit: 1 },
            });
            if (!hits.length) {
                throw new Error('Bench Gallery Mug product not found');
            }
            const tmplId = hits[0].id;

            const newId = await callKw({
                model: 'product.image',
                method: 'create',
                args: [[{
                    name: 'Bench Side View',
                    product_tmpl_id: tmplId,
                    image_1920: imgB64,
                }]],
                kwargs: {},
            });
            return 'ok:' + newId;
        }""",
        PLACEHOLDER_PNG_B64,
    )
    if not response or not str(response).startswith("ok"):
        raise RuntimeError(response)


run_oracle(oracle)
