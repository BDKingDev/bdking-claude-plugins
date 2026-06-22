---
name: pzk-personal-note
description: Converts a short or long source note, AI transcription, or personal voice memo into atomic linked Zettelkasten notes and action-item tasks using the parazettel MCP. Use whenever a user provides a raw transcript, Notion export, or markdown file to add to their knowledge base. Triggers on "process this note", "add this to my Zettelkasten", "atomize this", "convert this to Zettelkasten", or when a markdown file is provided with intent to add it to a vault.
compatibility: requires parazettel MCP (pzk_* tools); uses jdocmunch for long source files
---

Turn a source note into atomic permanent notes and action-item tasks via the parazettel MCP. Add a literature note only when source framing or provenance is worth preserving. Route action items to tasks via `pzk_create_task`.

**Treat literature notes as invisible during normal retrieval.** Anything future-you would search for — a claim, example, contrast, named object, or sequence — must live in a permanent, structure, or hub note body, not only in the literature note. After creating a literature note, run one more pass to externalize anything retrieval-worthy still trapped in it.

**These sources are typically personal voice memos or transcripts** — the speaker is also the vault owner. Their specific examples, reasoning chains, and personal framing are primary material, not noise to filter out.

**Sanitize third-party PII, and only PII.** Sanitize personally identifying information about *other people* — reduce an identifiable third party to a role ("my partner", "a friend") and drop their private names and identifying specifics. Everything else is signal: the vault owner's own content — their work, plans, goals, and personal or sensitive material about themselves — is exactly what future-them wants captured, so keep it specific rather than scrubbing it as "sensitive." Keep any crisis or substance framing factual. Note the sterilization in one phrase in the literature note when it materially changes the source.

**If jdocmunch is available** and the source is a long file: use `search_sections` / `get_section` to pull only relevant parts rather than loading the whole file into context. Process section by section — run the full two-phase workflow on each section, then do a final cross-section hub/structure check at the end.

## Workflow

### Phase 1 — Extract (graph-blind)

**If subagents are available:** spawn the `parazettel-helper:extractor` agent. If the source is a file, pass only the file path — the extractor has `Read` access and will read it directly. If the source is inline text (pasted into conversation), pass the text. The extractor returns a full candidate list with no graph awareness or pruning.

**If subagents are not available:** simulate the extractor by reading the source and writing out all candidates as if the vault were empty — no MCP calls, no consideration of existing notes. Treat this as a strict separate pass before any graph interaction.

The extractor surfaces:

- `observation`, `tactic`, `outcome` claims — see [atomization.md](../../references/atomization.md)
- `process-or-framework` — a reusable "how to do this" flow, setup sequence, or decision path; in personal transcripts this can outrank the abstract lesson behind it
- `action-item` — concrete things to do ("need to set up X", "should try Y this week")
- `object-or-design-decision` — specific choices about named things, tools, or mechanisms
- **Concrete carriers — their own atoms, never compressed into the headline lesson:** specific numbers and unit economics (prices, ratios, conversion math, counts, durations), verbatim scripts and quotable lines, named tools/products, worked examples, and diagnostic questions / screening tests / decision criteria. These are the highest-signal, most-retrievable material and the first thing a shallow pass drops — a headline like "treat it as three parts" must not swallow the per-part detail beneath it.
- **Teaching / how-to-teach layer** — when the source is itself teaching or designing a lesson, course, or video, the *craft* of how to teach it (framing devices, what belongs on a slide, pacing, journey-vs-essay structure) is a separate atom lane from the substance being taught; capture both.
- **Brainstorms, idea lists, and planning** — content/offer/module idea lists, course-design artifacts, swipe files, and loose "what could I make / what would help" ideation. Flag the whole brainstorm as a candidate (usually a `structure` note). This is durable provenance even when it is off-topic for the source, half-formed, rejected in the same breath, or a method the speaker was unsure about (flag those "to test"). The speaker searches for their own past ideas later — preserve them, and keep the reasoning for why an idea was set aside (that failure mode is often the sharpest note).
- **Metaphors and mental models** — if generative (applicable beyond this source), flag as its own candidate
- **Personal framing, lived examples, reasoning sequences** — flag for literature note even if not a standalone permanent
- **All topics present in the source, regardless of proportion** — a transcript that is 80% about marketing and 20% about relationships should produce permanent notes from both. Do not treat the minority topic as less worthy of capture; disparate, unexpected claims from an otherwise unrelated source are often the most valuable to pull.

**Mine line by line on the first pass.** Read the whole source closely and surface every distinct idea — including small observations made in passing and threads that occupy only a little of the runtime. A long, dense, or multi-thread transcript should produce many candidates; getting them all on the first pass is the job, not something to recover with a later re-read. Don't collapse separate threads together or stop at the headline points. Sweep deliberately through the **back third** of the source — re-checks consistently find the first pass kept the front-half headlines and dropped the later threads, where the sharpest reframes and the concrete detail usually live.

Extract only what the **raw** source supports. If the source bundles an AI-generated summary, main points, or action-item list, use those as discovery aids — never mint a permanent-note claim that the raw transcript or body does not back up.

Raw voice-memo ASR is noisy — discard stutter-loops (one line repeated many times), duplicated or garbled fragments, and filler ("yeah yeah yeah", "beeps"); these are transcription artifacts, not the speaker's voice. When a phrase looks distinctively worded, confirm it is intentional emphasis and not an ASR repetition before preserving it.

1. **Read** the source — via jdocmunch sections or from conversation context.
2. **Get the full candidate list** — do not consider existing notes yet.
3. **Decide on a literature note** — create one if the source is long, mixed, or has framing worth preserving. For personal transcripts, bias toward creating one. Keep the summary to 1–3 tight sentences stating the argument, not an abstract.

### Phase 2 — Prune and integrate

4. **Prune** — keep the smallest valid set of permanent notes. The goal is honest, specific insights grounded in what the source actually said — not general advice that could appear in any self-help article. Cut any candidate that: is generic enough to be true without this source, reads like conventional wisdom, or could have been written without the transcript. A pruned note should feel like something only this speaker, in this conversation, would say.
   - **Exception — brainstorms and planning are provenance, not pruned as "generic" or "transient":** a content/offer/module idea list, course-design artifact, or "what could I make" brainstorm is captured (usually as a `structure` note routed into the relevant cluster) and judged by provenance value, not by whether each line is a novel durable claim. The only ideation you skip is something already recorded in the graph. Never collapse a brainstorm into a no-note pass by calling it transient — including when it is off-topic for the source or was rejected in the same breath.
   - **Pure logistics get no note.** Real-time scheduling and coordination state ("text Karina by 3pm", weekend availability, who to message first) is genuinely transient — capture it as a task only if it is a live commitment, otherwise drop it, and mine the transcript for the durable principle embedded in the logistics rather than the schedule itself.
5. **Route action items** — candidates typed as `action-item` go to `pzk_create_task` instead of `pzk_create_note`. Use `source="voice"` for voice memos or `source="transcript"` for other transcripts, with `status="inbox"`. Follow the project resolution flow in [project-resolution.md](../../references/project-resolution.md).
6. **Enrichment pass** — for each **cut** knowledge candidate, search for the closest existing note and apply the atomicity gate (see [atomization.md](../../references/atomization.md)):
   - Keeps existing note at one idea → `pzk_update_note`
   - Would push existing note to two ideas → new note linked with `extends` or `supports`
   - No close match → drop or fold into literature note
7. **Graph comparison** — for each **surviving** knowledge candidate: search for duplicates. Link to existing if already covered; `pzk_update_note` if the source adds something durable.
8. **Create notes and links** — `pzk_create_note` then `pzk_create_link` immediately after each note. Tasks are created in step 5. **Tags follow the controlled vocabulary** (see [tagging.md](../../references/tagging.md)): use `pzk_suggest_tags(text=<the note's claim>)` to shortlist the closest existing tags by meaning (or `pzk_get_all_tags` for the full vocabulary), reuse the closest, and mint a new one only when the concept is genuinely absent — never a near-synonym spelling of an existing tag. For large batches (5+ notes already pruned and deduped), `pzk_ingest_batch` creates all notes + links + tasks in one call with `#N` cross-references. Leave its dedup gate ON even for vetted drafts: by default it creates-and-flags possible duplicates for your review (non-destructive safety net) rather than auto-folding — you judge each flag with the same same-claim-vs-same-topic test as the pre-create sweep. Treat the batch output's "Duplicate review" section as a mandatory step: resolve every line (fold or link) before moving to the next source. **Whole-source duplicates and re-recordings:** if the pre-create sweep flags most of a file's drafts at ≥0.9 against one cluster — *or* surfaces an existing structure/hub note for the same framework at any score — open that note. If it already holds the scaffold, the source is a re-recording or re-teaching: by default create one provenance literature note (it records which recording produced any new angle) linked into the existing cluster, and keep only the genuinely new or sharpened angles as atoms, instead of re-creating the flow. **Partial overlap is the common middle case:** atom count scales with novelty, not source length — a long source that mostly re-treads can correctly yield 2 permanents, and a short novel one 10+.
9. **Hub/structure check** — `pzk_find_central_notes` for the topic. Distinguish the two roles: a `hub` is a broad bucket/map of a cluster and its lanes; a `structure` note is the exact reusable scaffold — a sequence, flow, checklist, or decision path. Don't let one note do both jobs; if the cluster needs both a bucket and an exact flow, create both. Update an existing hub/structure note if found; create one only when several new permanents share a topic with no existing organizer. For a compact framework source whose provenance is a single line, one `structure` note may legitimately carry the scaffold, the hub map, and that provenance together — skip the separate literature note rather than splitting one line of provenance off into its own note. Link each new permanent to the hub/structure it sits under (`reference`/`supports`).
10. **Post-create semantic audit** — run `pzk_find_similar_notes` on each note you just created, then make two passes over the neighbours it surfaces:
    - **Links** — add 1–2 high-value cross-vocabulary / cross-domain links the lexical sweep missed (`pzk_create_link`). Treat loosely-related hits as links, not fold/merge triggers.
    - **Tension check** — judge whether any close neighbour *conflicts* with the new note (an opposing claim, a competing recommendation, or a condition that contradicts it). `pzk_find_tensions` on the new note returns exactly this candidate set (unlinked same-topic neighbours) in one call. On a real tension, reconcile rather than ignore: link `contradicts` (the system auto-adds the reciprocal `contradicted_by`), or `refines` if one note is the special case that resolves the other, or `pzk_update_note` to add the qualifying condition — and surface the tension in the report.
    **Embeddings augment domain memory; they don't replace it.** A low or empty result *suggests* (does not prove) the note is novel — a few ideal matches sit in a different embedding region and surface in neither `search` nor `find_similar`. If you recall an obviously-relevant note that didn't appear, link it manually; several of the best links come only from memory.
11. **Verify** — `pzk_get_linked_notes` to confirm links.

## Tool Order

Use tools in this order unless there is a clear reason not to:

1. Draft and prune the local candidate set first (no MCP calls).
2. **Pre-create sweep** — `pzk_search_notes` (now hybrid lexical+semantic) on each surviving candidate's claim text. Candidates have no ID yet, so `pzk_find_similar_notes` can't run on them. Read the top score as a signal, not a verdict: a **low top score usually means novel → create** (but see the recall caveat in the audit step — it can also mean the best match sits in a different embedding region); a strong, on-claim match → **fold/update**, but first open the match and confirm it's the **same atomic claim, not just the same topic** (dense clusters score genuinely distinct atoms high — over-folding is worst exactly there); a moderate, loosely-related match is a **link candidate, not a fold**. Query with the **full claim** (title + a sentence), not a terse keyword — phrasing strongly affects recall; with embeddings on, `pzk_find_similar_to_text` runs this semantic check on the draft text directly (calibrated cosine). If the semantic sweep errors ("daemon unavailable") or silently returns nothing, do not read that as "novel" — recover/verify embeddings (a known-note self-match probe) or fall back to lexical `pzk_search_notes` before trusting any low score.
3. `pzk_get_note` when an existing note might need updating.
4. `pzk_suggest_tags(text=<the note's claim>)` per note (or `pzk_get_all_tags` for the full list), before tagging — reuse existing tags per [tagging.md](../../references/tagging.md).
5. `pzk_create_note` / `pzk_update_note` / `pzk_create_task` to create items (or `pzk_ingest_batch` for large batches — leave its dedup gate on; it creates-and-flags possible duplicates, and every line of its "Duplicate review" section must be judged: same claim → fold, same topic → keep and link).
6. `pzk_create_link` to connect source and derived notes immediately.
7. **Post-create audit** — `pzk_find_similar_notes` on each *newly created* note. This is the semantic pass: it catches cross-vocabulary / cross-domain links (and productive tensions) the lexical sweep missed — often 1–2 good links per note, though some notes the pass is purely confirmatory. Add those links; don't retro-fold loosely-related hits. `pzk_find_tensions` surfaces the unlinked-neighbour set for the tension judgment in one call.
8. `pzk_get_linked_notes` to verify the result.

## Note Content Formats

**Permanent note — pass as `content`:**

```text
[Body: 1–3 sentences. Title already states the claim — do not restate it.
Second sentence adds a specific detail, named consequence, or edge case
from the source. Cut any sentence that starts "this means" or "this is why"
— that is commentary, not a new fact.
Preserve the speaker's original tone and language where possible — atomize
the idea but don't sand off the voice. If the source uses a distinctive word
or phrase, keep it.]

Source: [path/filename or description of source]
```

**Literature note — pass as `content`:**

```text
Source note: [path/filename]
Source type: AI Transcription
Uploaded by: [name]
Recommended area: [area]
Created time: [original created time from source metadata]
Duration: [duration from source metadata, if present]
Original recording: [URL if present]

Summary:
[1–3 sentences stating the argument. Include one concrete anchor detail
from the source — a specific example, named analogy, or vivid particular.]
```

The metadata block above is for sources that carry that metadata (Notion exports, AI-transcription files with header fields). **For voice memos or inline transcripts that lack it, drop the block:** use a `# Lit: <claim-stating title>` heading, a 1–3 sentence prose summary with one concrete anchor, and a single `Source: <description>` line. **When the source re-treads existing clusters, the literature note's main job becomes the source→graph map:** record in the summary (and in its outgoing link descriptions) what folded into which existing note and exactly what this source adds beyond the cluster.

## Linking

Apply `pzk_create_link` immediately after each note — don't batch at the end. Pass the description as the `description` parameter on the tool call, not written into the note content body.

```text
pzk_create_link(
  source_id="...",
  target_id="...",
  link_type="supports",
  description="Source note defines the core workflow this permanent note distills."
)
```

- `supports` — literature/source → each derived permanent and task
- `refines` — more specific → more general
- `extends` — note adds a distinct consequence or application
- `related` — adjacent, neither specializes the other
- `contradicts` — the note makes a claim that conflicts with the target's (reciprocal `contradicted_by` is auto-added); use when the audit finds a genuine tension to reconcile
- `reference` — hub/structure → notes it indexes

Note: tasks created via `pzk_create_task` with a `project_id` are automatically linked to their project (PART_OF/HAS_PART). You still need to create `supports` links from the literature note to each task.

## Output Report

1. **Candidates** — full list from Phase 1, including literature note flags and action-item typing.
2. **Pruning** — what was cut and why; anything folded back in.
3. **Action items** — tasks created, with project assignment and status.
4. **Enrichment** — cut candidates that strengthened an existing note.
5. **Literature note** — created or skipped, and why.
6. **Notes created/updated** — title, type, note ID; new vs. updated.
7. **Links** — relationship type + one-line rationale each.
8. **Hub/structure actions** — what was done and why, or why nothing was needed.
