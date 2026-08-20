# goviralbro — Content & Monetization

Stacks on top of `~/code/bigsidd/CLAUDE.md` (persona + operating mode + brand context) and global `~/.claude/CLAUDE.md`.

## Content & Monetization

Two distinct tracks — run them differently:

**Track 1: LinkedIn Personal Brand**
Real identity, linked account. AI-assisted, human-posted. Quality > quantity.
- Content chain: `content-engine` → `viral-script` (LinkedIn format) → manual review → post
- For deep topics: `deep-research` → `article-writing` → `content-engine`
- Log what resonates after each post → `claude-mem`
- No LinkedIn MCP yet. Manual posting is intentional — identity content needs a human review gate.

**Track 2: New Automated Channels (YouTube / Instagram / TikTok)**
New accounts only — NOT personal social media. Automation-first, niche testing at scale.
Pipeline lives at `~/code/bigsidd/goviralbro/`.
API keys required: add to `~/code/bigsidd/goviralbro/.env` (OpenAI, YouTube Data API v3 — use new Google account per channel).

**Activate goviralbro only after a niche is validated:**
1. Validate niche first: `market-research` + `data-scraper-agent` + 5 manual posts → observe signal
2. If signal found: `viral-setup` → `viral-onboard` (creates agent-brain.json) → `viral-discover`
3. Then set up cron via `mcp__scheduled-tasks__*` per `docs/CRON-SETUP.md`

| Task | Route |
|---|---|
| Niche validation before activating | `market-research` → `data-scraper-agent` |
| New channel or topic setup (post-validation) | `/viral-setup` → `/viral-onboard` |
| Weekly content production | `/viral-discover` → `/viral-angle` → `/viral-script` |
| Performance review + brain update | `/viral-analyze` → `/viral-update-brain` |

SEED type for this project: **Campaign** (tight rigor, ship fast, iterate on performance data).
After each `/viral-analyze` run → save performance learnings to claude-mem so the agent brain compounds across sessions.

**Signal before infrastructure. Validate first, then automate what's working.**

**Batch Playbook — speed default:**
- Creating any content piece → `/content-pack [topic]` (fans out angle + script + hooks + competitive analysis simultaneously — never do these sequentially)

---

## Python (goviralbro and future projects)

| Task | Skill |
|---|---|
| Writing Python code | `python-patterns` |
| Data scraping or recon pipeline | `data-scraper-agent` |
| Automation loops | `continuous-agent-loop` |
| Parallelizing multiple scraping/automation tasks | Dispatch subagents in a single message per global CLAUDE.md's Delegation & Parallelization rule |

---

## Social Media & Side Hustle Automation

Everything needed to build, run, and scale social media channels and side hustles.

### Content Creation
| Task | Route |
|---|---|
| X/LinkedIn/Instagram posts and threads | `content-engine` |
| Distributing content across platforms | `content-engine` → `crosspost` |
| Long-form article or newsletter | `article-writing` |
| AI-generated images for posts | `fal-ai-media` (ECC) |
| Short-form video scripts (Reels, Shorts, TikTok) | `viral-script` |
| Video editing or reel compilation | `video-editing` (ECC) |
| Quick deck, doc, or one-pager for a side hustle | `anthropic-skills:pptx` or `frontend-slides` |

### Research & Discovery
| Task | Route |
|---|---|
| Finding viral content to model | `viral-discover` |
| Competitor and market research | `market-research` → `deep-research` |
| Audience and account research | `common-room:account-research` |
| X/Twitter API integrations | `x-api` (ECC) |

### Automation & Growth
| Task | Route |
|---|---|
| Weekly content production loop | `/viral-discover` → `/viral-angle` → `/viral-script` |
| Performance review + brain update | `/viral-analyze` → `/viral-update-brain` |
| Scheduling content or automation | `mcp__scheduled-tasks__*` |
| Building automated posting pipelines | `continuous-agent-loop` + `autonomous-loops` |
| Running multiple content experiments in parallel | Dispatch subagents in a single message per global CLAUDE.md's Delegation & Parallelization rule |
| New channel setup | `/viral-setup` → `/viral-onboard` |

### Outreach & Monetization
| Task | Route |
|---|---|
| Brand partnership outreach emails | Gmail MCP — verify the connected account first (identity map in global CLAUDE.md) |
| Sponsorship or collab proposals | `content-engine` (brand partnership framing) + `anthropic-skills:pptx` for deck |
| Affiliate or ad campaign tracking | Apollo (`apollo:*`) for lead management |
