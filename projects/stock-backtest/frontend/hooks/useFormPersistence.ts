"use client";

/**
 * useFormPersistence — TASK-218 폼 값 localStorage 영속화 훅.
 *
 * 책임 1개: 임의 형태의 폼 state object 를 localStorage 에 디바운스 저장하고,
 * 마운트 시 1회 복원한다. /backtests/new 가 화면 전환 없이 in-place 결과를
 * 표시하는 흐름에서 (TASK-218) 사용자가 새로고침 / 탭 닫기를 해도 직전
 * 입력값이 살아 있도록 한다.
 *
 * 클린 아키텍처:
 *   - presentation 레이어 (`/backtests/new` page.tsx) 가 사용. domain/data
 *     로 import 되지 않는다.
 *   - localStorage 의 직렬화 / 버전 마이그레이션 / debounce 같은 reactive
 *     로직을 page.tsx 에서 떼어내, page.tsx 는 폼 상태와 렌더만 책임진다
 *     (Single Responsibility — coder.md L52).
 *
 * 버전 관리:
 *   - 키 접두사에 `:v1` 같은 버전을 포함해서 저장한다 (호출부에서 결정).
 *   - 복원 시 저장된 데이터의 `__version` 필드를 읽고, 일치하지 않으면
 *     null 반환 (= initialValue 사용). 사일런트 호환 깨짐을 방지.
 *
 * SSR 안전:
 *   - 첫 render 는 항상 initialValue. 그 다음 effect 에서 localStorage 읽음.
 *   - hydration mismatch 방지: 서버와 첫 클라이언트 render 가 같아야 한다.
 */
import { useCallback, useEffect, useRef, useState } from "react";

const SAVE_DEBOUNCE_MS = 500;

export interface UseFormPersistenceOptions<T> {
  /** localStorage 키. 호출부가 버전을 포함시킨다 (예: "backtest:last_form_state:v1"). */
  storageKey: string;
  /** SSR / 첫 마운트 시 반환할 초기값. localStorage 복원이 완료되면 setValue 로 덮어씀. */
  initialValue: T;
  /**
   * Schema 버전. 저장 시 `__version` 필드로 같이 직렬화된다. 복원 시 다른
   * 버전이면 무시 (null 처리) → initialValue 유지. 하위호환 마이그레이션이
   * 필요할 때 호출부가 `migrate` 옵션 제공.
   */
  version: number;
  /**
   * 선택. 복원된 데이터의 버전이 현재 `version` 과 다를 때 호출. 마이그레이션이
   * 가능하면 새 모양 T 를 반환, 불가능하면 null 반환 → initialValue 사용.
   */
  migrate?: (raw: unknown, fromVersion: number) => T | null;
  /** 디바운스(ms). 기본 500. */
  debounceMs?: number;
}

interface PersistedShape<T> {
  __version: number;
  data: T;
}

/**
 * 반환:
 *   [value, setValue, hydrated, clear]
 *     - value: 현재 값 (마운트 직후 = initialValue, 복원 후 = stored)
 *     - setValue: useState 와 동일 시그니처 (값 또는 updater 함수)
 *     - hydrated: localStorage 복원 시도가 완료됐는지 (true 이후 setValue 가
 *       자동 저장 트리거). 첫 render 에 false 로 깜빡이는 동안의 setValue 는
 *       복원 race 와 충돌하지 않게 저장 skip.
 *     - clear: 저장된 값을 지우고 state 를 initialValue 로 되돌린다.
 */
export function useFormPersistence<T>(
  options: UseFormPersistenceOptions<T>,
): [T, (next: T | ((prev: T) => T)) => void, boolean, () => void] {
  const { storageKey, initialValue, version, migrate, debounceMs } = options;
  const debounce = debounceMs ?? SAVE_DEBOUNCE_MS;

  const [value, setValueState] = useState<T>(initialValue);
  const [hydrated, setHydrated] = useState(false);

  // 마운트 시 1회 복원. SSR 환경에서 window 가 없을 수 있어 typeof 체크.
  useEffect(() => {
    if (typeof window === "undefined") {
      setHydrated(true);
      return;
    }
    try {
      const raw = window.localStorage.getItem(storageKey);
      if (raw !== null) {
        const parsed = JSON.parse(raw) as unknown;
        const restored = readPersisted<T>(parsed, version, migrate);
        if (restored !== null) {
          setValueState(restored);
        }
      }
    } catch {
      // 읽기/파싱 실패는 silent — initialValue 유지. localStorage 가 quota /
      // 권한 문제로 막혀 있어도 폼은 동작해야 한다.
    } finally {
      setHydrated(true);
    }
  }, [storageKey, version, migrate]);

  // value 변경 → debounce 후 저장. hydrated 전에는 저장하지 않는다 (초기
  // initialValue 가 stored 를 덮어쓰는 사고 방지).
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => {
    if (!hydrated) return;
    if (typeof window === "undefined") return;
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => {
      try {
        const payload: PersistedShape<T> = { __version: version, data: value };
        window.localStorage.setItem(storageKey, JSON.stringify(payload));
      } catch {
        // quota/권한 실패 silent. 사용자 작업이 막히지 않게.
      }
    }, debounce);
    return () => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [value, hydrated, storageKey, version, debounce]);

  const setValue = useCallback((next: T | ((prev: T) => T)) => {
    setValueState(next);
  }, []);

  const clear = useCallback(() => {
    if (typeof window !== "undefined") {
      try {
        window.localStorage.removeItem(storageKey);
      } catch {
        // silent
      }
    }
    setValueState(initialValue);
  }, [storageKey, initialValue]);

  return [value, setValue, hydrated, clear];
}

/**
 * 저장된 raw 객체를 검증하고 T 로 narrow.
 * - 신호: `{ __version: number, data: ... }` 모양이어야 한다.
 * - 버전 일치: `data` 그대로 반환.
 * - 버전 불일치 + migrate 제공: migrate 호출.
 * - 버전 불일치 + migrate 없음: null.
 * - 모양 불일치: null.
 */
function readPersisted<T>(
  raw: unknown,
  currentVersion: number,
  migrate?: (raw: unknown, fromVersion: number) => T | null,
): T | null {
  if (raw === null || typeof raw !== "object") return null;
  const obj = raw as Record<string, unknown>;
  const ver = typeof obj.__version === "number" ? obj.__version : null;
  if (ver === null) return null;
  if (ver === currentVersion) {
    // 형태 검증은 호출부 책임 (initialValue 와 같은 shape 가정).
    return obj.data as T;
  }
  if (migrate) {
    return migrate(obj.data, ver);
  }
  return null;
}
