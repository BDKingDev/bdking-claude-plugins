#!/usr/bin/env python
"""SessionStart hook: make the parazettel vault auto-consulted, not opt-in.

Injects a short context block telling the model to orient against the vault
(pzk_briefing) and to check for prior knowledge before substantive work
(pzk_find_similar_to_text with a full-claim query). If the parazettel daemon
is reachable, says so; if not, stays quiet about it (the MCP facade
auto-starts the daemon on first tool call anyway).

Always exits 0 — a recall nudge must never break session startup.
"""

import json
import sys
import urllib.request

DAEMON_HEALTH_URL = "http://127.0.0.1:8766/health"

CONTEXT = """<parazettel-memory>
This user has a persistent Zettelkasten vault (parazettel MCP, pzk_* tools) \
that serves as long-term memory across sessions.

- Orient first: call pzk_briefing once near the start of substantive work \
(active projects, due tasks, reminders, recently touched notes).
- Before researching, designing, or deciding something non-trivial, check for \
prior knowledge: pzk_find_similar_to_text with the task phrased as a complete \
sentence (full-claim queries vastly outperform keywords). The vault likely \
already has relevant notes; a low top score reliably means it does not.
- At the end of a session with durable insights, offer to capture them via \
/parazettel-helper:pzk-chat-session.{daemon_note}
</parazettel-memory>"""


def daemon_note() -> str:
    try:
        with urllib.request.urlopen(DAEMON_HEALTH_URL, timeout=1.5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if payload.get("ok"):
            return "\n- The parazettel daemon is up; tool calls will be fast."
    except Exception:
        pass
    return ""


def main() -> int:
    try:
        print(CONTEXT.format(daemon_note=daemon_note()))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
