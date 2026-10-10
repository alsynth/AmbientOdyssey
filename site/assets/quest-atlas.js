(() => {
  "use strict";
  const atlas = window.AO_QUEST_DATA;
  const $ = (id) => document.getElementById(id);
  const chapterList = $("chapters");
  const questGrid = $("questGrid");
  const dialog = $("questDialog");
  const questMap = new Map((atlas?.quests ?? []).map(q => [q.id, q]));
  const chapters = new Map((atlas?.chapters ?? []).map(c => [c.id, c]));
  let active = "all";

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = String(text);
    return node;
  }
  function append(parent, tag, cls, text) {
    const node = el(tag, cls, text);
    parent.appendChild(node);
    return node;
  }
  function shorten(str, n = 175) {
    return str.length <= n ? str : str.slice(0, n).replace(/\s+\S*$/, "") + "…";
  }
  function strip(s) { return String(s ?? "").replace(/^questlog:/, ""); }
  function pretty(s) { return String(s ?? "").replace(/^[^:]+:/, "").replaceAll("_", " "); }
  function chapterName(slug) { return chapters.get(slug)?.name || pretty(slug); }
  function objectiveText(obj) {
    const kind = strip(obj.type);
    if (kind === "read") return obj.name || "Read this field note";
    if (kind === "item_obtain") return obj.name || ("Obtain " + (obj.required_amount || 1) + " × " + pretty(obj.item));
    if (kind === "item_equip") return obj.name || ("Equip " + pretty(obj.item));
    if (kind === "visit_biome") return obj.name || ("Visit " + pretty(obj.biome));
    if (kind === "visit_structure") return obj.name || ("Find " + pretty(obj.structure));
    if (kind === "visit_dimension") return obj.name || ("Enter " + pretty(obj.dimension));
    if (kind === "stat") return obj.name || ("Progress: " + pretty(obj.stat));
    if (kind === "enchant") return obj.name || "Enchant an item";
    if (kind === "quest_complete") return "Finish: " + (questMap.get(strip(obj.quest))?.title || pretty(obj.quest));
    return obj.name || pretty(kind);
  }
  function hasType(obj, filter) {
    const kind = strip(obj.type);
    return kind === filter || (filter === "visit" && kind.startsWith("visit_")) ||
      (kind === "or" && (obj.objectives || []).some(child => hasType(child, filter)));
  }
  function questSearch(q) {
    const ch = chapterName(q.chapter);
    const objectiveTerms = JSON.stringify(q.objectives);
    return [q.id, q.title, q.description, q.icon, ch, objectiveTerms].join(" ").toLowerCase();
  }
  function chapterButton(slug, label, amount) {
    const b = el("button", "chapter" + (active === slug ? " active" : ""));
    b.type = "button";
    b.setAttribute("aria-pressed", String(active === slug));
    append(b, "span", "chapter-name", label);
    append(b, "span", "chapter-count", amount);
    b.addEventListener("click", () => {
      active = slug;
      renderChapters();
      renderQuests();
    });
    return b;
  }
  function renderChapters() {
    chapterList.replaceChildren();
    chapterList.appendChild(chapterButton("all", "All chapters", atlas.quests.length));
    atlas.chapters.forEach(c => chapterList.appendChild(chapterButton(c.id, c.name, c.quest_count)));
    $("chapterMeta").textContent = String(atlas.chapters.length) + " chapters";
  }
  function mainType(q) {
    const a = q.objectives[0];
    const type = a ? strip(a.type) : "read";
    if (type === "or") return "Alternate paths";
    if (type === "item_obtain" || type === "item_equip") return "Equipment";
    if (type.startsWith("visit_")) return "Exploration";
    if (type === "stat") return "Activity";
    if (type === "enchant") return "Crafting";
    return "Field note";
  }
  function openQuest(q) {
    $("dialogChapter").textContent = chapterName(q.chapter);
    $("dialogTitle").textContent = q.title;
    $("dialogId").textContent = "questlog:" + q.id;
    $("dialogDescription").textContent = q.description;
    $("dialogObjectives").replaceChildren();
    q.objectives.forEach(obj => renderObjective($("dialogObjectives"), obj));
    $("dialogPrereqs").replaceChildren();
    if (!q.prerequisites.length) {
      append($("dialogPrereqs"), "div", "detail-row", "No required prior quests.");
    }
    q.prerequisites.forEach(p => {
      if (strip(p.type) !== "quest_complete") {
        append($("dialogPrereqs"), "div", "detail-row", objectiveText(p));
        return;
      }
      const id = strip(p.quest);
      const pre = questMap.get(id);
      const button = append($("dialogPrereqs"), "button", "linked-quest", pre?.title || id);
      button.type = "button";
      button.addEventListener("click", () => {
        if (!pre) return;
        dialog.close();
        openQuest(pre);
      });
    });
    $("dialogRewards").replaceChildren();
    if (!q.rewards.length) append($("dialogRewards"), "div", "detail-row", "No completion reward — the discovery itself matters.");
    q.rewards.forEach(reward => {
      const type = strip(reward.type);
      const text = type === "experience" ? (reward.experience + " experience") :
        type === "item" ? ((reward.count || 1) + " × " + pretty(reward.item)) :
        pretty(type);
      append($("dialogRewards"), "div", "detail-row", text);
    });
    if (typeof dialog.showModal === "function") {
      if (!dialog.open) dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
    try {
      const u = new URL(window.location.href);
      u.searchParams.set("quest", q.id);
      history.replaceState(null, "", u);
    } catch (_) { /* offline URL handling remains optional */ }
  }
  function renderObjective(parent, obj) {
    if (strip(obj.type) === "or") {
      const group = append(parent, "div", "detail-or");
      append(group, "div", "minor", obj.name || "Choose one of these paths:");
      (obj.objectives || []).forEach(o => renderObjective(group, o));
      return;
    }
    append(parent, "div", "detail-row", objectiveText(obj));
  }
  function renderQuests() {
    const text = $("search").value.trim().toLowerCase();
    const type = $("type").value;
    const quests = atlas.quests.filter(q => (active === "all" || q.chapter === active) &&
      (!text || questSearch(q).includes(text)) &&
      (type === "all" || q.objectives.some(o => hasType(o, type))));
    const ch = chapters.get(active);
    $("heading").textContent = ch ? ch.name : "All chapters";
    $("subheading").textContent = ch ? "A path through the " + ch.name.toLowerCase() + " questline." :
      "Choose your own route through Ambient Odyssey.";
    $("resultCount").textContent = quests.length + (quests.length === 1 ? " quest" : " quests");
    questGrid.replaceChildren();
    $("empty").hidden = quests.length > 0;
    for (const q of quests) {
      const card = el("button", "quest-card");
      card.type = "button";
      card.setAttribute("aria-label", "Open quest " + q.title);
      const top = append(card, "div", "card-top");
      append(top, "span", "card-num", chapterName(q.chapter).toUpperCase() + " / " + String(q.sort_order).padStart(2, "0"));
      append(top, "span", "card-tag", mainType(q));
      append(card, "h3", "", q.title);
      append(card, "p", "", shorten(q.description.replace(/\s+/g, " ")));
      const foot = append(card, "div", "card-foot");
      append(foot, "span", "", q.objectives.length + (q.objectives.length === 1 ? " objective" : " objectives"));
      if (q.prerequisites.length) append(foot, "span", "", "↳ Prerequisites");
      if (q.rewards.length) append(foot, "span", "", "✧ Rewards");
      card.addEventListener("click", () => openQuest(q));
      questGrid.appendChild(card);
    }
  }
  if (!atlas || !Array.isArray(atlas.chapters) || !Array.isArray(atlas.quests)) {
    $("questGrid").textContent = "Quest data is missing. Run 'python tools/export_quest_atlas.py' or open the complete website ZIP.";
    $("resultCount").textContent = "Data unavailable";
    return;
  }
  $("questCount").textContent = String(atlas.quests.length);
  $("chapterCount").textContent = String(atlas.chapters.length);
  $("version").textContent = atlas.version;
  $("search").addEventListener("input", renderQuests);
  $("type").addEventListener("change", renderQuests);
  $("clear").addEventListener("click", () => {
    active = "all"; $("search").value = ""; $("type").value = "all";
    renderChapters(); renderQuests();
    $("search").focus();
  });
  $("closeDialog").addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", e => { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener("close", () => {
    try {
      const u = new URL(window.location.href);
      u.searchParams.delete("quest");
      history.replaceState(null, "", u);
    } catch (_) {}
  });
  renderChapters();
  renderQuests();
  try {
    const qid = new URL(window.location.href).searchParams.get("quest");
    if (qid && questMap.has(qid)) openQuest(questMap.get(qid));
  } catch (_) {}
})();
