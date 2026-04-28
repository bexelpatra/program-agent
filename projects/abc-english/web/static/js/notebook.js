/* ABC English — notebook page.
 *
 * Responsibilities:
 *   - List personal vocabulary with filter/sort/search.
 *   - Expand/collapse each entry (marks viewed on first expand).
 *   - Delete entries with confirmation.
 *   - Link source episodes → /study/{id}#s={sentence_index}.
 */

import { api, toast, fmtDate } from "/static/js/common.js";

// ------------------------------------------------------------ state
const state = {
  entries: [],        // raw list from server
  expanded: new Set(), // terms currently expanded
  viewed: new Set(),   // terms we've already pinged viewed for
  sort: "last_added",
  termType: "",
  q: "",
};

// ------------------------------------------------------------ utils
function $(id) {
  return document.getElementById(id);
}

function esc(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function fmtDateTime(iso) {
  if (!iso) return "-";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return String(iso);
  return d.toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// ------------------------------------------------------------ rendering

function filterBySearch(entries, needle) {
  const n = (needle || "").trim().toLowerCase();
  if (!n) return entries;
  return entries.filter(
    (e) =>
      (e.term || "").toLowerCase().includes(n) ||
      (e.explanation_en || "").toLowerCase().includes(n),
  );
}

function renderExpanded(e) {
  const examples = Array.isArray(e.examples) ? e.examples : [];
  const sources = Array.isArray(e.source_episodes) ? e.source_episodes : [];
  const examplesHtml = examples.length
    ? `<div class="nb-section"><h4>Examples</h4><ul>${examples
        .map(
          (ex) =>
            `<li>${esc(typeof ex === "string" ? ex : ex.text || "")}</li>`,
        )
        .join("")}</ul></div>`
    : "";
  const etymHtml = e.etymology
    ? `<div class="nb-etym-box"><span class="nb-etym-label">Etymology</span><p>${esc(
        e.etymology,
      )}</p></div>`
    : "";
  const sourcesHtml = sources.length
    ? `<div class="nb-section"><h4>Sources</h4><ul class="nb-sources">${sources
        .map((s) => {
          const epId = String(s.episode_id || "");
          const idx = Number(s.sentence_index ?? 0);
          const href = `/study/${encodeURIComponent(epId)}#s=${idx}`;
          return `<li><a class="nb-source-link" href="${href}">${esc(
            epId,
          )} @ sentence ${idx}</a><span class="muted"> — ${esc(
            fmtDateTime(s.added_at),
          )}</span></li>`;
        })
        .join("")}</ul></div>`
    : "";
  return `
    <div class="nb-details">
      <p class="nb-explanation">${esc(e.explanation_en || "")}</p>
      ${etymHtml}
      ${examplesHtml}
      ${sourcesHtml}
    </div>
  `;
}

function renderEntryCard(e) {
  const term = e.term || "";
  const type = e.term_type || "word";
  const addedCount = Number(e.added_count || 1);
  const viewCount = Number(e.view_count || 0);
  const isOpen = state.expanded.has(term);
  return `
    <article class="nb-card${isOpen ? " open" : ""}" data-term="${esc(term)}">
      <header class="nb-card-header">
        <button class="btn btn-ghost nb-toggle" type="button" aria-expanded="${
          isOpen ? "true" : "false"
        }" title="펼치기/접기">
          <span class="nb-caret" aria-hidden="true">${isOpen ? "▾" : "▸"}</span>
          <span class="nb-term">${esc(term)}</span>
        </button>
        <span class="badge badge-${esc(type)}">${esc(type)}</span>
        <span class="nb-count muted">×${addedCount}</span>
        <span class="nb-spacer"></span>
        <button class="btn btn-icon nb-delete" type="button" title="삭제" aria-label="삭제">🗑</button>
      </header>
      <div class="nb-meta muted">
        <span>최초: ${esc(fmtDate(e.first_added))}</span>
        <span>·</span>
        <span>최근 추가: ${esc(fmtDate(e.last_added))}</span>
        <span>·</span>
        <span>최근 조회: ${esc(fmtDate(e.last_viewed) || "-")}</span>
        <span>·</span>
        <span>조회수: ${viewCount}</span>
      </div>
      ${isOpen ? renderExpanded(e) : ""}
    </article>
  `;
}

function render() {
  const list = $("notebook-list");
  const countEl = $("nb-count");
  list.removeAttribute("data-loading");

  const filtered = filterBySearch(state.entries, state.q);
  countEl.textContent = state.q
    ? `${filtered.length}/${state.entries.length}`
    : `${state.entries.length}개`;

  if (!state.entries.length) {
    list.innerHTML = `<p class="nb-empty muted">단어장이 비어있습니다. 학습 페이지에서 단어를 추가해보세요.</p>`;
    return;
  }
  if (!filtered.length) {
    list.innerHTML = `<p class="nb-empty muted">검색 결과가 없습니다.</p>`;
    return;
  }
  list.innerHTML = filtered.map(renderEntryCard).join("");
}

// ------------------------------------------------------------ events

async function loadList() {
  const list = $("notebook-list");
  list.setAttribute("data-loading", "true");
  list.innerHTML = `<p class="muted">로딩 중…</p>`;

  const params = new URLSearchParams();
  params.set("sort", state.sort);
  if (state.termType) params.set("term_type", state.termType);
  // API also supports q, but we re-filter client-side for snappy search.
  try {
    const data = await api.get(`/api/notebook?${params.toString()}`);
    state.entries = Array.isArray(data) ? data : [];
  } catch {
    state.entries = [];
  }
  render();
}

async function handleToggleEntry(card, term) {
  const willOpen = !state.expanded.has(term);
  if (willOpen) {
    state.expanded.add(term);
    // fire-and-forget viewed ping (once per session per term)
    if (!state.viewed.has(term)) {
      state.viewed.add(term);
      api
        .patch(`/api/notebook/${encodeURIComponent(term)}/viewed`)
        .then((updated) => {
          // merge counters back into state so re-render shows fresh values
          const i = state.entries.findIndex(
            (e) => (e.term || "") === term,
          );
          if (i >= 0 && updated && typeof updated === "object") {
            state.entries[i] = { ...state.entries[i], ...updated };
          }
        })
        .catch(() => {
          /* toasted by api wrapper */
        });
    }
  } else {
    state.expanded.delete(term);
  }
  render();
}

async function handleDelete(term) {
  if (!window.confirm(`'${term}'을(를) 단어장에서 삭제할까요?`)) return;
  try {
    await api.del(`/api/notebook/${encodeURIComponent(term)}`);
    state.entries = state.entries.filter((e) => (e.term || "") !== term);
    state.expanded.delete(term);
    toast("삭제되었습니다", "success");
    render();
  } catch {
    /* toasted */
  }
}

function initEvents() {
  const list = $("notebook-list");
  list.addEventListener("click", (ev) => {
    const card = ev.target.closest(".nb-card");
    if (!card) return;
    const term = card.dataset.term || "";
    if (ev.target.closest(".nb-delete")) {
      ev.preventDefault();
      ev.stopPropagation();
      handleDelete(term);
      return;
    }
    if (ev.target.closest(".nb-toggle")) {
      ev.preventDefault();
      handleToggleEntry(card, term);
    }
  });

  const search = $("nb-search");
  search.addEventListener("input", () => {
    state.q = search.value || "";
    render();
  });

  const typeSel = $("nb-type");
  typeSel.addEventListener("change", () => {
    state.termType = typeSel.value || "";
    loadList();
  });

  const sortSel = $("nb-sort");
  sortSel.addEventListener("change", () => {
    state.sort = sortSel.value || "last_added";
    loadList();
  });
}

async function main() {
  initEvents();
  await loadList();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
