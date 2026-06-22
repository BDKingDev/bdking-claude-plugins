#!/usr/bin/env python
"""SessionStart hook: inject a live parazettel vault briefing.

Unlike a nudge that tells the model to *call* pzk_briefing, this fetches the
briefing itself (over the daemon's localhost RPC) and injects it as context, so
the vault is consulted automatically. Stdlib-only (urllib + json) so it stays
fast and needs no parazettel/kuzu import. Always exits 0 — a briefing must never
break session startup; if the daemon is down it injects a short nudge instead.
"""

import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8766"
TIMEOUT = 4.0


def rpc(service, method, args=None, kwargs=None):
    """Call a daemon service method; return the de-tagged result or None."""
    body = json.dumps({"args": args or [], "kwargs": kwargs or {}}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/rpc/{service}/{method}",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("ok") is False:
        return None
    return _simplify(payload.get("result"))


def _simplify(v):
    """Strip the daemon codec's __pz_type__ tags into plain dicts/lists/values."""
    if isinstance(v, list):
        return [_simplify(x) for x in v]
    if isinstance(v, dict):
        tag = v.get("__pz_type__")
        if tag in ("model", "search_result"):
            return _simplify(v["data"])
        if tag == "tuple":
            return [_simplify(x) for x in v["items"]]
        if tag == "enum":
            return v["value"]
        if tag in ("path", "datetime", "date"):
            return v["value"]
        return {k: _simplify(x) for k, x in v.items()}
    return v


# NoteType.PROJECT encoded the way the daemon codec expects an enum argument.
_PROJECT_ENUM = {"__pz_type__": "enum", "enum": "NoteType", "value": "project"}


def build_briefing():
    """Return the formatted briefing, or None if the daemon is unreachable."""
    # Health gate first: if the daemon isn't up, bail fast (the MCP facade will
    # start it on the first real tool call anyway).
    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=1.5) as r:
            if not json.loads(r.read().decode("utf-8")).get("ok"):
                return None
    except Exception:
        return None

    lines = []

    projects = rpc("zettel_service", "search_notes", kwargs={"note_type": _PROJECT_ENUM})
    if projects:
        active = [
            p for p in projects
            if (p.get("status") not in ("done", "cancelled"))
        ]
        if active:
            active.sort(key=lambda p: (p.get("due_date") or "9999-12-31"))
            lines.append(f"Active projects ({len(active)}):")
            for p in active[:8]:
                due = f" — due {p['due_date']}" if p.get("due_date") else ""
                lines.append(f"  - {p.get('title')}{due} (ID: {p.get('id')})")

    tasks = rpc("zettel_service", "get_todays_tasks", args=[True])
    if tasks:
        lines.append(f"Tasks due/overdue ({len(tasks)}):")
        for t in tasks[:10]:
            pr = f" [P{t['priority']}]" if t.get("priority") else ""
            due = f" — due {t['due_date']}" if t.get("due_date") else ""
            lines.append(f"  -{pr} {t.get('title')}{due} (ID: {t.get('id')})")

    reminders = rpc("zettel_service", "get_reminders", args=[8])
    if reminders:
        lines.append(f"Reminders due ({len(reminders)}):")
        for n in reminders:
            lines.append(f"  - {n.get('title')} (remind {n.get('remind_at')}, ID: {n.get('id')})")

    central = rpc("search_service", "find_central_notes", args=[6])
    if central:
        # find_central_notes may return notes or (note, score) pairs.
        lines.append("Most-connected notes (orientation):")
        for item in central[:6]:
            note = item[0] if isinstance(item, list) else item
            if isinstance(note, dict):
                lines.append(f"  - {note.get('title')} (ID: {note.get('id')})")

    if not lines:
        body = "The parazettel vault is up but returned no active items right now."
    else:
        body = "\n".join(lines)

    return (
        "<parazettel-briefing>\n"
        "Live snapshot of the user's persistent Zettelkasten vault (parazettel "
        "MCP, pzk_* tools) — their long-term memory across sessions. Consult it "
        "before researching/designing/deciding; phrase semantic checks "
        "(pzk_find_similar_to_text) as a full-claim sentence. Offer to capture "
        "durable insights at session end via /parazettel-helper:pzk-chat-session.\n\n"
        f"{body}\n"
        "</parazettel-briefing>"
    )


def main():
    try:
        context = build_briefing()
    except Exception:
        context = None
    if not context:
        # Daemon down or error: a minimal nudge, never a hard failure.
        context = (
            "<parazettel-memory>The user has a persistent parazettel Zettelkasten "
            "vault (pzk_* tools) as long-term memory. Call pzk_briefing near the "
            "start of substantive work and pzk_find_similar_to_text (full-claim "
            "query) before deciding things; the daemon auto-starts on first use."
            "</parazettel-memory>"
        )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
