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

/* ── Phase A: Exam tab toggle (selector-isolated from `.tab-btn`) ─── */
document.addEventListener("DOMContentLoaded", function () {
  // 기존 `.tab-btn` 핸들러 (initTabs) 와 selector 격리: `.exam-tab-bar
  // .exam-tab-btn` 만 매칭. study/coverage 토글 + TOC visibility 동기.
  const examTabBars = document.querySelectorAll(".exam-tab-bar");
  if (!examTabBars.length) return;

  examTabBars.forEach(function (bar) {
    const btns = bar.querySelectorAll(".exam-tab-btn");
    // 같은 .exam-main 내부의 컨텐츠와 페이지 내 .exam-toc.
    const main = bar.closest(".exam-main") || document;
    const contents = main.querySelectorAll(".exam-tab-content");
    const tocPanels = document.querySelectorAll(".exam-toc");

    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        const target = btn.dataset.tab;

        btns.forEach(function (b) { b.classList.remove("exam-tab-active"); });
        btn.classList.add("exam-tab-active");

        contents.forEach(function (c) {
          if (c.dataset.tab === target) {
            c.removeAttribute("hidden");
            c.dataset.active = "true";
          } else {
            c.setAttribute("hidden", "");
            delete c.dataset.active;
          }
        });

        // TOC 는 study-guide 활성 시만 표시 (coverage 시 hide).
        tocPanels.forEach(function (toc) {
          if (toc.dataset.tab === target) {
            toc.classList.remove("exam-toc-hidden");
          } else {
            toc.classList.add("exam-toc-hidden");
          }
        });
      });
    });
  });
});
