# Subtext — Weekly Business/Tech Publication

**Tagline:** Everyone reads the headline. We read the subtext.

**Promise:** Each issue takes a real business/tech story and delivers the product decision underneath it, plus what AI actually does to it.

## Structure

- **BRAND.md** — Persona, principles, voice
- **config.json** — Publication settings (cadence, distribution, sources)
- **drafts/** — Phase 1 samples + weekly drafts
- **published/** — Finished pieces (formatted per medium)
- **HANDOFF.md** — Phase 2 setup checklist

## Publishing Workflow

1. **Discover** — Weekly news sources are scanned (automated Monday morning)
2. **Lens** — Top 3 stories run through viral-subtext (outputs 3 × 10/10 drafts)
3. **Review** — You read drafts (~10 min)
4. **Format** — Pick medium (LinkedIn, newsletter, X) and render using subtext-formats-guide.md
5. **Approve & Post** — Manual post to LinkedIn (or distribution channel)

## Phase 1 (Validated)

✅ Lens engine (viral-subtext.md) — 10/10 quality bar
✅ Sample drafts (Meta, Google, SpaceX) — all forward-worthy
✅ Format guide (per medium — LinkedIn, newsletter, X, video)

## Phase 2 (Next Session)

- Wire news sources (user provides feeds)
- Create discover command
- Set up Monday auto-discovery
- Schedule first week of drafts

See HANDOFF.md for details.

## Quality Bar

Every issue must:
1. **Falsifiable** — not true of any company
2. **Non-consensus-but-right** — fresh angle, not repeating timeline
3. **Gated AI lens** — only include AI angle if it materially changes something
4. **Forward-worthy** — sharp operator would send to their team in under 3 min read

## References

- `viral-subtext.md` — The lens engine (in .claude/commands/)
- `subtext-formats-guide.md` — How to render per medium
- `BRAND.md` — Persona contract
