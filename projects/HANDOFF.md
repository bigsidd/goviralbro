# Subtext — Phase 2 Handoff

## What's Done (This Session)

✅ BRAND.md — persona, principles, voice guide
✅ viral-subtext.md — the lens engine (Step 0–4 with all gates)
✅ subtext-formats-guide.md — optimal rendering per medium (LinkedIn, newsletter, X, video)
✅ subtext-drafts-phase1.md — 3 × 10/10 sample drafts (Meta, Google, SpaceX)

**Gate:** Passed. All three drafts are forward-worthy.

---

## What's Next (Phase 2 — New Session)

### 1. News Source Setup
User provides: which feeds to monitor (HN, Twitter, Substack, etc.)

### 2. Wire Discover Command
Create `.claude/commands/viral-discover-subtext.md`:
- Input: list of story URLs from the week
- Output: scored candidates (which 3 stories have the most juice?)
- Selection criteria: real decision underneath + non-consensus angle + rewards both lenses

### 3. Wire Weekly Lens Pipeline
One command chains:
```
viral-discover-subtext → viral-subtext (on selected 3) → output to data/angles.jsonl
```

### 4. Schedule Auto-Discover
Use `mcp__scheduled-tasks__*` to run discover every Monday 7am.
- **Note:** Only discover runs on schedule. Lens engine + review + publish stay manual.
- Output: 3 candidate stories waiting in `data/angles.jsonl` when user wakes up.

### 5. Optional: Learnings Loop
After user publishes, log performance (forwards, engagement) to `data/angles.jsonl`.
Agent brain learns what angles actually land.

---

## Files to Reference
- `BRAND.md` — persona contract
- `.claude/commands/viral-subtext.md` — the lens engine
- `data/subtext-formats-guide.md` — format rules per medium
- `data/subtext-drafts-phase1.md` — sample outputs (ref for quality bar)

---

## Questions for User in Next Session
1. Which news sources? (HN, Twitter, Substack, specific beats, other?)
2. Publish cadence? (weekly, bi-weekly, as-needed?)
3. Distribution? (LinkedIn only, or also newsletter/X/other?)
4. Scheduling: run discover every Monday morning?

---

## Notes
- Post-to-publish stays manual. "Nothing publishes without explicit approve."
- Token cost remains ~$0.10–0.15/week.
- No new subscriptions needed.
