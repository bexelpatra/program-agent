---
title: "매시간 윤리 학습 자료가 텔레그램으로 오는 봇 만들기 — 그리고 같은 봇 토큰으로 polling 두 번 시작하면 안 되는 이유"
category: "Claude Code"
tags: ["Claude Code", "claude-code", "Telegram Bot API", "long-polling", "Elasticsearch", "systemd timer", "TypeScript", "SQLite", "마이크로서비스", "자동화", "임용고시", "윤리"]
---

# 매시간 윤리 학습 자료가 텔레그램으로 오는 봇 만들기

윤리 임용고시 준비 중인데, 책상 앞에 앉아있을 때만 공부하지 말고 자투리 시간에도 한 토막씩 흘러왔으면 좋겠다 싶었다. 마침 그동안 적재해 둔 ES(Elasticsearch) 윤리 인덱스 — 사상가 387명분의 검증된 주장(claim) · 해설 · 논거 · 반론이 들어있는 — 가 놀고 있었다. 매시간 09–18시에 한 건씩 텔레그램으로 받자.

오늘(2026-04-28) 만든 작은 서비스 `ethics-pulse` 의 설계 회고다. 코드 양은 적지만, 중간에 한 번 깊이 짚어야 할 함정이 하나 있었다 — **같은 봇 토큰을 두 프로세스가 동시에 polling 하면 안 된다**는 것. 이걸 원리부터 정리한다.

## 무엇을 만들었나

```
[systemd user timer] ─매시 정각(09–18 KST)─▶ ethics-pulse(oneshot)
                                                ├─▶ ES(:9200) ethics-claims 검색
                                                ├─▶ ethics-thinkers/works mget으로 사상가·작품명 조회
                                                ├─▶ formatter (현재 v1_emoji)
                                                ├─▶ 텔레그램 sendMessage HTTP
                                                └─▶ SQLite history.db 기록
```

스펙:

- 하루 10회 (09·10·…·18시 정각)
- 1건 = `ethics-claims` 1 doc — claim · explanation · argument · counterpoint · keywords 한 묶음 (대략 1,500–2,000자, 3분 분량)
- 같은 doc 14일 안에 중복 발송 금지 (SQLite dedup)
- 후보 풀(`verified=true` 필터) 387건. 14일 × 10회 = 140회/14일이라 풀이 충분히 큼
- 봇은 nanoclaw 의 a45hvn-agent-bot 재사용 (토큰만 공유, 수신은 안 함)

코드는 신규 디렉토리 `projects/ethics-pulse/` 단독 7개 파일 (config · es-client · selector · formatter · history · telegram · index). nanoclaw 코드는 한 줄도 손대지 않았다.

## 왜 nanoclaw 에 통합하지 않았나

기존 nanoclaw 안에는 이미 cron 비슷한 `task-scheduler.ts` 가 있다. 거기에 끼워넣었으면 코드 양은 더 적었을 것이다.

그런데 학습 콘텐츠는 자주 바뀐다 — 포맷터를 바꿔보고 싶을 수도 있고, 인덱스를 늘리고 싶을 수도 있고, 발송 시각을 조정할 수도 있다. 그때마다 nanoclaw 를 빌드하고 systemd 재시작하는 건 결합도가 너무 높다. nanoclaw 는 텔레그램 봇 + Claude Agent SDK 컨테이너 오케스트레이션이라는 더 무거운 책임을 진다.

그래서 신규 마이크로서비스 1개로 분리. **봇 토큰만 공유하고, 코드/DB/스케줄/배포는 완전 독립.**

이 결정이 다음 함정으로 자연스럽게 이어졌다.

## 봇 토큰 하나로 polling 두 번 — 왜 안 되나 (원리부터)

텔레그램 봇이 새 메시지를 받는 방식은 두 가지뿐이다.

1. **Webhook**: 메시지가 오면 텔레그램이 내 서버 URL 로 HTTP POST 를 쏨. 내 서버가 공인 도메인 + TLS 로 듣고 있어야 함.
2. **Polling**: 내 프로그램이 텔레그램 API 에 "새 거 있어?" 주기적으로 물어봄 (`getUpdates` HTTP 호출).

**Long-polling** 은 polling 의 효율 개선판. 그냥 polling 은 "있어? → 없어"를 1초마다 반복해 트래픽이 낭비되는데, long-polling 은 한 번 요청을 보내면 텔레그램이 **새 메시지가 도착할 때까지 응답을 최대 N초(기본 30초) 동안 보류**한다. 도착하면 즉시 응답, 안 오면 N초 후 빈 응답 → 다시 요청. 사실상 실시간이면서 호출 수는 적다.

`grammy` (Node.js 텔레그램 봇 라이브러리)는 내부적으로 long-polling 으로 메시지를 받는다. 그래서 nanoclaw 가 떠 있는 동안 a45hvn-agent-bot 은 **항상 텔레그램에 `getUpdates` 연결을 유지**하고 있다.

여기서 결정적인 사실: **텔레그램은 한 봇 토큰에 대해 `getUpdates` 호출자를 1개로만 허용한다.** 두 프로세스가 같은 토큰으로 polling 을 시작하면 두 번째 호출에 `409 Conflict` 가 떨어지고, 두 봇 사이에서 메시지가 들쑥날쑥 사라진다.

ethics-pulse 가 grammy 를 깔고 무심코 `bot.start()` 를 호출하면 nanoclaw 봇이 텔레그램 메시지 수신을 못 하게 된다. 사용자에게 "봇이 답을 안 해요" 사고가 난다.

해결은 단순하다. **`sendMessage` 같은 송신 API 는 이 1개 제한이 없다.** 여러 프로세스가 같은 토큰으로 동시에 보내도 OK. ethics-pulse 는 받을 일이 없으니 polling 자체를 시작 안 하면 된다.

구체적으로:

- 라이브러리(grammy 등) 자체를 안 쓰고 native fetch 로 `POST https://api.telegram.org/bot{TOKEN}/sendMessage` 한 줄만 호출
- 검증 단계에 `grep -rE 'getUpdates|polling' src/` → 0건이어야 통과 조건으로 박아둠 (혹시 미래에 라이브러리 재도입할 때 차단)

```ts
// telegram.ts 전체 (~25줄)
export async function sendMessage(token, chatId, text) {
  const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text, disable_web_page_preview: true }),
  });
  const json = await res.json();
  if (!json.ok) throw new Error(`Telegram API: ${json.description}`);
}
```

이게 끝. polling 도구함을 안 들이는 게 곧 충돌 회피다.

## 같은 데이터, 다른 형식 — 4개 템플릿 등록

매번 같은 형식(이모지 헤더 + 정렬된 섹션)으로만 오면 시각적으로 단조로워진다. 같은 내용도 형식이 바뀌면 새롭게 읽힌다. 그래서 포맷터를 단일 함수 → **인덱스 → 변형명 → 함수** 의 nested 레지스트리로 바꿨다.

```ts
const formatters: Record<string, Record<string, FormatterFn>> = {
  'ethics-claims': {
    v1_emoji:    formatEthicsClaim_v1Emoji,    // 🏛/📌/💡/📚/🔄/🔑
    v2_minimal:  formatEthicsClaim_v2Minimal,  // [헤더] / ▶ / —
    v3_question: formatEthicsClaim_v3Question, // 🤔 오늘의 질문 / ❓/🔍/⚠️
    v4_dialog:   formatEthicsClaim_v4Dialog,   // 💬 대화체 / 📖/💭/🌀
  },
};
```

활성 변형은 환경변수 1줄로 결정:

```
FORMATTER_VARIANT=v1_emoji   # 또는 v2_minimal / v3_question / v4_dialog
```

지금은 `v1_emoji` 만 쓰고 나머지는 등록만. 운영하다 질리면 .env 에서 한 글자 바꾸고 다음 정시부터 새 형식. 재빌드 불필요.

같은 doc(밀의 자유론)을 4개 변형으로 dry-run 한 결과를 비교해 보면 — 정보는 100% 동일한데 v3_question 은 "오늘의 윤리 질문"으로 시작해 시험 문제 톤이고, v4_dialog 는 "오늘은 OO 이야기예요" 로 시작해 친구가 설명해주는 톤이다. 같은 내용을 머리에 다른 모양으로 박아넣는 효과를 노린 것.

## selector + dedup — 짧은 SQLite 설계

매시간 발송할 때 **최근 14일 안에 보낸 doc 은 다시 안 보내기**. 387건 풀에 14일 × 10회 = 140회 발송이니, 풀이 충분히 크다.

스키마는 한 테이블:

```sql
CREATE TABLE sent_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  es_index TEXT NOT NULL,
  doc_id TEXT NOT NULL,
  recipient TEXT NOT NULL,
  sent_at INTEGER NOT NULL,           -- ms epoch
  message_preview TEXT
);
CREATE INDEX idx_sent_log_index_time ON sent_log(es_index, sent_at);
CREATE INDEX idx_sent_log_doc ON sent_log(es_index, doc_id);
```

selector 알고리즘:

1. `SELECTOR_WEIGHTS` env 에서 가중치 비례로 인덱스 선택 (현재는 `ethics-claims:100` 하나)
2. ES 에서 `verified=true` 필터로 후보 id 풀 가져오기 (387건)
3. SQLite 에서 `sent_at >= now - 14d` 인 doc_id 들 빼기 (`getRecentlySent`)
4. 남은 후보 ≥1 → 무작위 1건 반환
5. 후보 0 (= 풀 전체가 14일 내 발송됨, 매우 드문 케이스) → `getOldestSent` 로 가장 오래전 보낸 doc 다시 (`fallback=true` 표시 + warn)

5단계 fallback 은 보험. 387건 풀에 140회/14일이라 정상 동작 중에는 발생할 일이 거의 없다. 하지만 만약 미래에 인덱스를 좁히거나 dedup 기간을 늘려서 풀이 고갈되면 조용히 멈추지 말고 가장 옛날 것이라도 보내고 stderr 에 경고를 남기는 게 학습 흐름을 안 끊는 길이다.

dedup 동작 검증은 dry-run 단계에서 강제로 좁혀서 확인했다 — `DEDUP_DAYS=365` 로 임시 설정 후 send-once 2번:

```
1  spinoza-claim-002  2026-04-28 11:59:46
2  rawls-claim-002    2026-04-28 12:00:00
```

다른 doc 이 선택됨을 확인. .env 의 14일은 그대로 유지(런타임 override 만 사용).

## systemd user timer — cron 의 깔끔한 대체

cron 도 가능하지만 systemd user timer 가 다음 점이 좋다:

- **실행 결과가 journal 에 자동 누적**: `journalctl --user -u ethics-pulse.service` 한 줄로 과거 발송 모두 추적
- **`Persistent=true`** 옵션: 컴퓨터가 꺼져 있어서 trigger 시각을 놓쳤어도 켜자마자 한 번 실행 (cron 은 그냥 놓침)
- **`OnCalendar`** 표현식이 cron 보다 읽기 쉬움
- **사용자 단위로 격리**: root 권한 불필요, `~/.config/systemd/user/` 에서 본인 것만 관리

unit 2개:

```ini
# ethics-pulse.service
[Service]
Type=oneshot
WorkingDirectory=/home/jai/ai-agent/projects/ethics-pulse
EnvironmentFile=/home/jai/ai-agent/projects/ethics-pulse/.env
ExecStart=/usr/bin/node dist/index.js
StandardOutput=journal
StandardError=journal
```

```ini
# ethics-pulse.timer
[Timer]
OnCalendar=*-*-* 09..18:00:00 Asia/Seoul
Persistent=true
WakeSystem=false
Unit=ethics-pulse.service

[Install]
WantedBy=timers.target
```

`OnCalendar=*-*-* 09..18:00:00 Asia/Seoul` 이 정확히 09·10·…·18시 정각 10회/일을 의미한다는 건 `systemd-analyze calendar "..." --iterations 12` 로 미리 시뮬레이션해서 확인 (`18` inclusive). 한국에서 systemd 쓸 때 timezone 명시 안 하면 기본 UTC 라 특히 함정.

설치는 install-systemd.sh 가 `~/.config/systemd/user/` 에 심볼릭 링크 + `daemon-reload` + `enable --now`. 코드 수정 후 unit 만 바뀌면 `daemon-reload` 만 다시.

## 검증 흐름 — dry-run / send-once / 본 가동

3단계로 나눈 게 안전판이 됐다:

| 명령 | 동작 | 외부 영향 |
|------|------|-----------|
| `npm run dry-run` | ES 선택 + 포맷 + stdout 출력 | 없음 (history 미기록, 텔레그램 미발송) |
| `npm run send-once` | dry-run + 실제 텔레그램 발송 + history 기록 | 텔레그램 1건 |
| `bash scripts/install-systemd.sh` | timer 활성화 | 다음 정시부터 자동 발송 시작 |

dry-run 단계에서 4개 포맷터 변형을 모두 돌려서 같은 doc 이 시각적으로 어떻게 다른지 확인했고, send-once 단계에서 텔레그램에 실제로 도착하는 모양과 history.db 기록을 사람 눈으로 검증한 뒤에야 systemd 를 켰다. 한 번에 다 켜지 않고 미리보기 → 1회 실험 → 본 가동 의 3단 검증은 비교적 작은 자동화에서도 가치가 컸다.

## 이번에 좋았던 점

1. **마이크로서비스 분리 결정**. nanoclaw 에 끼워넣었으면 코드는 짧았겠지만, 추후 포맷 실험 / 인덱스 확장 / 시각 변경마다 다른 코드와 같이 빌드해야 했을 것. 분리한 덕분에 .env 변수 1개 변경으로 즉시 실험 가능.
2. **polling 충돌을 코드 작성 전에 짚은 것**. 만약 grammy 깔고 시작했다가 nanoclaw 봇이 죽었다면, 디버깅하는 데 한참 걸렸을 것. 합의 단계에서 위험을 명시하고 검증 기준에 grep 까지 박아둠.
3. **포맷터 nested 레지스트리**. 처음엔 `Record<index, fn>` 단일 dispatch 였는데, "변형 등록만 해두자" 요청이 들어왔을 때 `Record<index, Record<variant, fn>>` 로 한 단계 깊이만 더해서 끝남. 미래에 인덱스를 추가해도 같은 패턴.

## 다음 할 일

- **인덱스 확장**: 현재 `ethics-claims` 만. 사상가 카드(`ethics-thinkers`), 단원 주제 카드(`ethics-topics`), 사상가 간 영향 관계(`ethics-relations`) 를 가중치로 섞기. 환경변수 한 줄: `SELECTOR_WEIGHTS=ethics-claims:70,ethics-thinkers:15,ethics-topics:15`.
- **기출 해설 인덱스 신규 적재**: 현재 `ethics-topics` 의 `exam_appearances` 필드가 기출 연결만 가지고 있고 해설 본문은 별도 마크다운 파일에 있음. 이걸 `ethics-exam-solutions` 인덱스로 따로 ES 에 적재하면 ethics-pulse 코드는 formatter 1개 추가만으로 자동 발송 대상에 포함.
- **포맷 실험**: 14일 운영해보면서 어떤 변형이 머리에 잘 박히는지 감 잡기. 그 후 가중치 분산 또는 시간대별 변형 분리 (예: 점심 = v3_question, 저녁 = v4_dialog).

코드는 짧지만 **봇 토큰의 polling 1개 제한** 같은 비자명한 시스템 사실은 한 번 명문화해두면 다음 비슷한 자동화에서 같은 지뢰를 안 밟는다. 이번 회고를 쓴 이유의 절반은 그 사실 자체이고, 나머지 절반은 작은 자동화도 분리·검증·확장 포인트를 미리 박아두는 습관이 결국 이득이라는 확인.
