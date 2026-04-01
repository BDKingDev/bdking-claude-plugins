#!/Users/bailey/.local/bin/python3.13
"""
PreCompact hook: use Claude Haiku to extract Zettelkasten-worthy ideas
and action items from the conversation transcript, creating notes/tasks
directly via the parazettel MCP before context is compressed.

Always exits 0 — never blocks compaction.
"""
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

SYSTEM_PROMPT = (
    "You are a Zettelkasten extraction agent. Review this conversation chunk "
    "and output structured markdown for any insights worth capturing.\n\n"
    "For atomic insights, output:\n"
    "```\n"
    "## [Claim-style title]\n"
    "Type: note\n"
    "Tags: #chat-capture #[domain-tag]\n\n"
    "[1-3 sentences explaining the insight, decision rationale, or gotcha]\n"
    "```\n\n"
    "For structure notes (major organizing hubs only), output:\n"
    "```\n"
    "## [Major system or framework name]\n"
    "Type: structure\n"
    "Tags: #chat-capture #[domain-tag]\n\n"
    "[2-4 sentences describing the system/framework and its major components]\n"
    "```\n"
    "IMPORTANT: Structure notes must be broad enough to house 10+ permanent notes. "
    "Examples: 'Claude Hooks', 'PE Jira Board', 'eaze.com Checkout Flow'. "
    "Narrow frameworks with only 2-5 sub-concepts should be Type: note instead.\n\n"
    "For projects (multi-hour/multi-day efforts only), output:\n"
    "```\n"
    "## [Project name]\n"
    "Type: project\n"
    "Tags: #chat-capture #[domain-tag]\n\n"
    "[2-3 sentences describing the project goal and scope]\n"
    "```\n"
    "IMPORTANT: Projects must be substantial efforts (several hours or 1+ days). "
    "Only create if user explicitly said they want to work on something. "
    "Simple tasks should be Type: task, not project.\n\n"
    "For action items, output:\n"
    "```\n"
    "## [Action title]\n"
    "Type: task\n"
    "Tags: #chat-capture #action-item\n\n"
    "[What needs to be done and why]\n"
    "NOTE: Tasks should reference a project or area if mentioned in conversation.\n"
    "```\n\n"
    "Capture:\n"
    "- Architectural decisions with their rationale (Type: note)\n"
    "- Non-obvious debugging findings (Type: note)\n"
    "- Design trade-offs that were explicitly weighed (Type: note)\n"
    "- Pattern discoveries or gotchas (Type: note)\n"
    "- Narrow frameworks/workflows with 2-5 concepts (Type: note)\n"
    "- Major organizing frameworks that could house 10+ notes (Type: structure)\n"
    "- Multi-hour/multi-day efforts user wants to tackle (Type: project)\n"
    "- Concrete follow-up action items (Type: task)\n\n"
    "Rules:\n"
    "- Title notes as claims (e.g. 'BSD sed ignores GNU inline labels')\n"
    "- Title structures as major hubs (e.g. 'Claude Hooks', 'PE Jira Board')\n"
    "- Title projects as goals (e.g. 'Implement PostCompact hook integration')\n"
    "- Most frameworks should be Type: note unless they're broad organizing systems\n"
    "- Projects require high bar: only substantial multi-hour/multi-day efforts\n"
    "- Tasks should note which project/area they belong to if mentioned\n"
    "- Use semantic links (supports, extends, part-of) to show relationships\n"
    "- Skip mechanical changes, obvious patterns, standard practice\n"
    "- If nothing clears the bar, output 'No insights captured.'\n"
    "- Be selective: 0-3 insights per chunk is normal"
)




def chunk_transcript(transcript: str, chunk_size: int = 400000, overlap: int = 40000, test_mode: bool = False) -> list[str]:
    """Split transcript into overlapping chunks to fit Haiku's context window.

    Args:
        transcript: Full conversation transcript
        chunk_size: Target size per chunk in characters (~100K tokens)
        overlap: Overlap between chunks in characters (~10K tokens)
        test_mode: If True, return only the last chunk for testing

    Returns:
        List of transcript chunks with overlap at boundaries
    """
    if len(transcript) <= chunk_size:
        return [transcript]

    chunks = []
    start = 0

    while start < len(transcript):
        end = min(start + chunk_size, len(transcript))
        chunks.append(transcript[start:end])

        # Move start forward by chunk_size minus overlap
        start += chunk_size - overlap

        # Stop if we've covered the whole transcript
        if end >= len(transcript):
            break

    # In test mode, return only the last chunk
    if test_mode and chunks:
        return [chunks[-1]]

    return chunks


def run_haiku(transcript: str) -> str:
    """Run Claude Haiku against the transcript. Returns stdout."""
    result = subprocess.run(
        [
            "claude", "-p",
            "--bare",
            "--max-turns", "10",
            "--model", "haiku",
            "--output-format", "text",
            "--system-prompt", SYSTEM_PROMPT,
            (
                "Review this conversation transcript and output structured markdown "
                "for any Zettelkasten-worthy insights or action items."
            ),
        ],
        input=transcript,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    return result.stdout.strip()


def main():
    """Entry point: load transcript, run Haiku extraction, output results."""
    # Check for test mode
    test_mode = os.environ.get("TEST_MODE", "0") == "1"
    verbose = os.environ.get("VERBOSE", "0") == "1"

    try:
        data = json.load(sys.stdin)
        transcript_path = data.get("transcript_path", "")

        if not transcript_path or not os.path.exists(transcript_path):
            if verbose:
                print(f"ERROR: No transcript path or file doesn't exist: {transcript_path}", file=sys.stderr)
            sys.exit(0)

        if verbose:
            print(f"Loading transcript from: {transcript_path}", file=sys.stderr)

        with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
            transcript = f.read()

        if verbose:
            print(f"Transcript size: {len(transcript)} characters", file=sys.stderr)

        if len(transcript) < 500:
            if verbose:
                print("Transcript too short, skipping", file=sys.stderr)
            sys.exit(0)

        # Split transcript into chunks if needed
        chunks = chunk_transcript(transcript, test_mode=test_mode)
        if verbose:
            print(f"Created {len(chunks)} chunk(s) (test_mode={test_mode})", file=sys.stderr)

        results = []

        # Process chunks in parallel batches
        max_workers = 4  # Process 4 chunks at a time to avoid rate limits

        def process_chunk(chunk_index: int, chunk_text: str) -> tuple[int, Optional[str]]:
            """Process a single chunk and return (index, result)."""
            try:
                if verbose:
                    print(f"[Chunk {chunk_index}] Starting processing ({len(chunk_text)} chars)", file=sys.stderr)
                chunk_result = run_haiku(chunk_text)
                if verbose:
                    print(f"[Chunk {chunk_index}] Completed:\n{chunk_result[:200]}...\n", file=sys.stderr)
                if chunk_result and chunk_result.strip() and "No insights captured" not in chunk_result:
                    return (chunk_index, chunk_result)
                return (chunk_index, None)
            except Exception as e:  # pylint: disable=broad-except
                if verbose:
                    print(f"[Chunk {chunk_index}] ERROR: {e}", file=sys.stderr)
                return (chunk_index, None)

        if verbose:
            print(f"\nProcessing {len(chunks)} chunks in parallel (max {max_workers} at a time)...\n", file=sys.stderr)

        # Submit all chunks for processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all chunks
            futures = {
                executor.submit(process_chunk, i, chunk): i
                for i, chunk in enumerate(chunks, 1)
            }

            # Collect results as they complete
            chunk_results = {}
            for future in as_completed(futures):
                chunk_index, result = future.result()
                if result is not None:
                    chunk_results[chunk_index] = result

        # Sort results by chunk index to maintain order
        results = [chunk_results[i] for i in sorted(chunk_results.keys())]

        if verbose:
            print(f"\nCompleted: {len(results)} chunks with insights out of {len(chunks)} total", file=sys.stderr)

        # Write results to session directory
        if results:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

            # Store insights in ~/.claude/temp/ directory
            temp_dir = os.path.join(os.path.expanduser("~/.claude"), "temp")

            # Ensure temp directory exists
            os.makedirs(temp_dir, exist_ok=True)

            output_path = os.path.join(temp_dir, f"chat-insights-{timestamp}.md")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write("# Chat Insights\n\n")
                f.write(f"Extracted from conversation transcript\n")
                f.write(f"Chunks processed: {len(chunks)}\n")
                f.write(f"Insights found: {len(results)}\n\n")
                f.write("---\n\n")
                f.write("\n\n---\n\n".join(results))

            chunk_info = f" (processed {len(chunks)} chunks)" if len(chunks) > 1 else ""
            output = {
                "additionalContext": (
                    f"[PreCompact hook] Haiku extracted {len(results)} insight(s){chunk_info} "
                    f"→ {output_path}"
                )
            }
            print(json.dumps(output))
        elif verbose:
            print("No results captured from any chunks", file=sys.stderr)

    except Exception as e:  # pylint: disable=broad-except
        if verbose:
            print(f"FATAL ERROR: {e}", file=sys.stderr)
        # Hook must never crash - compaction must proceed even if extraction fails
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
