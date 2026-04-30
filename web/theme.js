// Claude Coach — 테마 토글. index.html / guide.html 양쪽에서 공유.
(() => {
  'use strict';
  const STORAGE_KEY = 'coach-theme';
  const root = document.documentElement;

  function detect() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === 'light' || stored === 'dark') return stored;
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) return 'light';
    return 'dark';
  }

  function currentTheme() {
    return root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
  }

  function apply(theme, persist = true) {
    root.setAttribute('data-theme', theme);
    if (persist) localStorage.setItem(STORAGE_KEY, theme);
    updateButton(theme);
    document.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
  }

  function updateButton(theme) {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    if (theme === 'light') {
      btn.textContent = '다크 모드';
      btn.setAttribute('aria-label', '다크 모드로 전환');
    } else {
      btn.textContent = '라이트 모드';
      btn.setAttribute('aria-label', '라이트 모드로 전환');
    }
  }

  function setupToggle() {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    updateButton(currentTheme());
    btn.addEventListener('click', () => {
      apply(currentTheme() === 'light' ? 'dark' : 'light');
    });
  }

  // 초기 테마는 head 의 인라인 스크립트가 이미 set 했지만, 안전하게 한 번 더.
  const initial = currentTheme() || detect();
  if (root.getAttribute('data-theme') !== initial) {
    apply(initial, false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupToggle);
  } else {
    setupToggle();
  }
})();
