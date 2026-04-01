#!/Users/bailey/.local/bin/python3.13
"""
PostCompact hook: create notes from PreCompact extraction markdown,
then perform link discovery. Runs after context compaction completes, so it
can take more time without blocking the user.

Always exits 0 — never disrupts the session.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile
from typing import Optional

INGEST_PROMPT = (
    "You are a Zettelkasten ingestion agent. You will receive markdown with "
    "structured insights extracted from a conversation. Each insight has:\n"
    "- ## Title\n"
    "- Type: note, structure, project, or task (or similar wording)\n"
    "- Tags: #tag1 #tag2\n"
    "- Content (1-4 sentences)\n\n"
    "For each insight:\n"
    "1. If it describes atomic knowledge (note, insight, observation, decision, etc): "
    "call pzk_create_note with note_type='permanent', status='inbox', "
    "tags='chat-capture,<extracted-tags>' (NO # prefix in tags)\n"
    "2. If it describes a framework/mental model (structure, framework, model, pattern, etc): "
    "call pzk_create_note with note_type='structure', status='inbox', "
    "tags='chat-capture,<extracted-tags>' (NO # prefix)\n"
    "3. If it describes a multi-hour/multi-day effort (project, initiative, goal, etc): "
    "call pzk_create_project with status='inbox', source='chat', "
    "tags='chat-capture,<extracted-tags>' (NO # prefix)\n"
    "4. If it describes an action item (task, todo, action, etc): "
    "call pzk_create_task with status='inbox', source='chat', "
    "tags='chat-capture,<extracted-tags>' (NO # prefix). "
    "If a project was just created, reference it with project_id.\n\n"
    "Be flexible with the format - focus on the semantic meaning, not exact wording. "
    "Report which notes/projects/tasks were created (title + ID)."
)

LINK_PROMPT = (
    "You are a Zettelkasten graph curator. Notes have just been created from "
    "a conversation extraction. Your job is to integrate those notes into the vault properly.\n\n"
    "STEP 1 — FIND RECENT CAPTURES:\n"
    "Call pzk_search_notes with status='inbox' tags='chat-capture' to find "
    "the newly created notes.\n\n"
    "STEP 2 — PRUNE:\n"
    "Review each note with status='inbox' and judge:\n"
    "- Is it a duplicate or near-duplicate of an existing note? "
    "Delete the weaker one (pzk_delete_note) and strengthen the survivor "
    "with pzk_update_note.\n"
    "- Is it too vague or context-dependent to have standalone value? "
    "Delete it.\n"
    "- Is it well-formed? Keep it for linking.\n\n"
    "STEP 3 — LINK:\n"
    "For each remaining note, call pzk_find_similar_notes to surface related "
    "existing notes. Create links (pzk_create_link) wherever there is genuine "
    "conceptual overlap — not just shared keywords. Prioritise linking "
    "to permanent notes where the new note supports, extends, or contradicts "
    "an existing idea. Skip weak or superficial matches. Leave all notes with "
    "status='inbox' for human review.\n\n"
    "Rules:\n"
    "- Prefer fewer, stronger notes over many weak ones\n"
    "- Never delete a note that has incoming links from non-fleeting notes\n"
    "- When in doubt, leave it — deletion is irreversible"
)


def load_mcp_config(plugin_root: str) -> Optional[dict]:
    """Load and resolve the plugin's .mcp.json into claude --mcp-config format."""
    mcp_path = os.path.join(plugin_root, ".mcp.json")
    if not os.path.exists(mcp_path):
        return None

    try:
        with open(mcp_path, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:  # pylint: disable=broad-except
        # Hook must never crash - silently skip if MCP config is malformed
        return None

    servers = {}
    for name, config in raw.items():
        resolved = json.loads(os.path.expandvars(json.dumps(config)))
        servers[name] = resolved

    return {"mcpServers": servers}


def find_latest_insights() -> Optional[str]:
    """Find the most recent chat-insights markdown file in ~/.claude/temp/."""
    # Look for insights files in ~/.claude/temp/ directory
    temp_dir = os.path.join(os.path.expanduser("~/.claude"), "temp")

    insights_pattern = os.path.join(temp_dir, "chat-insights-*.md")
    insights_files = glob.glob(insights_pattern)
    if not insights_files:
        return None
    return max(insights_files, key=os.path.getmtime)


def run_ingest(mcp_config: dict, insights_file: str, verbose: bool = False) -> None:
    """Run Claude Haiku to ingest markdown and create notes."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(mcp_config, tmp)
        tmp_path = tmp.name

    try:
        with open(insights_file, "r", encoding="utf-8") as f:
            insights_content = f.read()

        prompt = f"Ingest these insights and create notes:\n\n{insights_content}"

        result = subprocess.run(
            [
                "claude", "-p",
                "--bare",
                "--max-turns", "10",
                "--model", "haiku",
                "--output-format", "text",
                "--mcp-config", tmp_path,
                "--system-prompt", INGEST_PROMPT,
            ],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        if verbose:
            debug_file = f"/tmp/post-compact-ingest-{os.getpid()}.log"
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write("=== INGEST PHASE OUTPUT ===\n\n")
                f.write("STDOUT:\n")
                f.write(result.stdout)
                f.write("\n\nSTDERR:\n")
                f.write(result.stderr)
                f.write(f"\n\nReturn code: {result.returncode}\n")
            print(f"Ingest debug log: {debug_file}", file=sys.stderr)
    finally:
        os.unlink(tmp_path)


def run_linking(mcp_config: dict, verbose: bool = False) -> None:
    """Run Claude Haiku with MCP tools to perform linking and pruning."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as tmp:
        json.dump(mcp_config, tmp)
        tmp_path = tmp.name

    try:
        prompt = (
            "Perform the linking and pruning pass on recently "
            "captured notes with status='inbox' and tags='chat-capture'."
        )

        result = subprocess.run(
            [
                "claude", "-p",
                "--bare",
                "--max-turns", "10",
                "--model", "haiku",
                "--output-format", "text",
                "--mcp-config", tmp_path,
                "--system-prompt", LINK_PROMPT,
            ],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )

        if verbose:
            debug_file = f"/tmp/post-compact-linking-{os.getpid()}.log"
            with open(debug_file, "w", encoding="utf-8") as f:
                f.write("=== LINKING PHASE OUTPUT ===\n\n")
                f.write("STDOUT:\n")
                f.write(result.stdout)
                f.write("\n\nSTDERR:\n")
                f.write(result.stderr)
                f.write(f"\n\nReturn code: {result.returncode}\n")
            print(f"Linking debug log: {debug_file}", file=sys.stderr)
    finally:
        os.unlink(tmp_path)


def main():
    """Entry point: find insights file, ingest notes, then link/prune."""
    try:
        # Check for verbose mode
        verbose = os.environ.get("VERBOSE", "0") == "1"

        # Find the latest insights markdown file
        insights_file = find_latest_insights()
        if not insights_file:
            sys.exit(0)

        # Load MCP config
        plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
        mcp_config = load_mcp_config(plugin_root)
        if not mcp_config:
            sys.exit(0)

        # Phase 1: Ingest markdown and create notes
        run_ingest(mcp_config, insights_file, verbose)

        # Phase 2: Link and prune notes
        run_linking(mcp_config, verbose)

    except Exception:  # pylint: disable=broad-except
        # Hook must never crash - session must continue even if pruning fails
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
