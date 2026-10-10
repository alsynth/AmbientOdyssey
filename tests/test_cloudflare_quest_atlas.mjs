import assert from "node:assert/strict";
import test from "node:test";
import { maybeHandleQuestAtlasRequest, questAtlasMeta } from "../integrations/cloudflare/quest-atlas-api.mjs";
const origin = "https://ambient-odyssey.ltalsynth.workers.dev";
const prefix = "/api/ambient-odyssey/quests";
function request(path, options) { return new Request(origin + path, options); }
async function call(path, options) {
  const res = maybeHandleQuestAtlasRequest(request(path, options));
  return { status: res.status, json: res.status === 405 || options?.method === "HEAD" ? null : await res.json(), res };
}
test("non-quest Worker paths pass through unchanged", () => {
  for (const path of ["/", "/api/news", "/quests", "/api/ambient-odyssey/questlines"]) {
    assert.equal(maybeHandleQuestAtlasRequest(request(path)), null);
  }
});
test("entire source-backed index has 50 Q1 quests and 13 chapters", async () => {
  assert.deepEqual([questAtlasMeta.quests, questAtlasMeta.chapters], [50,13]);
  const { status, json } = await call(prefix);
  assert.equal(status, 200);
  assert.equal(json.quests.length, 50);
  assert.equal(json.chapters.length, 13);
  assert.equal(json.data_status.includes("not verified"), true);
});
test("chapter API and filtered listings agree", async () => {
  const all = (await call(prefix + "/chapters")).json.chapters;
  assert.equal(all.reduce((n,ch)=>n+ch.quest_count,0),50);
  const chapter = await call(prefix + "/chapters/first_pages");
  assert.equal(chapter.json.chapter.id,"first_pages");
  assert.equal(chapter.json.quests.length,13);
  const filtered = await call(prefix + "?chapter=first_pages&q=shield");
  assert.equal(filtered.json.quests.length,1);
  assert.match(filtered.json.quests[0].title,/Shield/);
});
test("individual quest preserves objectives, prerequisites and rewards", async () => {
  const r = await call(prefix + "/quests/ao_first_pages_05_craft_a_shield_and_learn_off_han");
  assert.equal(r.status,200);
  assert.equal(r.json.quest.objectives[0].item, "minecraft:shield");
  assert.equal(r.json.quest.rewards[0].experience,35);
  assert.equal(r.json.quest.prerequisites[0].type,"questlog:quest_complete");
});
test("unknown chapter and quest are explicit 404s", async () => {
  assert.equal((await call(prefix+"?chapter=does-not-exist")).status,404);
  assert.equal((await call(prefix+"/chapters/nonexistent")).status,404);
  assert.equal((await call(prefix+"/quests/does-not-exist")).status,404);
});
test("method restrictions, HEAD behavior and safe JSON headers", async () => {
  const bad = await call(prefix,{method:"POST"});
  assert.equal(bad.status,405);
  assert.equal(bad.res.headers.get("allow"),"GET, HEAD");
  const head = await call(prefix,{method:"HEAD"});
  assert.equal(head.status,200);
  assert.equal(await head.res.text(),"");
  const res=(await call(prefix)).res;
  assert.match(res.headers.get("content-type"),/application\/json/);
  assert.equal(res.headers.get("x-content-type-options"),"nosniff");
});
test("no player identifiers or world progress fields leak", async () => {
  const { json }=await call(prefix);
  const s=JSON.stringify(json).toLowerCase();
  assert.equal(s.includes("player_uuid"),false);
  assert.equal(s.includes("player_name"),false);
  assert.equal(s.includes("completed_at"),false);
});
