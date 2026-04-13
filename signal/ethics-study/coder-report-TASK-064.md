# Coder Report — TASK-064

- **Task**: 순자 데이터 이슈 수정 (검증 결과 반영)
- **Status**: DONE
- **Timestamp**: 2026-04-13

---

## 수행 내용

### 경미 이슈 4건 수정

| # | 위치 | 수정 전 | 수정 후 |
|---|------|---------|---------|
| 1 | thinker.name_en | "Xunzi (Hsün Tzu)" | "Xunzi" — Pinyin 단독 표기 |
| 2 | claim-009 source_detail | "순자 왕제편(王制篇), 성악편(性惡篇)" | "순자 성악편(性惡篇) — 예법병용(禮法竝用) 논의 부분, 왕제편(王制篇) 참조" |
| 3 | claim-011 argument | "형명(刑名)" + "刑名不正 則賞罰不當" | "형명(形名)" + "名不正 則賞罰不當" — 법가 용어 혼동 해소 |
| 4 | claim-008 source_detail | "순자 성악편(性惡篇), 권학편(勸學篇)" | "순자 성악편(性惡篇) — 군자·소인 논의 및 권학편(勸學篇) 적선성덕(積善成德) 관련" |

### verified 설정

- 11건 claims 전체 `verified: true` 설정 완료
- `verification_log`에 TASK-063 검증 결과 기록 추가

---

## 검증 결과

- thinker name_en: "Xunzi" (Wade-Giles 제거 확인)
- claim-011 argument: 刑名 → 形名 전환 완료 (0건 잔존)
- verified claims: 11/11 (ES refresh 후 확인)

---

## 변경 파일

- ES index `ethics-thinkers`: xunzi 문서 (name_en 필드)
- ES index `ethics-claims`: xunzi-claim-008, 009, 011 (source_detail/argument 필드)
- ES index `ethics-claims`: xunzi-claim-001~011 (verified, verification_log 필드)
