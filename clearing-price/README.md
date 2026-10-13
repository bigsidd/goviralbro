# Clearing Price

A column, every other Tuesday: one big business story, follow the money, then one dated call readers can vote against. Lives at [clearingprice.substack.com](https://clearingprice.substack.com) and on LinkedIn.

## Cards

One locked template; only the words change each issue.

```bash
cd clearing-price/cards
NODE_PATH=$(npm root -g) node render.js data/issue01-openai.json ../out/issue01-openai   # writes -tall.png (1080x1350) and -wide.png (1200x627)
NODE_PATH=$(npm root -g) node logo.js ../out/clearing-price-logo.png
```

Data fields: `issue` (the date tag), `kicker`, `call`, `sub`, `date` (settle date on the price tag), `by`. Use curly apostrophes in the data.

Brand: cream `F6F3EC`, orange `E4572E`, ink `111111`, Source Serif 4 and Source Sans 3 (OFL, in `cards/fonts`). Headline size steps down automatically for longer calls. Design refreshes happen deliberately, once a quarter, not per issue; v2 merged the typography and controlled-UX passes (bencium skills, Oct 13 2026).

## Issues

Final copy for each issue lives in `issues/`, rendered cards in `out/`.
