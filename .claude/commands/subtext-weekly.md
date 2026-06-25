# subtext-weekly

One command for the weekly Subtext run. Chains **discover → lens → review**, then
writes approved issues to `data/subtext/issues.jsonl`. SCRIPT→POST stays manual.
Nothing publishes without the user's explicit "approve."

**Inputs (all optional):**
- `--count N` — candidate episodes to fetch (default 8)
- `--issues N` — issues to draft (default 3)
- `--format` — `linkedin_longform` (default), `newsletter`, `x_thread`, `shortform_script`
- `--no-fetch` — skip the live fetch, reuse today's existing candidates file

---

## Step 1 — Discover (fetch candidates)

Run the fetcher:

```bash
python3 scripts/subtext_fetch.py --count {N|8}
```

This writes `data/subtext/candidates/{YYYY-MM-DD}-candidates.json` — TBOY's recent
episodes (title + description) as candidate stories. If it returns 0 candidates,
stop and report (likely network or a changed channel URL). If `--no-fetch` was
passed, load the most recent candidates file instead.

Load `recon/format-dna.json` for the narrative skeletons (structure only).

## Step 2 — Lens (run viral-subtext)

Hand the candidates to the `viral-subtext` engine (`.claude/commands/viral-subtext.md`):
- CANDIDATE_STORIES = the fetched candidates (title + description + url)
- STORY_COUNT = `--issues` (default 3)
- OUTPUT_FORMAT = `--format` (default linkedin_longform)
- FORMAT_DNA = `recon/format-dna.json` (structural scaffolding only — never copy TBOY's words)

Execute all four steps of viral-subtext: Select (with one-line cut/keep notes) →
Product/Strategy lens → gated AI lens → Render → Self-critique. Flag the weakest issue.

## Step 3 — Review (gate)

Present all drafts with self-scores and the weakest-issue flag. **STOP.** Do not write
anything yet. The user reads and replies with one of:
- `approve` / `approve all` — write every draft
- `approve 1 3` — write only those issues
- edits — revise in place, re-present, wait again

This is the publish gate. Per BRAND.md, the validated take is the deliverable.

## Step 4 — Persist (only after approval)

For each approved issue, append one JSON line to `data/subtext/issues.jsonl` matching
`schemas/subtext-issue.schema.json`:

```json
{"id":"subtext_20260624_001","issue_date":"2026-06-24","source":{"publication":"The Best One Yet (TBOY)","video_id":"...","title":"...","url":"..."},"surface_line":"...","subtext":"...","ps_take":"...","ai_take":null,"ai_lens_skipped_reason":"...","takeaway":"...","scores":{"differentiation":8,"could_anyone_else_write_this":"no, because ..."},"format":"linkedin_longform","status":"approved","weakest_flag":false,"created_at":"<ISO8601>"}
```

`id` = `subtext_{YYYYMMDD}_{NNN}`, NNN incrementing within the day. `status` is `approved`
on write (never `published` — posting is manual). This file is the learning log: the
analyze step reads it to see which reads performed.

## Hard Rules

- STOP at Step 3 review — never auto-write, never POST.
- Structure ≠ copy. The format-DNA gives skeletons; every word is original.
- Gate the AI lens hard. "AI lens: skipped — <reason>" is a good outcome.
- Every take must be falsifiable. If it's true of any company, kill it.
- Ask before scheduling this command or fetching at scale beyond the weekly run.
