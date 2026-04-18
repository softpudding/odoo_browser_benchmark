# event_product.create_event_product_link_to_ticket — quirks

## product.template duplicate-name nondeterminism

The base snapshot ships with two `product.template` records both named
`Gift Card` but with different `list_price` (0.0 and 50.0). When
`state_spec.yaml` uses `match_key: [name]` for `product.template`, the
diff engine resolves the duplicates with non-deterministic
`#dup0`/`#dup1` ordering between before/after captures. This produces
spurious `set` edits on `list_price` (50.0 ↔ 0.0) every run, even when
the agent never touches Gift Card.

Fix: extend `match_key` to include differentiating fields, e.g.

```yaml
product.template:
  match_key:
    - name
    - service_tracking
    - list_price
```

The corresponding `entity_key` in `expected_state.json` becomes
`["Conference Pass Std", "event", 100.0]` instead of just
`["Conference Pass Std"]`. F1 jumped from 0.9 (with two phantom Gift
Card edits) to 1.0 after the fix.

Generalisation: any task that tracks `product.template` should expect
the same Gift Card collision. Either widen the match_key, scope the
diff to event-related models only, or rely on `check.py` for the
substantive product assertions.

## Service Tracking visibility on product form

`service_tracking` is `invisible="1 or type != 'service'"` in the base
product view. The `event_sale` module (auto-installed because both
`event` and `sale` are present in the base snapshot) removes the
`invisible` attribute via a view extension, exposing the selection
including the `event` ('Event Registration') option contributed by
`event_product`. No explicit module install needed in the seed.
