/* ABC English — study page.
 *
 * Responsibilities:
 *   - Load episode data + sentences.
 *   - Drive the custom audio player (play/seek/rate/skip/shortcuts).
 *   - Sync subtitle highlight with audio timeupdate (cached index + bsearch).
 *   - Word click / drag-selection -> lookup modal -> notebook add.
 *   - Right slide drawer showing notebook preview (last_added, 30).
 *   - Persist UI toggles + skip seconds in localStorage.
 */

import {
  api,
  fmtDate,
  fmtDuration,
  toast,
  setupDrawer,
} from "/static/js/common.js";

// ------------------------------------------------------------------- state

const LS_KEYS = {
  skip: "skipSeconds",
  showTranscript: "study.showTranscript",
  showHighlight: "study.showHighlight",
  helperType: "study.helperType",
  helperDiff: "study.helperDifficulty",
};

const state = {
  episodeId: document.body.dataset.episodeId || "",
  episode: null,
  sentences: [], // sorted by start_time asc
  currentIdx: -1,
  skipSeconds: 3,
  drawer: null,
  notebookTerms: new Set(),
};

// ------------------------------------------------------------------- utils

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

function lsGet(key, fallback) {
  try {
    const v = localStorage.getItem(key);
    return v === null ? fallback : v;
  } catch {
    return fallback;
  }
}
function lsSet(key, value) {
  try {
    localStorage.setItem(key, String(value));
  } catch {
    /* ignore */
  }
}

function isEditable(el) {
  if (!el) return false;
  const tag = (el.tagName || "").toLowerCase();
  if (tag === "input" || tag === "textarea" || tag === "select") return true;
  return !!el.isContentEditable;
}

// ------------------------------------------------------------------- sentence index search

/**
 * Find the sentence index whose [start_time, end_time] contains `t`.
 * Uses a cached `state.currentIdx`, checks neighbours, then falls back
 * to binary search. Returns -1 when no sentence matches.
 */
function findSegment(t) {
  const s = state.sentences;
  if (!s.length) return -1;

  const idx = state.currentIdx;
  const inRange = (i) => {
    if (i < 0 || i >= s.length) return false;
    const seg = s[i];
    const st = Number(seg.start_time ?? 0);
    const en = Number(seg.end_time ?? st);
    return t >= st && t <= en;
  };

  if (inRange(idx)) return idx;
  if (inRange(idx + 1)) return idx + 1;
  if (inRange(idx - 1)) return idx - 1;

  // Binary search for the greatest start_time <= t.
  let lo = 0;
  let hi = s.length - 1;
  let best = -1;
  while (lo <= hi) {
    const mid = (lo + hi) >> 1;
    const st = Number(s[mid].start_time ?? 0);
    if (st <= t) {
      best = mid;
      lo = mid + 1;
    } else {
      hi = mid - 1;
    }
  }
  if (best === -1) return -1;
  const seg = s[best];
  const en = Number(seg.end_time ?? seg.start_time ?? 0);
  if (t <= en) return best;
  return best; // prefer "current" sentence even if we're between gaps
}

// ------------------------------------------------------------------- transcript render

const WORD_SPLIT_RE = /(\s+)/; // keep whitespace tokens

function tokenizeSentence(text) {
  // Split on whitespace; each non-whitespace token becomes a `.word` span
  // with the surrounding punctuation stripped for lookup purposes.
  const parts = String(text || "").split(WORD_SPLIT_RE);
  return parts
    .map((p) => {
      if (!p) return "";
      if (/^\s+$/.test(p)) return esc(p);
      const cleaned = p.replace(/^[^\p{L}\p{N}'’-]+|[^\p{L}\p{N}'’-]+$/gu, "");
      if (!cleaned) return esc(p);
      return `<span class="word" data-term="${esc(cleaned.toLowerCase())}">${esc(p)}</span>`;
    })
    .join("");
}

function renderTranscript() {
  const container = $("transcript");
  if (!state.sentences.length) {
    container.innerHTML = `<p class="muted">이 에피소드에는 문장 데이터가 없습니다.</p>`;
    return;
  }
  const html = state.sentences
    .map((s, i) => {
      const start = Number(s.start_time ?? 0);
      const sidx = Number.isFinite(Number(s.sentence_index))
        ? Number(s.sentence_index)
        : i;
      return `
        <p class="sentence" data-idx="${i}" data-sentence-index="${sidx}" data-start="${start}">
          <button type="button" class="sentence-time" data-start="${start}" title="이 지점으로 이동">${fmtDuration(start)}</button>
          <span class="sentence-text">${tokenizeSentence(s.official_text || "")}</span>
        </p>
      `;
    })
    .join("");
  container.innerHTML = html;
}

// ------------------------------------------------------------------- hash jump

function handleHashJump() {
  const raw = (location.hash || "").replace(/^#/, "");
  if (!raw) return;
  const hashParams = new URLSearchParams(raw);
  const s = hashParams.get("s");
  if (s === null || s === "") return;
  const sel = `[data-sentence-index="${CSS.escape(String(s))}"]`;
  const target = document.querySelector(sel);
  if (!target) return;
  try {
    target.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch {
    /* older browsers */
  }
  target.classList.add("hash-flash");
  setTimeout(() => {
    target.classList.remove("hash-flash");
  }, 1600);
}

// ------------------------------------------------------------------- highlight

function applyHighlight(idx) {
  const container = $("transcript");
  const showHighlight = $("toggle-highlight").checked;

  if (!showHighlight) {
    container
      .querySelectorAll(".sentence.active")
      .forEach((el) => el.classList.remove("active"));
    return;
  }

  const prev = container.querySelector(".sentence.active");
  if (prev && Number(prev.dataset.idx) === idx) return;
  if (prev) prev.classList.remove("active");
  if (idx >= 0) {
    const next = container.querySelector(`.sentence[data-idx="${idx}"]`);
    if (next) {
      next.classList.add("active");
      // scroll the transcript container only (not the whole window)
      try {
        next.scrollIntoView({ behavior: "smooth", block: "center" });
      } catch {
        /* older browsers */
      }
    }
  }
}

// ------------------------------------------------------------------- player

function initPlayer() {
  const audio = $("audio");
  const btnPlay = $("btn-play");
  const btnBack = $("btn-back");
  const btnFwd = $("btn-fwd");
  const seek = $("seek");
  const timeCur = $("time-cur");
  const timeDur = $("time-dur");
  const rate = $("rate");
  const skipInput = $("skip-seconds");

  // Skip seconds persistence
  const storedSkip = parseInt(lsGet(LS_KEYS.skip, "3"), 10);
  state.skipSeconds = Number.isFinite(storedSkip) && storedSkip >= 1 && storedSkip <= 30
    ? storedSkip
    : 3;
  skipInput.value = String(state.skipSeconds);
  updateSkipLabels();

  skipInput.addEventListener("change", () => {
    let n = parseInt(skipInput.value, 10);
    if (!Number.isFinite(n)) n = 3;
    n = Math.max(1, Math.min(30, n));
    state.skipSeconds = n;
    skipInput.value = String(n);
    lsSet(LS_KEYS.skip, n);
    updateSkipLabels();
  });

  btnPlay.addEventListener("click", () => togglePlay());
  btnBack.addEventListener("click", () => skip(-state.skipSeconds));
  btnFwd.addEventListener("click", () => skip(+state.skipSeconds));

  rate.addEventListener("change", () => {
    const r = parseFloat(rate.value) || 1;
    audio.playbackRate = r;
  });

  seek.addEventListener("input", () => {
    const v = parseFloat(seek.value);
    if (Number.isFinite(v) && Number.isFinite(audio.duration)) {
      audio.currentTime = v;
    }
  });

  audio.addEventListener("loadedmetadata", () => {
    seek.max = String(audio.duration || 0);
    timeDur.textContent = fmtDuration(audio.duration || 0);
  });
  audio.addEventListener("play", () => {
    btnPlay.textContent = "❚❚";
  });
  audio.addEventListener("pause", () => {
    btnPlay.textContent = "▶";
  });
  audio.addEventListener("ended", () => {
    btnPlay.textContent = "▶";
  });
  audio.addEventListener("timeupdate", onTimeUpdate);

  // Transcript: click on .sentence-time seeks audio to that sentence start.
  const transcript = $("transcript");
  transcript.addEventListener("click", (ev) => {
    const btn = ev.target.closest(".sentence-time");
    if (!btn) return;
    ev.preventDefault();
    ev.stopPropagation();
    const t = parseFloat(btn.dataset.start || "");
    if (!Number.isFinite(t)) return;
    audio.currentTime = t;
    if (audio.paused) audio.play().catch(() => {});
  });

  // Keyboard shortcuts
  document.addEventListener("keydown", onKeydown);
}

function updateSkipLabels() {
  $("btn-back-label").textContent = `-${state.skipSeconds}s`;
  $("btn-fwd-label").textContent = `+${state.skipSeconds}s`;
}

function togglePlay() {
  const audio = $("audio");
  if (!audio) return;
  if (audio.paused) audio.play().catch((e) => toast(`재생 실패: ${e.message || e}`, "error"));
  else audio.pause();
}

function skip(delta) {
  const audio = $("audio");
  if (!audio) return;
  const dur = Number.isFinite(audio.duration) ? audio.duration : 0;
  audio.currentTime = Math.max(0, Math.min(dur || audio.currentTime + delta, audio.currentTime + delta));
}

function stepRate(dir) {
  const rate = $("rate");
  const opts = Array.from(rate.options).map((o) => parseFloat(o.value));
  const current = parseFloat(rate.value) || 1;
  let i = opts.indexOf(current);
  if (i === -1) i = opts.indexOf(1);
  i = Math.max(0, Math.min(opts.length - 1, i + dir));
  rate.value = String(opts[i]);
  const audio = $("audio");
  audio.playbackRate = opts[i];
}

function onTimeUpdate() {
  const audio = $("audio");
  if (!audio) return;
  const t = audio.currentTime || 0;
  $("seek").value = String(t);
  $("time-cur").textContent = fmtDuration(t);

  const idx = findSegment(t);
  if (idx !== state.currentIdx) {
    state.currentIdx = idx;
    applyHighlight(idx);
  }
}

function onKeydown(ev) {
  if (isEditable(document.activeElement)) return;
  if (ev.ctrlKey || ev.metaKey || ev.altKey) return;

  switch (ev.key) {
    case " ":
    case "Spacebar":
      ev.preventDefault();
      togglePlay();
      break;
    case "ArrowLeft":
      ev.preventDefault();
      skip(-state.skipSeconds);
      break;
    case "ArrowRight":
      ev.preventDefault();
      skip(+state.skipSeconds);
      break;
    case "ArrowUp":
      ev.preventDefault();
      stepRate(+1);
      break;
    case "ArrowDown":
      ev.preventDefault();
      stepRate(-1);
      break;
    default:
      break;
  }
}

// ------------------------------------------------------------------- toggles

function initToggles() {
  const tTranscript = $("toggle-transcript");
  const tHighlight = $("toggle-highlight");

  tTranscript.checked = lsGet(LS_KEYS.showTranscript, "1") !== "0";
  tHighlight.checked = lsGet(LS_KEYS.showHighlight, "1") !== "0";

  applyToggleVisibility();

  tTranscript.addEventListener("change", () => {
    lsSet(LS_KEYS.showTranscript, tTranscript.checked ? "1" : "0");
    applyToggleVisibility();
  });
  tHighlight.addEventListener("change", () => {
    lsSet(LS_KEYS.showHighlight, tHighlight.checked ? "1" : "0");
    applyHighlight(state.currentIdx);
  });
}

function applyToggleVisibility() {
  $("transcript").hidden = !$("toggle-transcript").checked;
}

// ------------------------------------------------------------------- lookup modal

let _modalEl = null;

function openLookupModal(term, context) {
  closeLookupModal();
  const root = $("lookup-root");
  const backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop";
  backdrop.innerHTML = `
    <div class="modal lookup-modal" role="dialog" aria-modal="true">
      <header class="lookup-modal-header">
        <h3 class="lookup-term">${esc(term)}</h3>
        <span class="lookup-type badge badge-muted">loading…</span>
        <button class="btn btn-icon lookup-close" type="button" aria-label="닫기">×</button>
      </header>
      <div class="lookup-body">
        <div class="lookup-loading">
          <span class="spinner" aria-hidden="true"></span>
          <span>Ollama 질의 중…</span>
        </div>
      </div>
      <footer class="lookup-footer">
        <button class="btn lookup-close" type="button">닫기</button>
        <button class="btn btn-primary lookup-add" type="button" disabled>📒 단어장에 추가</button>
      </footer>
    </div>
  `;
  root.appendChild(backdrop);
  _modalEl = backdrop;

  backdrop.addEventListener("click", (e) => {
    if (e.target === backdrop) closeLookupModal();
  });
  backdrop.querySelectorAll(".lookup-close").forEach((b) =>
    b.addEventListener("click", closeLookupModal),
  );

  const onEsc = (ev) => {
    if (ev.key === "Escape") {
      closeLookupModal();
      document.removeEventListener("keydown", onEsc);
    }
  };
  document.addEventListener("keydown", onEsc);

  // Fetch lookup
  api
    .post("/api/lookup", { term, context: context || null })
    .then((data) => {
      if (!_modalEl) return;
      const typeEl = _modalEl.querySelector(".lookup-type");
      const bodyEl = _modalEl.querySelector(".lookup-body");
      const addBtn = _modalEl.querySelector(".lookup-add");

      const termType = data.term_type || "word";
      typeEl.textContent = termType;
      typeEl.classList.remove("badge-muted");
      typeEl.classList.add(`badge-${termType}`);

      const examples = Array.isArray(data.examples) ? data.examples : [];
      bodyEl.innerHTML = `
        <p class="lookup-explanation">${esc(data.explanation_en || "")}</p>
        ${
          data.etymology
            ? `<div class="lookup-section"><h4>Etymology</h4><p>${esc(data.etymology)}</p></div>`
            : ""
        }
        ${
          examples.length
            ? `<div class="lookup-section"><h4>Examples</h4><ul>${examples
                .map((ex) => `<li>${esc(typeof ex === "string" ? ex : ex.text || "")}</li>`)
                .join("")}</ul></div>`
            : ""
        }
      `;
      addBtn.disabled = false;
      addBtn.addEventListener("click", async () => {
        addBtn.disabled = true;
        try {
          const payload = {
            term,
            context: context || null,
            source_episode_id: state.episodeId || null,
            sentence_index:
              state.currentIdx >= 0 ? state.currentIdx : null,
          };
          const entry = await api.post("/api/notebook", payload);
          toast("단어장에 추가됨", "success");
          state.notebookTerms.add(String(entry.term || term).toLowerCase());
          onNotebookAdded(entry);
          closeLookupModal();
        } catch (err) {
          addBtn.disabled = false;
        }
      });
    })
    .catch(() => {
      if (!_modalEl) return;
      const bodyEl = _modalEl.querySelector(".lookup-body");
      bodyEl.innerHTML = `<p class="error">조회에 실패했습니다.</p>`;
    });
}

function closeLookupModal() {
  if (_modalEl && _modalEl.parentNode) {
    _modalEl.parentNode.removeChild(_modalEl);
  }
  _modalEl = null;
}

// ------------------------------------------------------------------- selection & click

function initWordInteractions() {
  const container = $("transcript");

  container.addEventListener("click", (ev) => {
    const w = ev.target.closest(".word");
    if (!w) return;
    const term = w.dataset.term || w.textContent.trim();
    if (!term) return;
    const sentEl = w.closest(".sentence");
    const context = sentEl ? sentEl.querySelector(".sentence-text")?.textContent.trim() : "";
    openLookupModal(term, context);
  });

  const handleSelection = () => {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed) return;
    const text = (sel.toString() || "").trim();
    if (!text) return;
    // must be within the transcript container
    const anchor = sel.anchorNode;
    if (!anchor || !container.contains(anchor.nodeType === 1 ? anchor : anchor.parentNode)) {
      return;
    }
    const words = text.split(/\s+/).filter(Boolean);
    if (words.length < 1 || words.length > 6) return;
    showSelectionLookupBubble(sel, text);
  };

  container.addEventListener("mouseup", handleSelection);
  container.addEventListener("touchend", handleSelection);
}

let _bubbleEl = null;
function showSelectionLookupBubble(selection, text) {
  hideSelectionLookupBubble();
  let rect;
  try {
    rect = selection.getRangeAt(0).getBoundingClientRect();
  } catch {
    return;
  }
  if (!rect || (rect.width === 0 && rect.height === 0)) return;

  const el = document.createElement("button");
  el.type = "button";
  el.className = "lookup-bubble";
  el.textContent = "🔍 lookup";
  el.style.position = "fixed";
  el.style.left = `${Math.max(8, rect.left + rect.width / 2 - 40)}px`;
  el.style.top = `${Math.max(8, rect.top - 36)}px`;
  el.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const sentEl =
      selection.anchorNode && selection.anchorNode.parentNode
        ? selection.anchorNode.parentNode.closest(".sentence")
        : null;
    const context = sentEl ? sentEl.querySelector(".sentence-text")?.textContent.trim() : "";
    hideSelectionLookupBubble();
    openLookupModal(text, context);
  });
  document.body.appendChild(el);
  _bubbleEl = el;

  const dismiss = () => {
    hideSelectionLookupBubble();
    document.removeEventListener("mousedown", onDown, true);
  };
  const onDown = (ev) => {
    if (ev.target === el) return;
    dismiss();
  };
  // attach on next tick so the current mouseup doesn't immediately dismiss
  setTimeout(() => {
    document.addEventListener("mousedown", onDown, true);
  }, 0);
  // auto-dismiss after 5s
  setTimeout(dismiss, 5000);
}
function hideSelectionLookupBubble() {
  if (_bubbleEl && _bubbleEl.parentNode) {
    _bubbleEl.parentNode.removeChild(_bubbleEl);
  }
  _bubbleEl = null;
}

// ------------------------------------------------------------------- drawer / notebook

function initDrawer() {
  const drawerEl = $("drawer");
  const toggleBtn = $("drawer-toggle");
  const closeBtn = $("drawer-close");
  const badgeEl = $("drawer-badge");
  state.drawer = setupDrawer({
    drawerEl,
    toggleBtnEl: toggleBtn,
    closeBtnEl: closeBtn,
    badgeEl,
    shortcutKey: "n",
  });

  const search = $("drawer-search");
  search.addEventListener("input", () => renderDrawerList(search.value));
}

function truncate(s, n = 140) {
  s = String(s || "");
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

let _drawerEntries = [];
function renderDrawerList(needle) {
  const body = $("drawer-body");
  const count = $("drawer-count");
  const n = (needle || "").trim().toLowerCase();
  const items = n
    ? _drawerEntries.filter(
        (e) =>
          (e.term || "").toLowerCase().includes(n) ||
          (e.explanation_en || "").toLowerCase().includes(n),
      )
    : _drawerEntries;

  count.textContent = n
    ? `${items.length}/${_drawerEntries.length}`
    : `${_drawerEntries.length}개`;

  if (!items.length) {
    body.innerHTML = `<p class="muted">단어장이 비어 있습니다.</p>`;
    return;
  }

  body.innerHTML = items
    .map(
      (e) => `
      <details class="nb-entry" data-term="${esc(e.term)}">
        <summary>
          <span class="nb-term">${esc(e.term)}</span>
          <span class="badge badge-${esc(e.term_type || "word")}">${esc(e.term_type || "word")}</span>
          <span class="nb-count muted">×${Number(e.added_count || 1)}</span>
        </summary>
        <p class="nb-exp">${esc(truncate(e.explanation_en))}</p>
        ${
          e.etymology
            ? `<p class="nb-etym muted">🏛 ${esc(truncate(e.etymology))}</p>`
            : ""
        }
      </details>`,
    )
    .join("");
}

async function loadNotebookPreview() {
  try {
    const data = await api.get("/api/notebook?sort=last_added");
    _drawerEntries = Array.isArray(data) ? data.slice(0, 30) : [];
    state.notebookTerms = new Set(
      _drawerEntries.map((e) => String(e.term || "").toLowerCase()),
    );
    renderDrawerList("");
    if (state.drawer) state.drawer.bumpBadge(_drawerEntries.length);
  } catch (err) {
    /* api wrapper toasted already */
  }
}

function onNotebookAdded(entry) {
  // Prepend (replace if already present)
  const key = String(entry.term || "").toLowerCase();
  _drawerEntries = _drawerEntries.filter(
    (e) => String(e.term || "").toLowerCase() !== key,
  );
  _drawerEntries.unshift(entry);
  if (_drawerEntries.length > 30) _drawerEntries.length = 30;

  if (state.drawer) {
    if (state.drawer.isOpen()) {
      renderDrawerList($("drawer-search").value);
    } else {
      state.drawer.bumpBadge(_drawerEntries.length);
    }
  }
}

// ------------------------------------------------------------------- bootstrap

async function loadEpisode() {
  if (!state.episodeId) {
    toast("episode_id 누락", "error");
    return;
  }
  try {
    const data = await api.get(`/api/episodes/${encodeURIComponent(state.episodeId)}`);
    state.episode = data.episode || {};
    const sents = Array.isArray(data.sentences) ? data.sentences.slice() : [];
    sents.sort(
      (a, b) => Number(a.start_time ?? 0) - Number(b.start_time ?? 0),
    );
    state.sentences = sents;

    $("study-title").textContent =
      state.episode.title || state.episodeId;
    $("study-date").textContent = fmtDate(state.episode.published_date);
    $("study-dur").textContent = state.episode.duration_seconds
      ? fmtDuration(state.episode.duration_seconds)
      : "";

    renderTranscript();
    handleHashJump();
  } catch (err) {
    $("transcript").innerHTML = `<p class="error">에피소드를 불러오지 못했습니다.</p>`;
  }
}

// ------------------------------------------------------------------- helper panel

const helperState = {
  cards: [],
  loading: false,
  loadedKey: "",
};

function helperKey() {
  const t = $("helper-type")?.value || "all";
  const d = $("helper-difficulty")?.value || "all";
  return `${t}|${d}|${state.episodeId || ""}`;
}

function renderHelperCardItem(c, idx) {
  const examples = Array.isArray(c.examples) ? c.examples.slice(0, 3) : [];
  const examplesHtml = examples.length
    ? `<div class="helper-examples"><h4>예문</h4><ul>${examples
        .map((ex) => {
          if (typeof ex === "string") return `<li>${esc(ex)}</li>`;
          const txt = esc(ex.text || ex.sentence || "");
          const ko = ex.translation_ko ? ` <span class="muted">— ${esc(ex.translation_ko)}</span>` : "";
          return `<li>${txt}${ko}</li>`;
        })
        .join("")}</ul></div>`
    : "";

  const ety = c.etymology
    ? `<details class="helper-etymology"><summary>어원/유래</summary><p>${esc(c.etymology)}</p></details>`
    : "";

  const kindLabel = c.kind === "expression" ? (c.type || "표현") : (c.type || "단어");
  const diffLabel = c.difficulty || "—";
  const term = c.term || "";
  const inNotebook = term && state.notebookTerms.has(String(term).toLowerCase());

  return `
    <article class="helper-card" data-idx="${idx}" data-term="${esc(term)}">
      <div class="helper-card-head">
        <h3 class="helper-term">${esc(term)}</h3>
        <div class="helper-meta">
          <span class="badge">${esc(kindLabel)}</span>
          <span class="badge badge-diff">${esc(diffLabel)}</span>
        </div>
      </div>
      <div class="helper-defs">
        ${c.definition_ko ? `<p class="helper-def-ko">${esc(c.definition_ko)}</p>` : ""}
        ${c.definition_en ? `<p class="helper-def-en muted">${esc(c.definition_en)}</p>` : ""}
      </div>
      ${ety}
      ${examplesHtml}
      <div class="helper-actions">
        <button class="btn btn-primary helper-add" type="button" ${inNotebook ? "disabled" : ""}>
          ${inNotebook ? "이미 단어장에 있음" : "단어장에 담기"}
        </button>
      </div>
    </article>
  `;
}

function renderHelperList() {
  const list = $("helper-list");
  const count = $("helper-count");
  if (!list) return;

  if (helperState.loading) {
    list.innerHTML = `<p class="muted">로딩 중…</p>`;
    if (count) count.textContent = "…";
    return;
  }
  const cards = helperState.cards;
  if (count) count.textContent = `${cards.length}개`;
  if (cards.length === 0) {
    list.innerHTML = `<p class="muted">이 에피소드에 표시할 카드가 없습니다.</p>`;
    return;
  }
  list.innerHTML = cards.map((c, i) => renderHelperCardItem(c, i)).join("");
}

async function loadHelperCards(force = false) {
  const key = helperKey();
  if (!force && key === helperState.loadedKey && helperState.cards.length) {
    renderHelperList();
    return;
  }
  helperState.loading = true;
  renderHelperList();
  try {
    const [type, diff, ep] = key.split("|");
    const params = new URLSearchParams({ type, difficulty: diff, limit: "500" });
    if (ep) params.set("episode_id", ep);
    const cards = await api.get(`/api/study/helper?${params.toString()}`);
    helperState.cards = Array.isArray(cards) ? cards : [];
    helperState.loadedKey = key;
  } catch {
    helperState.cards = [];
  } finally {
    helperState.loading = false;
    renderHelperList();
  }
}

function setHelperOpen(open) {
  const panel = $("study-helper");
  const btn = $("toggle-helper");
  if (!panel) return;
  panel.hidden = !open;
  if (btn) btn.setAttribute("aria-expanded", open ? "true" : "false");
  if (open && helperState.cards.length === 0 && !helperState.loading) {
    loadHelperCards();
  }
}

function initHelper() {
  const toggle = $("toggle-helper");
  const close = $("helper-close");
  const typeSel = $("helper-type");
  const diffSel = $("helper-difficulty");
  const list = $("helper-list");
  if (!toggle || !$("study-helper")) return;

  const savedType = lsGet(LS_KEYS.helperType, "all");
  const savedDiff = lsGet(LS_KEYS.helperDiff, "all");
  if (typeSel) typeSel.value = savedType;
  if (diffSel) diffSel.value = savedDiff;

  toggle.addEventListener("click", () => {
    const open = $("study-helper").hidden;
    setHelperOpen(open);
  });
  close?.addEventListener("click", () => setHelperOpen(false));
  typeSel?.addEventListener("change", () => {
    lsSet(LS_KEYS.helperType, typeSel.value);
    loadHelperCards(true);
  });
  diffSel?.addEventListener("change", () => {
    lsSet(LS_KEYS.helperDiff, diffSel.value);
    loadHelperCards(true);
  });

  list?.addEventListener("click", async (ev) => {
    const btn = ev.target.closest(".helper-add");
    if (!btn) return;
    const card = btn.closest(".helper-card");
    const idx = parseInt(card?.dataset.idx || "", 10);
    const c = helperState.cards[idx];
    if (!c) return;
    btn.disabled = true;
    try {
      const entry = await api.post("/api/notebook", {
        term: c.term,
        context: c.definition_en || c.definition_ko || null,
        source_episode_id: state.episodeId || null,
        sentence_index: null,
      });
      toast("단어장에 추가됨", "success");
      state.notebookTerms.add(String(entry.term || c.term).toLowerCase());
      btn.textContent = "단어장에 추가됨";
    } catch {
      btn.disabled = false;
    }
  });
}

async function main() {
  initPlayer();
  initToggles();
  initWordInteractions();
  initDrawer();
  initHelper();
  await Promise.allSettled([loadEpisode(), loadNotebookPreview()]);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", main);
} else {
  main();
}
