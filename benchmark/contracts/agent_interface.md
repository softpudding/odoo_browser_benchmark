# Agent Interface Contract

Version: 0.1

## Browser-Only Track (Default)

The primary benchmark track uses the `browser_only` agent interface.

### Allowed Observations

The agent may observe:

- The task instruction text
- Current browser URL
- Browser-rendered DOM / accessibility tree / HTML (obtained through the browser automation framework)
- Screenshots of the current browser viewport
- Browser-visible text, attributes, and styles
- Agent-maintained memory from within the current episode

### Allowed Actions

The agent may perform:

- **click** — click on any visible element
- **type** — enter text into form fields
- **keypress** — send keyboard events (Enter, Tab, Escape, shortcuts, etc.)
- **scroll** — scroll the page or specific elements
- **hover** — hover over elements to trigger tooltips/menus
- **drag and drop** — drag elements to new positions
- **tab management** — open, close, and switch between browser tabs
- **navigation** — `goto(url)`, back, forward, refresh
- **file upload** — attach files when the task requires it

### Forbidden Actions

The agent must NOT:

1. **Make direct HTTP calls** to Odoo endpoints outside the browser page context
2. **Construct and submit JSON-RPC** requests programmatically
3. **Access the database** directly (SQL, ORM, or any non-browser channel)
4. **Shell into the server** to inspect state, logs, or configuration
5. **Read benchmark oracle files** (`task.yaml`, `trace_spec.yaml`, `state_spec.yaml`, etc.) during task execution

### Enforcement

The benchmark runner enforces this contract via the `RunnerGuard`:

- Direct RPC calls from agent code are intercepted and blocked
- Direct database access attempts are logged and blocked
- Oracle file reads are prevented
- All violations are recorded and reported in the run artifacts

### Contract Violations

Any violation of the forbidden actions above results in:

- The violation being logged in `violations.json`
- The run is still scored, but violations are reported alongside metrics
- Agents with contract violations should be flagged in leaderboard results

## Hybrid Track (Future)

A separate track for agents that use both browser and API access may be
defined in a future version. Hybrid agents must be evaluated separately
from browser-only agents and must not appear on the browser-only leaderboard.
