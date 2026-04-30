// Claude Coach — single-file vanilla JS dashboard
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
  const TOOL_PALETTE = [
    '#7aa2f7', '#56d364', '#e3b341', '#f0883e',
    '#bc8cff', '#79c0ff', '#ff7b72', '#a5d6ff',
  ];

  // Chart.js global defaults (dark theme)
  if (window.Chart) {
    Chart.defaults.color = COLORS.muted;
    Chart.defaults.borderColor = COLORS.border;
    Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Pretendard', 'Noto Sans KR', sans-serif";
  }

  // ---------- state ----------
  const state = {
    sessions: [],
    charts: { radar: null, trend: null, tools: null, modalRadar: null, modalTools: null },
    lastFocus: null,
  };

  // ---------- helpers ----------
  const $ = (sel) => document.querySelector(sel);

  function showError(msg) {
    const el = $('#error-banner');
    el.textContent = msg;
    el.classList.remove('hidden');
  }

  function hideError() {
    $('#error-banner').classList.add('hidden');
  }

  function fmtDuration(sec) {
    if (sec == null || isNaN(sec)) return '–';
    const s = Math.max(0, Math.round(sec));
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    const r = s % 60;
    if (h > 0) return `${h}시 ${String(m).padStart(2, '0')}분`;
    if (m > 0) return `${m}분 ${String(r).padStart(2, '0')}초`;
    return `${r}초`;
  }

  function fmtTotalDuration(secTotal) {
    if (!secTotal) return '0시간';
    const h = Math.floor(secTotal / 3600);
    const m = Math.floor((secTotal % 3600) / 60);
    return `${h}시 ${String(m).padStart(2, '0')}분`;
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

  function fmtNumber(n, digits = 0) {
    if (n == null || isNaN(n)) return '–';
    return Number(n).toLocaleString('ko-KR', {
      minimumFractionDigits: digits,
      maximumFractionDigits: digits,
    });
  }

  function fmtPct(rate, digits = 1) {
    if (rate == null || isNaN(rate)) return '–';
    return `${(rate * 100).toFixed(digits)}%`;
  }

  function tailCwd(cwd) {
    if (!cwd) return '–';
    const parts = cwd.split('/').filter(Boolean);
    if (parts.length <= 2) return cwd;
    return '…/' + parts.slice(-2).join('/');
  }

  function scoreClass(total) {
    if (total >= 75) return 'good';
    if (total >= 50) return 'warn';
    return 'bad';
  }

  function scoreColor(total) {
    if (total >= 75) return COLORS.good;
    if (total >= 50) return COLORS.warn;
    return COLORS.bad;
  }

  function topTools(map, k = 2) {
    if (!map) return [];
    return Object.entries(map)
      .sort((a, b) => b[1] - a[1])
      .slice(0, k);
  }

  function avg(arr) {
    if (!arr.length) return 0;
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }

  function sum(arr) {
    return arr.reduce((a, b) => a + (b || 0), 0);
  }

  // ---------- data fetch ----------
  async function fetchSessions() {
    const res = await fetch('/api/sessions', { headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error(`/api/sessions HTTP ${res.status}`);
    const data = await res.json();
    if (!Array.isArray(data)) throw new Error('서버 응답이 배열이 아닙니다.');
    return data;
  }

  async function fetchSession(id) {
    const res = await fetch(`/api/session/${encodeURIComponent(id)}`, {
      headers: { Accept: 'application/json' },
    });
    if (!res.ok) throw new Error(`/api/session/${id} HTTP ${res.status}`);
    return res.json();
  }

  // ---------- rendering ----------
  function renderHeaderStats(sessions) {
    $('#stat-total-sessions').textContent = fmtNumber(sessions.length);
    $('#stat-total-time').textContent = fmtTotalDuration(sum(sessions.map((s) => s.duration_sec || 0)));

    const totals = sessions.map((s) => (s.score && s.score.total) || 0);
    const overallAvg = avg(totals);
    $('#stat-avg-score').textContent = totals.length ? overallAvg.toFixed(1) : '–';

    const recent = [...sessions]
      .sort((a, b) => new Date(b.start_ts) - new Date(a.start_ts))
      .slice(0, 10);
    const recentAvg = avg(recent.map((s) => (s.score && s.score.total) || 0));
    $('#stat-recent-score').textContent = recent.length ? recentAvg.toFixed(1) : '–';

    const deltaEl = $('#stat-recent-delta');
    if (recent.length && totals.length) {
      const delta = recentAvg - overallAvg;
      const cls = delta > 0.05 ? 'up' : delta < -0.05 ? 'down' : 'flat';
      const sign = delta > 0 ? '+' : '';
      const arrow = cls === 'up' ? '▲' : cls === 'down' ? '▼' : '→';
      deltaEl.className = `delta ${cls}`;
      deltaEl.textContent = `${arrow} ${sign}${delta.toFixed(1)}`;
    } else {
      deltaEl.className = 'delta';
      deltaEl.textContent = '';
    }
  }

  function renderMetricCards(sessions) {
    const thinkingTotal = sum(sessions.map((s) => s.thinking_chars_total || 0));
    const parallelAvg = avg(sessions.map((s) => s.parallel_rate || 0));
    const subagentTotal = sum(sessions.map((s) => s.subagent_invocations || 0));
    const correctionAvg = avg(sessions.map((s) => s.correction_rate || 0));

    $('#metric-thinking').textContent = fmtNumber(thinkingTotal);
    $('#metric-parallel').textContent = fmtPct(parallelAvg, 1);
    $('#metric-subagent').textContent = fmtNumber(subagentTotal);
    $('#metric-correction').textContent = fmtPct(correctionAvg, 1);
  }

  function aggregateAxes(sessions) {
    const sums = Object.fromEntries(AXES.map((a) => [a, 0]));
    let n = 0;
    sessions.forEach((s) => {
      if (!s.score || !s.score.axes) return;
      AXES.forEach((a) => {
        const v = s.score.axes[a];
        if (typeof v === 'number') sums[a] += v;
      });
      n++;
    });
    if (!n) return AXES.map(() => 0);
    return AXES.map((a) => sums[a] / n);
  }

  function renderRadarChart(sessions) {
    const ctx = document.getElementById('radar-chart').getContext('2d');
    if (state.charts.radar) state.charts.radar.destroy();

    const overall = aggregateAxes(sessions);
    const recent = [...sessions]
      .sort((a, b) => new Date(b.start_ts) - new Date(a.start_ts))
      .slice(0, 10);
    const recentAxes = aggregateAxes(recent);

    state.charts.radar = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: AXES.map((a) => AXIS_LABELS[a]),
        datasets: [
          {
            label: '전체 평균',
            data: overall,
            backgroundColor: 'rgba(122, 162, 247, 0.15)',
            borderColor: COLORS.accent,
            borderWidth: 2,
            pointBackgroundColor: COLORS.accent,
            pointRadius: 3,
          },
          {
            label: '최근 10세션',
            data: recentAxes,
            backgroundColor: 'rgba(86, 211, 100, 0.15)',
            borderColor: COLORS.good,
            borderWidth: 2,
            pointBackgroundColor: COLORS.good,
            pointRadius: 3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom', labels: { color: COLORS.text } } },
        scales: {
          r: {
            min: 0,
            max: 20,
            ticks: { stepSize: 5, color: COLORS.muted, backdropColor: 'transparent' },
            angleLines: { color: COLORS.border },
            grid: { color: COLORS.border },
            pointLabels: { color: COLORS.text, font: { size: 12 } },
          },
        },
      },
    });
  }

  function renderTrendChart(sessions) {
    const ctx = document.getElementById('trend-chart').getContext('2d');
    if (state.charts.trend) state.charts.trend.destroy();

    const ordered = [...sessions]
      .filter((s) => s.start_ts)
      .sort((a, b) => new Date(a.start_ts) - new Date(b.start_ts))
      .slice(-30);

    const labels = ordered.map((s) => fmtTimestamp(s.start_ts));
    const values = ordered.map((s) => (s.score && s.score.total) || 0);

    state.charts.trend = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Coach Score',
          data: values,
          borderColor: COLORS.accent,
          backgroundColor: 'rgba(122, 162, 247, 0.18)',
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointBackgroundColor: COLORS.accent,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { min: 0, max: 100, ticks: { color: COLORS.muted }, grid: { color: COLORS.border } },
          x: { ticks: { color: COLORS.muted, maxRotation: 0, autoSkip: true, maxTicksLimit: 8 }, grid: { color: 'transparent' } },
        },
      },
    });
  }

  function renderToolsChart(sessions) {
    const ctx = document.getElementById('tools-chart').getContext('2d');
    if (state.charts.tools) state.charts.tools.destroy();

    const totals = {};
    sessions.forEach((s) => {
      const m = s.tool_calls_by_name || {};
      Object.entries(m).forEach(([k, v]) => {
        totals[k] = (totals[k] || 0) + v;
      });
    });
    const top = Object.entries(totals).sort((a, b) => b[1] - a[1]).slice(0, 8);

    if (!top.length) {
      state.charts.tools = new Chart(ctx, {
        type: 'doughnut',
        data: { labels: ['데이터 없음'], datasets: [{ data: [1], backgroundColor: [COLORS.border] }] },
        options: { plugins: { legend: { display: false } } },
      });
      return;
    }

    state.charts.tools = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: top.map((t) => t[0]),
        datasets: [{
          data: top.map((t) => t[1]),
          backgroundColor: top.map((_, i) => TOOL_PALETTE[i % TOOL_PALETTE.length]),
          borderColor: COLORS.card,
          borderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { color: COLORS.text, boxWidth: 12 } },
        },
      },
    });
  }

  function renderTips(sessions) {
    const list = $('#tips-list');
    list.innerHTML = '';

    const counts = {}; // key -> { count, message, priority }
    sessions.forEach((s) => {
      (s.tips || []).forEach((tip) => {
        if (!tip || tip.priority !== 1 || !tip.key) return;
        if (!counts[tip.key]) counts[tip.key] = { count: 0, message: tip.message || '', priority: tip.priority };
        counts[tip.key].count += 1;
        if (!counts[tip.key].message && tip.message) counts[tip.key].message = tip.message;
      });
    });

    const top = Object.entries(counts)
      .map(([key, v]) => ({ key, ...v }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    if (!top.length) {
      const p = document.createElement('div');
      p.className = 'tips-empty';
      p.textContent = '아직 반복 등장한 priority 1 팁이 없습니다.';
      list.appendChild(p);
      return;
    }

    top.forEach((tip) => {
      const card = document.createElement('div');
      card.className = 'tip-card';

      const k = document.createElement('div');
      k.className = 'tip-key mono';
      k.textContent = tip.key;
      card.appendChild(k);

      const m = document.createElement('div');
      m.className = 'tip-message';
      m.textContent = tip.message || '(메시지 없음)';
      card.appendChild(m);

      const c = document.createElement('div');
      c.className = 'tip-count';
      c.textContent = `이 패턴이 ${tip.count}개 세션에서 보였어요`;
      card.appendChild(c);

      list.appendChild(card);
    });
  }

  function renderTable(sessions) {
    const tbody = $('#sessions-tbody');
    tbody.innerHTML = '';

    const ordered = [...sessions].sort((a, b) => new Date(b.start_ts) - new Date(a.start_ts));
    ordered.forEach((s) => {
      const tr = document.createElement('tr');
      tr.tabIndex = 0;
      tr.dataset.sessionId = s.session_id;
      tr.addEventListener('click', () => openModal(s.session_id));
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openModal(s.session_id); }
      });

      const total = (s.score && s.score.total) || 0;

      tr.appendChild(td(fmtTimestamp(s.start_ts), 'col-time'));
      tr.appendChild(td(tailCwd(s.cwd), 'col-cwd', s.cwd || ''));
      tr.appendChild(td(fmtDuration(s.duration_sec), 'col-duration'));

      const scoreTd = document.createElement('td');
      scoreTd.className = 'col-score';
      const pill = document.createElement('span');
      pill.className = `score-pill ${scoreClass(total)}`;
      pill.textContent = total.toFixed(1);
      scoreTd.appendChild(pill);
      tr.appendChild(scoreTd);

      tr.appendChild(td(`${s.user_turns ?? '–'} → ${s.assistant_turns ?? '–'}`, 'col-turns'));

      const tools = topTools(s.tool_calls_by_name, 2)
        .map(([k, v]) => `${k}(${v})`).join(', ') || '–';
      tr.appendChild(td(tools, 'col-tools'));

      tbody.appendChild(tr);
    });
  }

  function td(text, cls, title) {
    const el = document.createElement('td');
    if (cls) el.className = cls;
    el.textContent = text;
    if (title) el.title = title;
    return el;
  }

  // ---------- modal ----------
  async function openModal(id) {
    state.lastFocus = document.activeElement;
    const backdrop = $('#modal-backdrop');
    const body = $('#modal-body');
    body.innerHTML = '<p class="card-hint">불러오는 중…</p>';
    backdrop.classList.remove('hidden');
    $('#modal-close').focus();

    try {
      const s = await fetchSession(id);
      renderModal(s);
    } catch (err) {
      console.error('session detail load failed', err);
      body.innerHTML = '<p class="card-hint">세션 상세를 불러오지 못했습니다.</p>';
    }
  }

  function closeModal() {
    $('#modal-backdrop').classList.add('hidden');
    if (state.charts.modalRadar) { state.charts.modalRadar.destroy(); state.charts.modalRadar = null; }
    if (state.charts.modalTools) { state.charts.modalTools.destroy(); state.charts.modalTools = null; }
    if (state.lastFocus && state.lastFocus.focus) state.lastFocus.focus();
  }

  function renderModal(s) {
    const body = $('#modal-body');
    body.innerHTML = '';

    const total = (s.score && s.score.total) || 0;
    $('#modal-title').textContent = `세션 ${s.session_id ? s.session_id.slice(0, 8) : ''} · 점수 ${total.toFixed(1)}`;

    // metrics
    const metricsSec = document.createElement('div');
    metricsSec.className = 'modal-section';
    metricsSec.innerHTML = '<h3>주요 메트릭</h3>';
    const grid = document.createElement('div');
    grid.className = 'metric-detail-grid';

    const items = [
      ['시작', fmtTimestamp(s.start_ts)],
      ['종료', fmtTimestamp(s.end_ts)],
      ['기간', fmtDuration(s.duration_sec)],
      ['cwd', s.cwd || '–'],
      ['git branch', s.git_branch || '–'],
      ['version', s.version || '–'],
      ['user turns', fmtNumber(s.user_turns)],
      ['assistant turns', fmtNumber(s.assistant_turns)],
      ['sidechain turns', fmtNumber(s.sidechain_assistant_turns)],
      ['first prompt chars', fmtNumber(s.first_prompt_chars)],
      ['avg prompt chars', fmtNumber(s.avg_prompt_chars, 1)],
      ['median prompt chars', fmtNumber(s.median_prompt_chars, 1)],
      ['prompt specificity', fmtNumber(s.prompt_specificity, 4)],
      ['correction signals', fmtNumber(s.correction_signals)],
      ['correction rate', fmtPct(s.correction_rate, 2)],
      ['tool calls total', fmtNumber(s.tool_calls_total)],
      ['parallel calls', fmtNumber(s.parallel_tool_calls)],
      ['parallel rate', fmtPct(s.parallel_rate, 2)],
      ['subagent invocations', fmtNumber(s.subagent_invocations)],
      ['plan tool uses', fmtNumber(s.plan_tool_uses)],
      ['bash total', fmtNumber(s.bash_total)],
      ['bash failures', fmtNumber(s.bash_failures)],
      ['bash fail rate', fmtPct(s.bash_fail_rate, 2)],
      ['edit string not found', fmtNumber(s.edit_string_not_found)],
      ['file reads total', fmtNumber(s.file_reads_total)],
      ['file reread count', fmtNumber(s.file_reread_count)],
      ['file reread rate', fmtPct(s.file_reread_rate, 2)],
      ['redundant searches', fmtNumber(s.redundant_searches)],
      ['thinking chars total', fmtNumber(s.thinking_chars_total)],
      ['thinking blocks', fmtNumber(s.thinking_blocks)],
      ['thinking avg/turn', fmtNumber(s.thinking_chars_avg_per_turn, 1)],
      ['assistant text chars', fmtNumber(s.assistant_text_chars)],
    ];

    items.forEach(([k, v]) => {
      const it = document.createElement('div');
      it.className = 'metric-detail-item';
      const kk = document.createElement('div'); kk.className = 'k'; kk.textContent = k;
      const vv = document.createElement('div'); vv.className = 'v'; vv.textContent = v;
      it.appendChild(kk); it.appendChild(vv);
      grid.appendChild(it);
    });

    metricsSec.appendChild(grid);
    body.appendChild(metricsSec);

    // tips
    const tipsSec = document.createElement('div');
    tipsSec.className = 'modal-section';
    tipsSec.innerHTML = '<h3>이 세션의 팁</h3>';
    if (!s.tips || !s.tips.length) {
      const p = document.createElement('p'); p.className = 'card-hint'; p.textContent = '팁이 없습니다.';
      tipsSec.appendChild(p);
    } else {
      [...s.tips]
        .sort((a, b) => (a.priority || 99) - (b.priority || 99))
        .forEach((tip) => {
          const t = document.createElement('div');
          t.className = 'modal-tip';
          const k = document.createElement('div');
          k.className = 'tk mono';
          k.textContent = `priority ${tip.priority ?? '–'} · ${tip.key || ''}`;
          t.appendChild(k);
          const m = document.createElement('div');
          m.textContent = tip.message || '';
          t.appendChild(m);
          tipsSec.appendChild(t);
        });
    }
    body.appendChild(tipsSec);

    // charts
    const chartsSec = document.createElement('div');
    chartsSec.className = 'modal-section';
    chartsSec.innerHTML = '<h3>차트</h3>';

    const grid2 = document.createElement('div');
    grid2.className = 'modal-charts';

    const radarBox = document.createElement('div');
    radarBox.className = 'modal-chart-wrap';
    radarBox.innerHTML = '<h4>5축 점수</h4>';
    const radarCanvasWrap = document.createElement('div');
    radarCanvasWrap.className = 'modal-chart-canvas-wrap';
    const radarCanvas = document.createElement('canvas');
    radarCanvasWrap.appendChild(radarCanvas);
    radarBox.appendChild(radarCanvasWrap);

    const toolsBox = document.createElement('div');
    toolsBox.className = 'modal-chart-wrap';
    toolsBox.innerHTML = '<h4>툴 사용</h4>';
    const toolsCanvasWrap = document.createElement('div');
    toolsCanvasWrap.className = 'modal-chart-canvas-wrap';
    const toolsCanvas = document.createElement('canvas');
    toolsCanvasWrap.appendChild(toolsCanvas);
    toolsBox.appendChild(toolsCanvasWrap);

    grid2.appendChild(radarBox);
    grid2.appendChild(toolsBox);
    chartsSec.appendChild(grid2);
    body.appendChild(chartsSec);

    // build modal radar
    const axesData = AXES.map((a) => (s.score && s.score.axes && s.score.axes[a]) || 0);
    state.charts.modalRadar = new Chart(radarCanvas.getContext('2d'), {
      type: 'radar',
      data: {
        labels: AXES.map((a) => AXIS_LABELS[a]),
        datasets: [{
          label: '이 세션',
          data: axesData,
          backgroundColor: 'rgba(122, 162, 247, 0.18)',
          borderColor: scoreColor(total),
          borderWidth: 2,
          pointBackgroundColor: scoreColor(total),
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          r: {
            min: 0, max: 20,
            ticks: { stepSize: 5, color: COLORS.muted, backdropColor: 'transparent' },
            angleLines: { color: COLORS.border },
            grid: { color: COLORS.border },
            pointLabels: { color: COLORS.text, font: { size: 11 } },
          },
        },
      },
    });

    // build modal tools doughnut
    const tools = Object.entries(s.tool_calls_by_name || {}).sort((a, b) => b[1] - a[1]);
    if (tools.length) {
      state.charts.modalTools = new Chart(toolsCanvas.getContext('2d'), {
        type: 'doughnut',
        data: {
          labels: tools.map((t) => t[0]),
          datasets: [{
            data: tools.map((t) => t[1]),
            backgroundColor: tools.map((_, i) => TOOL_PALETTE[i % TOOL_PALETTE.length]),
            borderColor: COLORS.card,
            borderWidth: 2,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { color: COLORS.text, boxWidth: 10, font: { size: 11 } } } },
        },
      });
    } else {
      toolsCanvasWrap.innerHTML = '<p class="card-hint chart-empty">툴 사용 없음</p>';
    }
  }

  // ---------- bootstrapping ----------
  function bindModalEvents() {
    $('#modal-close').addEventListener('click', closeModal);
    $('#modal-backdrop').addEventListener('click', (e) => {
      if (e.target === e.currentTarget) closeModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !$('#modal-backdrop').classList.contains('hidden')) {
        closeModal();
      }
    });
  }

  async function init() {
    bindModalEvents();
    try {
      const sessions = await fetchSessions();
      hideError();
      state.sessions = sessions;

      if (!sessions.length) {
        $('#empty-state').classList.remove('hidden');
        $('#dashboard').classList.add('hidden');
        return;
      }

      $('#empty-state').classList.add('hidden');
      $('#dashboard').classList.remove('hidden');

      renderHeaderStats(sessions);
      renderRadarChart(sessions);
      renderTrendChart(sessions);
      renderToolsChart(sessions);
      renderMetricCards(sessions);
      renderTips(sessions);
      renderTable(sessions);
    } catch (err) {
      console.error('dashboard load failed', err);
      showError(`세션 데이터를 불러오지 못했습니다: ${err.message}`);
      $('#dashboard').classList.add('hidden');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
