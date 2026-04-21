/* ABC English — shared frontend utilities (ESM).
 *
 * Exports:
 *   api      fetch wrapper (get/post/patch/del) with JSON + error toast.
 *   toast    right-bottom toast notifications.
 *   fmtDate  ISO date → locale string.
 *   fmtDuration  seconds → "MM:SS" / "HH:MM:SS".
 *   setupDrawer  generic slide-drawer controller (toggle/shortcut/ESC).
 *
 * Side effect: calls initNav() on DOMContentLoaded.
 */

// ---------- toast ------------------------------------------------------

function _toastRoot() {
  let root = document.getElementById("toast-root");
  if (!root) {
    root = document.createElement("div");
    root.id = "toast-root";
    root.className = "toast-root";
    document.body.appendChild(root);
  }
  return root;
}

export function toast(msg, type = "info") {
  const root = _toastRoot();
  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  el.textContent = String(msg);
  root.appendChild(el);
  // next tick to trigger transition
  requestAnimationFrame(() => el.classList.add("show"));
  setTimeout(() => {
    el.classList.remove("show");
    setTimeout(() => el.remove(), 250);
  }, 3000);
  return el;
}

// ---------- api fetch wrapper -----------------------------------------

async function _request(method, url, body) {
  const init = { method, headers: {} };
  if (body !== undefined && body !== null) {
    init.headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(body);
  }
  let resp;
  try {
    resp = await fetch(url, init);
  } catch (err) {
    toast(`네트워크 오류: ${err.message || err}`, "error");
    throw err;
  }
  const ctype = resp.headers.get("content-type") || "";
  let data = null;
  if (ctype.includes("application/json")) {
    try {
      data = await resp.json();
    } catch {
      data = null;
    }
  } else {
    try {
      data = await resp.text();
    } catch {
      data = null;
    }
  }
  if (!resp.ok) {
    const detail =
      (data && typeof data === "object" && (data.detail || data.message)) ||
      (typeof data === "string" && data) ||
      `HTTP ${resp.status}`;
    toast(`요청 실패: ${detail}`, "error");
    const err = new Error(`HTTP ${resp.status}: ${detail}`);
    err.status = resp.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const api = {
  get: (url) => _request("GET", url),
  post: (url, body) => _request("POST", url, body ?? {}),
  patch: (url, body) => _request("PATCH", url, body ?? {}),
  del: (url) => _request("DELETE", url),
};

// ---------- formatting utilities --------------------------------------

export function fmtDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return String(iso);
  return d.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}

export function fmtDuration(seconds) {
  const s = Math.max(0, Math.floor(Number(seconds) || 0));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  const pad = (n) => String(n).padStart(2, "0");
  return h > 0 ? `${h}:${pad(m)}:${pad(sec)}` : `${m}:${pad(sec)}`;
}

// ---------- nav --------------------------------------------------------

export function initNav() {
  const path = window.location.pathname;
  const links = document.querySelectorAll(".nav-link");
  links.forEach((a) => {
    const href = a.getAttribute("href") || "";
    const nav = a.dataset.nav;
    let active = false;
    if (nav === "episodes") {
      active = path === "/" || path.startsWith("/study/");
    } else if (nav === "notebook") {
      active = path.startsWith("/notebook");
    } else {
      active = href && path === href;
    }
    a.classList.toggle("active", !!active);
  });
}

// ---------- drawer controller -----------------------------------------

function _isEditableTarget(el) {
  if (!el) return false;
  const tag = (el.tagName || "").toLowerCase();
  if (tag === "input" || tag === "textarea" || tag === "select") return true;
  if (el.isContentEditable) return true;
  return false;
}

/**
 * Wire up a slide-drawer.
 *
 * @param {Object} opts
 * @param {HTMLElement} opts.drawerEl     The drawer container (position:fixed).
 * @param {HTMLElement} opts.toggleBtnEl  Button that toggles the drawer.
 * @param {HTMLElement} [opts.closeBtnEl] Optional close (×) button inside.
 * @param {HTMLElement} [opts.badgeEl]    Optional badge element to bump.
 * @param {string}      [opts.shortcutKey='n']
 * @returns {{open:Function, close:Function, toggle:Function, isOpen:Function, bumpBadge:Function}}
 */
export function setupDrawer({
  drawerEl,
  toggleBtnEl,
  closeBtnEl,
  badgeEl,
  shortcutKey = "n",
} = {}) {
  if (!drawerEl) {
    throw new Error("setupDrawer: drawerEl is required");
  }

  const setState = (open) => {
    drawerEl.classList.toggle("open", open);
    drawerEl.setAttribute("aria-hidden", open ? "false" : "true");
    if (toggleBtnEl) toggleBtnEl.setAttribute("aria-expanded", open ? "true" : "false");
  };

  const isOpen = () => drawerEl.classList.contains("open");
  const open = () => setState(true);
  const close = () => setState(false);
  const toggle = () => setState(!isOpen());

  if (toggleBtnEl) toggleBtnEl.addEventListener("click", toggle);
  if (closeBtnEl) closeBtnEl.addEventListener("click", close);

  document.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape" && isOpen()) {
      close();
      return;
    }
    if (shortcutKey && ev.key.toLowerCase() === shortcutKey.toLowerCase()) {
      if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
      if (_isEditableTarget(document.activeElement)) return;
      ev.preventDefault();
      toggle();
    }
  });

  const bumpBadge = (count) => {
    if (!badgeEl) return;
    if (typeof count === "number") {
      badgeEl.textContent = String(count);
      badgeEl.hidden = count <= 0;
    }
    badgeEl.classList.remove("bump");
    // force reflow to restart animation
    void badgeEl.offsetWidth;
    badgeEl.classList.add("bump");
  };

  // initial state
  setState(false);

  return { open, close, toggle, isOpen, bumpBadge };
}

// ---------- bootstrap --------------------------------------------------

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initNav);
} else {
  initNav();
}
