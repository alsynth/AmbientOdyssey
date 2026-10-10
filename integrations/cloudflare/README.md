# Cloudflare Workers: Ambient Odyssey Questlog source integration

**Target identified by the user:** https://ambient-odyssey.ltalsynth.workers.dev

**Integration state:** Prepared against 50 Questlog Q1 quests and 13 installed chapters; **not deployed**. The current Workers site source/account is not available in the connected GitHub repositories and its deployed page could not be fetched from this runtime. Do not replace the existing Worker to install this adapter.

## Non-invasive route handler

The module `quest-atlas-api.mjs` is an **additive API** and does not register a new Worker on its own. It returns `null` for every path outside its namespaced route. After fetching the actual site's Worker source, connect it inside its existing fetch handler:

```js
import { maybeHandleQuestAtlasRequest } from "./integrations/cloudflare/quest-atlas-api.mjs";

export default {
  async fetch(request, env, ctx) {
    const quests = maybeHandleQuestAtlasRequest(request);
    if (quests) return quests;
    // Keep the EXISTING Workers handler for every other request.
    return originalSiteHandler(request, env, ctx);
  }
};
```

The example is illustrative: `originalSiteHandler` must be the original function, not a new dummy implementation. The actual module import path must be adapted to the Worker project layout. **Do not deploy that snippet alone.**

### Available routes, once mounted

| Route | Returns |
| --- | --- |
| `GET /api/ambient-odyssey/quests` | 50 Q1 quest definitions, chapters, source verification label |
| `GET /api/ambient-odyssey/quests?chapter=first_pages&q=shield` | Filtered data for search and navigation |
| `GET /api/ambient-odyssey/quests/chapters` | All 13 Questlog chapters |
| `GET /api/ambient-odyssey/quests/chapters/first_pages` | Chapter metadata and 13 opening quests |
| `GET /api/ambient-odyssey/quests/quests/ao_first_pages_05_craft_a_shield_and_learn_off_han` | Quest details incl. objectives and rewards |

HEAD is supported; unrelated URLs are unaffected; other methods on the API return 405; unknown quest/chapter IDs return 404. No wildcard CORS, authentication bypass, query mutation, or player-progress handling is included.

## Automatic source generation

The source of truth is *never* copied website text. The exporter reads the exact installed modpack Questlog JSON under `release_030/overrides/config/questlog/` and the `docs/questing/QUESTLOG_Q1_INSTALLED_INDEX.json` count/IDs:

```bash
python tools/export_cloudflare_quests.py
python tools/export_cloudflare_quests.py --check
node --test tests/test_cloudflare_quest_atlas.mjs
```

The generated `generated/quest-data.json` and `generated/quest-data.mjs` contain the **same 50 quest definitions**, only public metadata. Do not expose world saves, player names, completion or private server administration. A dedicated CI job checks exact source parity, Node's Worker-compatible Request/Response API, and every known chapter/quest mapping.

## Actual Worker UI work still needed

1. **Identify existing Cloudflare Worker source:** the deployed Worker script via the Cloudflare dashboard (Workers & Pages → ambient-odyssey → Edit code / source export) or its connected deployment repository. Never share account tokens.
2. Inspect its existing routing, navigation, style tokens, menus, content type and deployment workflow.
3. Mount the additive API without taking over `/`, and create a **Questlines** section that uses existing page templates/styles instead of a second unrelated standalone HTML site.
4. Design Q1 chapter cards, quest detail panels, prerequisites, rewards and warnings about untested in-game triggers. The optional FTB Manual and additional adventure tiers can follow.
5. Run Worker-local/request tests, preview deployment and browser QA, then deploy after checking routes and rollback behavior.

**No Cloudflare account has been accessed, no production domain has been changed, and no actual gameplay has been runtime-tested.**
