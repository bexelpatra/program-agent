/**
 * Ethics Study Guide — app.js
 * Tab switching and search bar behaviour.
 */

document.addEventListener("DOMContentLoaded", function () {
  initTabs();
  initSearchEnter();
});

/* ── Tab Switching ──────────────────────────── */
function initTabs() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  const cards = document.querySelectorAll(".thinker-card");
  const noResult = document.getElementById("no-result");

  if (!tabBtns.length) return;

  tabBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      // Update active state
      tabBtns.forEach(function (b) {
        b.classList.remove("active");
      });
      btn.classList.add("active");

      const selectedField = btn.dataset.field;
      let visibleCount = 0;

      cards.forEach(function (card) {
        const cardField = card.dataset.field;
        const show = selectedField === "all" || cardField === selectedField;
        card.style.display = show ? "" : "none";
        if (show) visibleCount++;
      });

      if (noResult) {
        noResult.classList.toggle("hidden", visibleCount > 0);
      }
    });
  });
}

/* ── Search Bar ─────────────────────────────── */
function initSearchEnter() {
  const searchInput = document.querySelector(".search-input");
  if (!searchInput) return;

  searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      const q = searchInput.value.trim();
      if (q) {
        window.location.href = "/search?q=" + encodeURIComponent(q);
      }
    }
  });
}
