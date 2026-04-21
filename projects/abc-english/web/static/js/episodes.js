/* ABC English — episodes list page.
 *
 * Loads GET /api/episodes, renders a filterable card list.
 * Client-side search is a simple title substring match.
 */

import { api, fmtDate, fmtDuration, toast } from "/static/js/common.js";

const LIST_EL_ID = "episode-list";

/** In-memory cache of the last fetched list for client-side filtering. */
let _episodes = [];

function _escape(s) {
  return String(s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function _renderCard(ep) {
  const id = _escape(ep.episode_id);
  const title = _escape(ep.title || ep.episode_id || "(제목 없음)");
  const date = fmtDate(ep.published_date);
  const dur = fmtDuration(ep.duration_seconds);
  const sc = Number(ep.sentence_count || 0);
  const hasT = !!ep.has_transcript;
  const badge = hasT
    ? `<span class="badge badge-success" title="공식 transcript 있음">transcript</span>`
    : `<span class="badge badge-muted" title="transcript 없음">no transcript</span>`;
  return `
    <a class="episode-card" href="/study/${id}" data-episode-id="${id}">
      <div class="episode-card-title">${title}</div>
      <div class="episode-card-meta">
        <span class="episode-card-date">${date || "-"}</span>
        <span class="episode-card-dot">•</span>
        <span class="episode-card-dur">${dur}</span>
        <span class="episode-card-dot">•</span>
        <span class="episode-card-sc">${sc} sentences</span>
        ${badge}
      </div>
    </a>
  `;
}

function _renderList(container, items) {
  if (!items.length) {
    container.innerHTML = `<p class="muted">일치하는 에피소드가 없습니다.</p>`;
    return;
  }
  container.innerHTML = `
    <div class="episode-cards">
      ${items.map(_renderCard).join("")}
    </div>
  `;
}

function _applyFilter(container, needle) {
  const n = (needle || "").trim().toLowerCase();
  if (!n) {
    _renderList(container, _episodes);
    return;
  }
  const filtered = _episodes.filter((ep) =>
    String(ep.title || "").toLowerCase().includes(n),
  );
  _renderList(container, filtered);
}

function _buildToolbar(container) {
  // Inject a search toolbar just above the container if not already present.
  if (document.getElementById("episode-search")) return;
  const bar = document.createElement("div");
  bar.className = "episode-toolbar";
  bar.innerHTML = `
    <input id="episode-search"
           type="search"
           placeholder="제목으로 검색..."
           autocomplete="off"
           spellcheck="false" />
    <span id="episode-count" class="muted"></span>
  `;
  container.parentNode.insertBefore(bar, container);
  const input = bar.querySelector("#episode-search");
  input.addEventListener("input", () => {
    _applyFilter(container, input.value);
    _updateCount(input.value);
  });
}

function _updateCount(needle) {
  const el = document.getElementById("episode-count");
  if (!el) return;
  const total = _episodes.length;
  const n = (needle || "").trim().toLowerCase();
  if (!n) {
    el.textContent = `${total}개`;
    return;
  }
  const matched = _episodes.filter((ep) =>
    String(ep.title || "").toLowerCase().includes(n),
  ).length;
  el.textContent = `${matched}/${total}개`;
}

async function main() {
  const container = document.getElementById(LIST_EL_ID);
  if (!container) return;

  _buildToolbar(container);

  try {
    const data = await api.get("/api/episodes");
    _episodes = Array.isArray(data) ? data : [];
    container.dataset.loading = "false";
    _renderList(container, _episodes);
    _updateCount("");
  } catch (err) {
    container.dataset.loading = "false";
    container.innerHTML = `
      <p class="error">에피소드 목록을 불러오지 못했습니다.</p>
    `;
    // api wrapper already toasted; keep a console trace for dev.
    console.error("episodes load failed", err);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
