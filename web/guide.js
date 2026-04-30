// Claude Coach — 사용 가이드 (vanilla JS, 단일 fetch)
(() => {
  'use strict';

  // ---------- constants ----------
  const AXES = ['clarity', 'efficiency', 'economy', 'planning', 'health'];
  const AXIS_LABELS = {
    clarity: '명료성',
    efficiency: '효율성',
    economy: '경제성',
    planning: '계획성',
    health: '건강도',
  };
  const SESSION_TYPE_LABELS_FALLBACK = {
    one_shot: '원샷',
    mixed: '혼합',
    implementation: '구현',
    exploration: '탐색',
    debugging: '디버깅',
    review: '리뷰',
  };
  const COLORS = {
    bg: '#0e1116',
    card: '#161b22',
    border: '#2a313c',
    text: '#e6edf3',
    muted: '#9da7b3',
    accent: '#7aa2f7',
    good: '#56d364',
    warn: '#e3b341',
    bad: '#f0883e',
  };
  const TYPE_PALETTE = [
    '#7aa2f7', '#56d364', '#e3b341', '#f0883e',
    '#bc8cff', '#79c0ff', '#ff7b72', '#a5d6ff',
  ];

  if (window.Chart) {
    Chart.defaults.color = COLORS.muted;
    Chart.defaults.borderColor = COLORS.border;
    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Pretendard', 'Noto Sans KR', sans-serif";
  }

  const state = {
    data: null,
    typeChart: null,
  };

  // ---------- helpers ----------
  const $ = (sel) => document.querySelector(sel);

  function el(tag, attrs, ...children) {
    const node = document.createElement(tag);
    if (attrs) {
      Object.entries(attrs).forEach(([k, v]) => {
        if (v == null || v === false) return;
        if (k === 'class') node.className = v;
        else if (k === 'text') node.textContent = v;
        else if (k === 'html') node.innerHTML = v; // only for trusted strings
        else if (k === 'dataset') Object.assign(node.dataset, v);
        else if (k.startsWith('on') && typeof v === 'function') {
          node.addEventListener(k.slice(2).toLowerCase(), v);
        } else if (v === true) node.setAttribute(k, '');
        else node.setAttribute(k, v);
      });
    }
    children.flat().forEach((c) => {
      if (c == null || c === false) return;
      if (typeof c === 'string') node.appendChild(document.createTextNode(c));
      else node.appendChild(c);
    });
    return node;
  }

  function showError(msg) {
    const banner = $('#error-banner');
    banner.textContent = msg;
    banner.classList.remove('hidden');
  }

  function hideError() {
    $('#error-banner').classList.add('hidden');
  }

  function fmtTimestamp(iso) {
    if (!iso) return '–';
    const d = new Date(iso);
    if (isNaN(d.getTime())) return '–';
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    const hh = String(d.getHours()).padStart(2, '0');
    const mi = String(d.getMinutes()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
  }

  function tailCwd(cwd) {
    if (!cwd) return '–';
    const parts = cwd.split('/').filter(Boolean);
    if (parts.length <= 2) return cwd;
    return '…/' + parts.slice(-2).join('/');
  }

  function axisChipClass(score) {
    if (score == null || isNaN(score)) return '';
    if (score >= 15) return 'good';
    if (score >= 10) return 'warn';
    return 'bad';
  }

  function fmtScore(v, digits = 1) {
    if (v == null || isNaN(v)) return '–';
    return Number(v).toFixed(digits);
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // ---------- data fetch ----------
  async function fetchGuide() {
    const res = await fetch('/api/guide', { headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error(`/api/guide HTTP ${res.status}`);
    return res.json();
  }

  async function postCoach(sessionId) {
    const res = await fetch(`/api/coach/${encodeURIComponent(sessionId)}`, {
      method: 'POST',
      headers: { Accept: 'application/json' },
    });
    let body = null;
    try { body = await res.json(); } catch (_) { /* ignore */ }
    if (!res.ok) {
      const msg = body && (body.error || body.detail) ? `${body.error || ''}${body.detail ? ' — ' + body.detail : ''}` : `HTTP ${res.status}`;
      throw new Error(msg);
    }
    return body || {};
  }

  // ---------- markdown (very small, safe) ----------
  // 지원: ## H2, ### H3, - bullet, **bold**, ```code``` 블록, `inline code`
  function renderMarkdown(src) {
    const lines = String(src || '').replace(/\r\n/g, '\n').split('\n');
    let out = '';
    let inCode = false;
    let codeBuf = [];
    let listOpen = false;
    let paraBuf = [];

    function flushPara() {
      if (paraBuf.length) {
        const text = paraBuf.join(' ').trim();
        if (text) out += `<p>${inlineMd(text)}</p>`;
        paraBuf = [];
      }
    }
    function closeList() {
      if (listOpen) { out += '</ul>'; listOpen = false; }
    }

    for (const raw of lines) {
      const line = raw;
      // code fence
      const fence = line.match(/^```(.*)$/);
      if (fence) {
        if (!inCode) {
          flushPara();
          closeList();
          inCode = true;
          codeBuf = [];
        } else {
          out += `<pre><code>${escapeHtml(codeBuf.join('\n'))}</code></pre>`;
          inCode = false;
        }
        continue;
      }
      if (inCode) { codeBuf.push(line); continue; }

      const trimmed = line.trim();
      if (trimmed === '') {
        flushPara();
        closeList();
        continue;
      }
      const h2 = trimmed.match(/^##\s+(.*)$/);
      const h3 = trimmed.match(/^###\s+(.*)$/);
      const bullet = trimmed.match(/^[-*]\s+(.*)$/);

      if (h3) {
        flushPara(); closeList();
        out += `<h3>${inlineMd(h3[1])}</h3>`;
        continue;
      }
      if (h2) {
        flushPara(); closeList();
        out += `<h2>${inlineMd(h2[1])}</h2>`;
        continue;
      }
      if (bullet) {
        flushPara();
        if (!listOpen) { out += '<ul>'; listOpen = true; }
        out += `<li>${inlineMd(bullet[1])}</li>`;
        continue;
      }
      paraBuf.push(trimmed);
    }
    if (inCode) { out += `<pre><code>${escapeHtml(codeBuf.join('\n'))}</code></pre>`; }
    flushPara(); closeList();
    return out;
  }

  function inlineMd(text) {
    // escape first, then re-introduce supported markup
    let s = escapeHtml(text);
    // code spans `...`
    s = s.replace(/`([^`]+)`/g, (_, m) => `<code>${m}</code>`);
    // bold **...**
    s = s.replace(/\*\*([^*]+)\*\*/g, (_, m) => `<strong>${m}</strong>`);
    return s;
  }

  // ---------- rendering ----------
  function renderDiagnosis(root, data) {
    const diag = data.diagnosis || {};
    const stats = data.stats || {};
    const typeDist = data.type_distribution || {};
    const sessionTypes = (data.principles && data.principles.session_types) || {};

    const card = el('section', { class: 'card diagnosis-card' });
    card.appendChild(el('h2', null,
      '종합 진단',
      el('span', {
        class: 'help', tabindex: '0', 'aria-label': '도움말',
        'data-tip': '최근 분석된 세션의 5축 평균 점수와, 가장 약한 축을 강조해 보여줍니다. 약한 축 위주로 아래 원칙을 읽어보세요.',
      }, ' ? '),
    ));
    card.appendChild(el('p', { class: 'card-hint' },
      `분석된 세션 ${stats.total ?? '–'}개 · 평균 ${stats.avg_score != null ? Number(stats.avg_score).toFixed(1) : '–'} · worst spot 보유 ${stats.with_worst_spots ?? '–'}개`,
    ));

    if (diag.summary) {
      card.appendChild(el('p', { class: 'diagnosis-summary' }, String(diag.summary)));
    }

    const grid = el('div', { class: 'diagnosis-grid' });

    // axes chips
    const axesAvg = diag.axes_avg || {};
    const weakest = new Set(diag.weakest_axes || []);
    const chips = el('div', { class: 'diagnosis-axes' });
    AXES.forEach((aid) => {
      const v = axesAvg[aid];
      const cls = `axis-chip ${axisChipClass(v)} ${weakest.has(aid) ? 'weak' : ''}`.trim();
      const chip = el('span', { class: cls, title: weakest.has(aid) ? '약한 축' : '' },
        el('span', { class: 'axis-chip-label' }, AXIS_LABELS[aid] || aid),
        el('span', { class: 'axis-chip-score mono' }, fmtScore(v, 1)),
      );
      chips.appendChild(chip);
    });
    grid.appendChild(chips);

    // session type distribution chart
    const chartBox = el('div', { class: 'diagnosis-chart-wrap' },
      el('h4', null, '세션 유형 분포'),
    );
    const canvasWrap = el('div', { class: 'diagnosis-chart-canvas-wrap' });
    const canvas = el('canvas', { id: 'type-dist-chart' });
    canvasWrap.appendChild(canvas);
    chartBox.appendChild(canvasWrap);
    grid.appendChild(chartBox);

    card.appendChild(grid);
    root.appendChild(card);

    // build chart now (canvas is in DOM)
    buildTypeChart(canvas, typeDist, sessionTypes);
  }

  function buildTypeChart(canvas, typeDist, sessionTypes) {
    const entries = Object.entries(typeDist || {})
      .filter(([, v]) => typeof v === 'number' && v > 0)
      .sort((a, b) => b[1] - a[1]);

    if (state.typeChart) { state.typeChart.destroy(); state.typeChart = null; }

    if (!entries.length) {
      const ctx = canvas.getContext('2d');
      state.typeChart = new Chart(ctx, {
        type: 'doughnut',
        data: { labels: ['데이터 없음'], datasets: [{ data: [1], backgroundColor: [COLORS.border] }] },
        options: { plugins: { legend: { display: false } }, responsive: true, maintainAspectRatio: false },
      });
      return;
    }

    const labels = entries.map(([k]) =>
      (sessionTypes[k] && sessionTypes[k].label) || SESSION_TYPE_LABELS_FALLBACK[k] || k
    );
    const values = entries.map(([, v]) => v);

    state.typeChart = new Chart(canvas.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: entries.map((_, i) => TYPE_PALETTE[i % TYPE_PALETTE.length]),
          borderColor: COLORS.card,
          borderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { color: COLORS.text, boxWidth: 10, font: { size: 11 } } },
        },
      },
    });
  }

  function renderAxisSection(root, axis, data) {
    const axesAvg = (data.diagnosis && data.diagnosis.axes_avg) || {};
    const examplesByPrinciple = data.examples_by_principle || {};
    const coachAvailable = !!(data.stats && data.stats.coach_available);

    const section = el('section', { class: 'axis-section' });

    const avgScore = axesAvg[axis.id];
    const cls = `axis-score-chip ${axisChipClass(avgScore)}`.trim();
    const header = el('div', { class: 'axis-header' },
      el('h2', null,
        `${axis.label} — ${axis.summary || ''}`,
        el('span', {
          class: 'help', tabindex: '0', 'aria-label': '도움말',
          'data-tip': axis.summary || axis.label,
        }, ' ? '),
      ),
      el('span', { class: cls },
        '평균 ',
        el('span', { class: 'v mono' }, fmtScore(avgScore, 1)),
        ' / 20',
      ),
    );
    section.appendChild(header);

    (axis.principles || []).forEach((p) => {
      section.appendChild(renderPrincipleCard(p, examplesByPrinciple[p.id] || [], coachAvailable));
    });

    root.appendChild(section);
  }

  function renderPrincipleCard(principle, examples, coachAvailable) {
    const card = el('div', { class: 'principle-card' });
    card.appendChild(el('h3', { class: 'principle-title' }, principle.title || ''));
    if (principle.body) {
      card.appendChild(el('p', { class: 'principle-body' }, principle.body));
    }

    if (Array.isArray(principle.linked_metrics) && principle.linked_metrics.length) {
      const linked = el('div', { class: 'principle-linked mono' }, '연관 지표: ');
      principle.linked_metrics.forEach((m) => {
        linked.appendChild(el('span', { class: 'lk' }, m));
      });
      card.appendChild(linked);
    }

    if (principle.anti_pattern || principle.good_pattern) {
      const cmp = el('div', { class: 'code-compare' },
        el('div', { class: 'code-block bad' },
          el('span', { class: 'code-label' }, '❌ 안 좋음'),
          principle.anti_pattern || '(없음)',
        ),
        el('div', { class: 'code-block good' },
          el('span', { class: 'code-label' }, '✅ 더 좋음'),
          principle.good_pattern || '(없음)',
        ),
      );
      card.appendChild(cmp);
    }

    // 내 사례 섹션
    const details = el('details', { class: 'principle-examples' });
    details.appendChild(el('summary', null,
      ` 내 사례 (${examples.length})`,
    ));

    if (!examples.length) {
      details.appendChild(el('div', { class: 'examples-empty' },
        '관련된 worst spot 이 분석된 세션에서 아직 발견되지 않았어요.',
      ));
    } else {
      examples.forEach((ex) => {
        details.appendChild(renderExampleSession(ex, coachAvailable));
      });
    }
    card.appendChild(details);

    return card;
  }

  function renderExampleSession(ex, coachAvailable) {
    const wrap = el('div', { class: 'example-session', dataset: { sessionId: ex.session_id || '' } });

    const left = el('div');
    const meta = el('div', { class: 'example-meta' },
      el('span', { class: 'mono' }, fmtTimestamp(ex.start_ts)),
      el('span', { class: 'em-cwd mono', title: ex.cwd || '' }, tailCwd(ex.cwd)),
      ex.session_type ? el('span', { class: 'em-type' }, ex.session_type) : null,
      el('span', { class: 'em-score mono' }, `점수 ${fmtScore(ex.score_total, 1)}`),
    );
    left.appendChild(meta);

    // 첫 worst spot 사용
    const spot = (ex.worst_spots && ex.worst_spots[0]) || null;
    if (spot) {
      if (spot.summary) {
        left.appendChild(el('p', { class: 'example-summary' }, spot.summary));
      }
      if (spot.user_prompt_excerpt) {
        left.appendChild(el('blockquote', { class: 'example-quote' },
          spot.user_prompt_excerpt,
        ));
      }
      if (spot.suggestion) {
        left.appendChild(el('p', { class: 'example-suggest' },
          el('strong', null, '제안: '),
          spot.suggestion,
        ));
      }
    }

    if (ex.metrics_excerpt && Object.keys(ex.metrics_excerpt).length) {
      const parts = Object.entries(ex.metrics_excerpt).map(([k, v]) => `${k}=${v}`);
      left.appendChild(el('div', { class: 'example-metrics mono' }, parts.join(' · ')));
    }

    wrap.appendChild(left);

    // actions (coach button)
    const actions = el('div', { class: 'example-actions' });
    const btn = el('button', {
      class: 'coach-button',
      type: 'button',
      'aria-label': 'Claude 코칭 받기',
    }, 'Claude 코칭 받기');

    if (!coachAvailable) {
      btn.disabled = true;
      // help-tooltip 시스템에 태우려고 .help 와 같은 data-tip 을 button 에 직접 달기는 어려우니
      // span 으로 안내. (대신 title 도 fallback)
      btn.title = 'ANTHROPIC_API_KEY 설정 필요';
      const hint = el('span', {
        class: 'help', tabindex: '0', 'aria-label': '도움말',
        'data-tip': 'ANTHROPIC_API_KEY 설정 필요',
        style: 'align-self:flex-end;',
      }, ' ? ');
      actions.appendChild(hint);
    }

    const result = el('div', { class: 'coach-result hidden' });

    btn.addEventListener('click', async () => {
      if (btn.disabled) return;
      if (!ex.session_id) {
        showCoachError(result, 'session_id 가 비어 있습니다.');
        return;
      }
      btn.disabled = true;
      const prevLabel = btn.textContent;
      btn.textContent = '코칭 중…';
      result.className = 'coach-result';
      result.classList.add('hidden');
      result.textContent = '';

      try {
        const data = await postCoach(ex.session_id);
        showCoachSuccess(result, data);
        btn.textContent = '재요청';
      } catch (err) {
        console.error('coach failed', err);
        showCoachError(result, err && err.message ? err.message : String(err));
        btn.textContent = prevLabel || 'Claude 코칭 받기';
      } finally {
        btn.disabled = false;
      }
    });

    actions.appendChild(btn);
    wrap.appendChild(actions);
    wrap.appendChild(result);
    return wrap;
  }

  function showCoachSuccess(container, data) {
    container.className = 'coach-result';
    container.classList.remove('hidden');
    container.innerHTML = '';

    const inner = document.createElement('div');
    inner.innerHTML = renderMarkdown(data.text || '(빈 응답)');
    container.appendChild(inner);

    const meta = el('div', { class: 'coach-meta mono' },
      `model: ${data.model || '–'} · ${data.elapsed_sec != null ? data.elapsed_sec.toFixed(1) + 's' : '–'} · stop: ${data.stop_reason || '–'}`,
    );
    container.appendChild(meta);
  }

  function showCoachError(container, msg) {
    container.className = 'coach-result error';
    container.classList.remove('hidden');
    container.textContent = `코칭 요청 실패: ${msg}`;
  }

  function renderSessionTypes(root, data) {
    const types = (data.principles && data.principles.session_types) || {};
    const ids = Object.keys(types);
    if (!ids.length) return;

    const section = el('section');
    section.appendChild(el('div', { class: 'axis-header' },
      el('h2', null,
        '세션 유형별 잣대',
        el('span', {
          class: 'help', tabindex: '0', 'aria-label': '도움말',
          'data-tip': '세션 유형마다 점수 가중치(공정한 축)가 다릅니다. 예를 들어 원샷 질문 세션을 탐색 세션의 잣대로 평가하지 않아요.',
        }, ' ? '),
      ),
    ));

    const grid = el('div', { class: 'session-type-grid' });
    ids.forEach((tid) => {
      const t = types[tid] || {};
      const card = el('div', { class: 'session-type-card' });
      card.appendChild(el('h3', null, t.label || SESSION_TYPE_LABELS_FALLBACK[tid] || tid));
      if (t.expectation) {
        card.appendChild(el('p', { class: 'stype-expectation' }, t.expectation));
      }
      const fairAxes = Array.isArray(t.fair_axes) ? t.fair_axes : [];
      if (fairAxes.length) {
        const axesEl = el('div', { class: 'stype-axes' });
        fairAxes.forEach((a) => {
          axesEl.appendChild(el('span', { class: 'stype-axis' },
            AXIS_LABELS[a] || a,
          ));
        });
        card.appendChild(axesEl);
      }
      grid.appendChild(card);
    });

    section.appendChild(grid);
    root.appendChild(section);
  }

  function renderFooter(root) {
    root.appendChild(el('footer', { class: 'guide-footer' },
      '원칙은 사용자의 개인 학습을 돕기 위한 시작점입니다. 시간이 지나면서 본인만의 원칙을 만들어 나가세요.',
    ));
  }

  function renderAll(data) {
    const root = $('#guide-root');
    root.innerHTML = '';

    renderDiagnosis(root, data);

    const axes = (data.principles && data.principles.axes) || [];
    axes.forEach((axis) => renderAxisSection(root, axis, data));

    renderSessionTypes(root, data);
    renderFooter(root);

    $('#guide-loading').classList.add('hidden');
    root.classList.remove('hidden');
  }

  // ---------- viewport-aware help tooltip (app.js 와 동일 로직) ----------
  function setupHelpTooltips() {
    const tip = document.createElement('div');
    tip.className = 'help-tooltip';
    tip.setAttribute('role', 'tooltip');
    document.body.appendChild(tip);

    let currentTrigger = null;
    const MARGIN = 8;
    const VIEW_PAD = 8;

    function position(trigger) {
      const text = trigger.getAttribute('data-tip') || '';
      tip.textContent = text;
      tip.style.maxWidth = '';
      tip.classList.remove('place-above', 'place-below');
      tip.style.visibility = 'hidden';
      tip.classList.add('visible');

      const trect = trigger.getBoundingClientRect();
      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const ttRect = tip.getBoundingClientRect();
      const tw = ttRect.width;
      const th = ttRect.height;

      const spaceAbove = trect.top;
      const spaceBelow = vh - trect.bottom;
      const placeAbove = spaceAbove >= th + MARGIN || spaceAbove >= spaceBelow;
      let top;
      if (placeAbove) {
        top = trect.top - th - MARGIN;
        tip.classList.add('place-above');
      } else {
        top = trect.bottom + MARGIN;
        tip.classList.add('place-below');
      }
      if (top < VIEW_PAD) top = VIEW_PAD;
      if (top + th > vh - VIEW_PAD) top = Math.max(VIEW_PAD, vh - th - VIEW_PAD);

      const triggerCenterX = trect.left + trect.width / 2;
      let left = triggerCenterX - tw / 2;
      if (left < VIEW_PAD) left = VIEW_PAD;
      if (left + tw > vw - VIEW_PAD) left = vw - tw - VIEW_PAD;

      const arrowLeft = Math.min(
        Math.max(triggerCenterX - left, 12),
        tw - 12,
      );
      tip.style.setProperty('--arrow-left', arrowLeft + 'px');

      tip.style.top = Math.round(top) + 'px';
      tip.style.left = Math.round(left) + 'px';
      tip.style.visibility = '';
    }

    function show(trigger) {
      if (currentTrigger === trigger) return;
      currentTrigger = trigger;
      position(trigger);
    }
    function hide(trigger) {
      if (trigger && trigger !== currentTrigger) return;
      currentTrigger = null;
      tip.classList.remove('visible', 'place-above', 'place-below');
    }

    document.addEventListener('mouseover', (e) => {
      const t = e.target.closest('.help');
      if (t) show(t);
    });
    document.addEventListener('mouseout', (e) => {
      const t = e.target.closest('.help');
      if (!t) return;
      const related = e.relatedTarget && e.relatedTarget.closest && e.relatedTarget.closest('.help');
      if (related === t) return;
      hide(t);
    });
    document.addEventListener('focusin', (e) => {
      const t = e.target.closest('.help');
      if (t) show(t);
    });
    document.addEventListener('focusout', (e) => {
      const t = e.target.closest('.help');
      if (t) hide(t);
    });
    window.addEventListener('scroll', () => {
      if (currentTrigger) position(currentTrigger);
    }, true);
    window.addEventListener('resize', () => {
      if (currentTrigger) position(currentTrigger);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && currentTrigger) hide(currentTrigger);
    });
  }

  // ---------- bootstrap ----------
  async function init() {
    setupHelpTooltips();
    try {
      const data = await fetchGuide();
      hideError();
      state.data = data;
      renderAll(data);
    } catch (err) {
      console.error('guide load failed', err);
      showError(`가이드 데이터를 불러오지 못했습니다: ${err.message}`);
      $('#guide-loading').textContent = '데이터를 불러오지 못했습니다.';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
