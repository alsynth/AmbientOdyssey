# R5 corrections report (15 October 2026)

Applies the owner's R5 decisions handoff over the earlier packet. **Nothing has been pushed or merged since the corrections arrived.** All commits listed below are local only.

## What I changed to match the corrections

| Earlier item | Conflict | Change (local commit) |
|---|---|---|
| Swords route doc recommended dropping the 6 legacy IDs | Owner: keep all 17 | Recommendation withdrawn, keep-all-17 decision recorded (`feature/simply-swords-full-pool` `2c45151`, `92cf900`). The pool code was never changed. |
| Packager doc recommended the R5/R6 split | Split is a proposal only | Marked proposal-only (same commit `2c45151`) |
| Cornelia proof doc proposed an assist/contribution credit fix | No proximity or party credit | Proposal withdrawn, never applied (`feature/pinnacle-cornelia` `65129a9`) |
| Grand audit recommended approving all five | All five stay PENDING | Withdrawn; per-table evidence added (`status/grand-five-pool-audit` `f880e7c`, `6067390`) |
| Git history audit recommended a rewrite + force-push | No force-push or filtering | Withdrawn; audit marked read-only (`hygiene/untrack-jars` `5743abf`) |

Nothing was reverted in code or data: no approval flag was ever set, the Annihilator was never added, no legacy ID was ever dropped, and git history was never rewritten. No license table was touched.

## Task status

| Task | Approved | Implemented | Statically verified | In-game tested | Multiplayer tested | Blocked |
|---|---|---|---|---|---|---|
| R4 restore | n/a | **restored** | **yes**: ZIP `31b037a7…6c6d`, rollback `15a66db3…2dab` and report `8b094b91…a55b` match the receipt; 5,399/5,399 members match; 337 CF refs; campaign JAR SHA matches; 10 custom JARs | no | no | — |
| B: T2–T6 Scrap/Treasure | intent only | no | spec search done | no | no | **yes**: no selected rates exist; 5 values missing ([doc](T2_SCRAP_TREASURE_APPROACH_A.md)) |
| Simply Swords 17 audit | keep all 17 | no change needed | **yes**: 6 obsolete aliases (all duplicates of 2 base items), 0 incompatible ([audit](../simplyswords-full-pool-20261015/UNIQUE_17_ALIAS_AUDIT.md), on the swords branch) | no | no | boss-roll inclusion question open |
| Cornelia credit | rule approved | existing gate already follows it; no change | **yes**: vanilla kill-credit bytecode + Cornelia damage filter ([doc](CORNELIA_KILL_CREDIT_POLICY.md)) | no | no | summon attribution needs an engine test |
| Annihilator | **no** | no | facts only ([proposal](ANNIHILATOR_REGALIA_PROPOSAL.md)) | no | no | your decision |
| Grand five pools | **no, PENDING** | no | **yes** ([evidence](GRAND_FIVE_POOL_EVIDENCE_PER_TABLE.md)) | no | no | your approvals; table 5 trigger scope |
| R5 build | no | no | — | no | no | waits on Grand approvals; R4 is now available |

## Files
- Restored R4 artifacts: kept in a local work folder outside the repo (not committed).
- No ZIP or build output was deleted.
