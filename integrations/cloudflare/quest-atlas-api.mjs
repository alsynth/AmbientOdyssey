/**
 * Optional Cloudflare Workers Q1 quest API adapter.
 *
 * The existing site's original Worker must call this function and return
 * its Response only if non-null; all unrelated URLs pass through untouched.
 * No HTTP deployment, Cloudflare credentials, or player progress is involved.
 */
import questAtlas from "./generated/quest-data.mjs";

const DEFAULT_PREFIX = "/api/ambient-odyssey/quests";
const chapterById = new Map(questAtlas.chapters.map(ch => [ch.id, ch]));
const questById = new Map(questAtlas.quests.map(q => [q.id, q]));

function jsonResponse(payload, { status = 200, head = false } = {}) {
  return new Response(head ? null : JSON.stringify(payload), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": status === 200 ? "public, max-age=300" : "no-store",
      "x-content-type-options": "nosniff",
    },
  });
}
const problem = (status, message, head) => jsonResponse({ error: message }, { status, head });

/**
 * @param {Request} request Browser/Worker request
 * @param {Object} options Configuration; prefix defaults to an AO namespaced path.
 * @returns {Response|null} null for unrelated site routes
 */
export function maybeHandleQuestAtlasRequest(request, { prefix = DEFAULT_PREFIX } = {}) {
  const url = new URL(request.url);
  const path = url.pathname.replace(/\/+$/, "") || "/";
  if (path !== prefix && !path.startsWith(prefix + "/")) return null;
  const head = request.method === "HEAD";
  if (request.method !== "GET" && !head) {
    return new Response(null, { status: 405, headers: { allow: "GET, HEAD" } });
  }
  const suffix = path.slice(prefix.length);
  if (!suffix) {
    const q = (url.searchParams.get("q") || "").trim().toLowerCase().slice(0, 100);
    const ch = url.searchParams.get("chapter");
    if (ch && !chapterById.has(ch)) return problem(404, "Unknown chapter", head);
    const quests = questAtlas.quests.filter(item => {
      if (ch && item.chapter !== ch) return false;
      if (!q) return true;
      return [item.title, item.description, item.id].join(" ").toLowerCase().includes(q);
    });
    return jsonResponse({
      schema: questAtlas.schema,
      version: questAtlas.version,
      game_version: questAtlas.game_version,
      data_status: questAtlas.data_status,
      chapters: questAtlas.chapters,
      count: quests.length,
      quests,
    }, { head });
  }
  if (suffix === "/chapters") return jsonResponse({ chapters: questAtlas.chapters }, { head });
  if (suffix.startsWith("/chapters/")) {
    const id = suffix.slice("/chapters/".length);
    const chapter = chapterById.get(id);
    if (!chapter) return problem(404, "Unknown chapter", head);
    return jsonResponse({
      chapter, quests: questAtlas.quests.filter(q => q.chapter === id),
    }, { head });
  }
  if (suffix.startsWith("/quests/")) {
    const id = suffix.slice("/quests/".length).replace(/^questlog:/, "");
    const quest = questById.get(id);
    if (!quest) return problem(404, "Unknown quest", head);
    return jsonResponse({ quest, chapter: chapterById.get(quest.chapter) }, { head });
  }
  return problem(404, "Unknown quest API route", head);
}

export const questAtlasMeta = Object.freeze({
  source: "release_030/overrides/config/questlog/",
  chapters: questAtlas.chapters.length,
  quests: questAtlas.quests.length,
  status: "source-authored, not Minecraft runtime tested",
});
