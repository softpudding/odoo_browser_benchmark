## calendar.event.set_discuss_videocall_location is a frontend-only stub

In Odoo 19, `calendar.event.set_discuss_videocall_location()` on the server is
a no-op that just `return True` — the actual videocall URL generation happens
in JS (the method is intercepted by the frontend). The private method
`_set_discuss_videocall_location()` does the real work but isn't callable via
JSON-RPC.

**For JSON-RPC oracle scripts that need a Discuss videocall URL**, craft the
URL manually and write it to `videocall_location` along with an `access_token`:

```js
const token = crypto.randomUUID().replace(/-/g, '');
await callKw({
    model: 'calendar.event',
    method: 'create',
    args: [[{
        name: '...',
        // ... other fields ...
        videocall_location: `${window.location.origin}/calendar/join_videocall/${token}`,
        access_token: token,
    }]],
    kwargs: {},
});
```

Check the URL with `"/calendar/join_videocall/" in event.videocall_location`
(the `DISCUSS_ROUTE` constant on `calendar.event`).
