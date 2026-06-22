#!/usr/bin/env python
"""UserPromptSubmit hook: auto-recall relevant vault notes for the prompt.

Semantic-searches the parazettel vault with the user's message and, only when
there is a genuinely relevant hit, injects the matches as context — so prior
knowledge surfaces without anyone asking. Self-scoping (no hit -> no output) and
stdlib-only (urllib + json), so it adds almost nothing on prompts the vault has
nothing for. Always exits 0 — recall must never block a prompt.
"""

import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8766"
TIMEOUT = 6.0
THRESHOLD = 0.55          # min cosine similarity to bother injecting
LIMIT = 4                 # max notes to surface
MIN_PROMPT_CHARS = 24     # skip trivial prompts ("yes", "continue", "fix that")


def _simplify(v):
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


def recall(prompt):
    """Return formatted relevant notes, or None when nothing clears the bar."""
    # Health gate: if the daemon is down, stay silent (don't pay startup cost).
    try:
        with urllib.request.urlopen(f"{BASE}/health", timeout=1.0) as r:
            if not json.loads(r.read().decode("utf-8")).get("ok"):
                return None
    except Exception:
        return None

    body = json.dumps({
        "args": [prompt, THRESHOLD, LIMIT],
        "kwargs": {},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/rpc/zettel_service/find_similar_to_text",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("ok") is False:
        return None

    pairs = _simplify(payload.get("result")) or []  # list of [note_dict, score]
    rows = []
    for pair in pairs:
        if not isinstance(pair, list) or len(pair) != 2:
            continue
        note, score = pair
        if not isinstance(note, dict):
            continue
        rows.append(f"  - [{score:.2f}] {note.get('title')} (ID: {note.get('id')})")
    if not rows:
        return None

    return (
        "<parazettel-recall>\n"
        "Possibly-relevant notes already in the user's vault (semantic match to "
        "this message). Open the top one before creating overlapping content; a "
        "high score means same topic, not necessarily the same atomic claim.\n"
        + "\n".join(rows)
        + "\n</parazettel-recall>"
    )


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = (data.get("prompt") or "").strip()
    if len(prompt) < MIN_PROMPT_CHARS:
        return 0
    try:
        context = recall(prompt)
    except Exception:
        context = None
    if context:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
