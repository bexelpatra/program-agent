/**
 * useFormPersistence — 단위 테스트 (TASK-218 DoD).
 *
 * 검증 영역:
 *   1. save: setValue 후 debounce ms 경과 시 localStorage 에 적재.
 *   2. restore: 마운트 시 stored payload 가 있으면 initialValue 대신 채택.
 *   3. version migration: 저장된 __version 이 현재 버전과 다르면 무시 (또는
 *      migrate 콜백 결과 채택).
 *   4. clear: storage key 제거 + state 를 initialValue 로 복귀.
 *
 * 비동기 정리: vitest fake timers + act() 로 debounce ms 를 flush.
 */
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { renderHook, act } from "@testing-library/react";

import { useFormPersistence } from "@/hooks/useFormPersistence";

interface FormShape {
  universe_asset_ids: number[];
  allocator_name: string;
  initial_cash: Record<string, number>;
}

const KEY = "test:form:v1";

const initial: FormShape = {
  universe_asset_ids: [],
  allocator_name: "",
  initial_cash: {},
};

describe("useFormPersistence", () => {
  beforeEach(() => {
    window.localStorage.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("save: setValue 후 debounce ms 경과 시 localStorage 에 직렬화 저장", () => {
    const { result } = renderHook(() =>
      useFormPersistence<FormShape>({
        storageKey: KEY,
        initialValue: initial,
        version: 1,
        debounceMs: 100,
      }),
    );

    // 마운트 직후엔 initialValue 그대로, hydrated true (stored 없음)
    expect(result.current[0]).toEqual(initial);
    expect(result.current[2]).toBe(true);
    expect(window.localStorage.getItem(KEY)).toBeNull();

    act(() => {
      result.current[1]({
        universe_asset_ids: [10, 20],
        allocator_name: "fixed_weight",
        initial_cash: { KRW: 1_000_000 },
      });
    });

    // debounce 미경과 — 아직 저장 안 됨
    expect(window.localStorage.getItem(KEY)).toBeNull();

    act(() => {
      vi.advanceTimersByTime(150);
    });

    const raw = window.localStorage.getItem(KEY);
    expect(raw).not.toBeNull();
    const parsed = JSON.parse(raw as string);
    expect(parsed.__version).toBe(1);
    expect(parsed.data).toEqual({
      universe_asset_ids: [10, 20],
      allocator_name: "fixed_weight",
      initial_cash: { KRW: 1_000_000 },
    });
  });

  it("restore: 마운트 시 동일 버전 stored 를 채택", () => {
    window.localStorage.setItem(
      KEY,
      JSON.stringify({
        __version: 1,
        data: {
          universe_asset_ids: [42],
          allocator_name: "all_weather",
          initial_cash: { USD: 50_000 },
        },
      }),
    );

    const { result } = renderHook(() =>
      useFormPersistence<FormShape>({
        storageKey: KEY,
        initialValue: initial,
        version: 1,
        debounceMs: 100,
      }),
    );

    expect(result.current[0]).toEqual({
      universe_asset_ids: [42],
      allocator_name: "all_weather",
      initial_cash: { USD: 50_000 },
    });
    expect(result.current[2]).toBe(true);
  });

  it("version mismatch: migrate 미제공 시 stored 무시 → initialValue 유지", () => {
    window.localStorage.setItem(
      KEY,
      JSON.stringify({
        __version: 0, // 다른 버전
        data: { foo: "bar" },
      }),
    );

    const { result } = renderHook(() =>
      useFormPersistence<FormShape>({
        storageKey: KEY,
        initialValue: initial,
        version: 1,
        debounceMs: 100,
      }),
    );

    expect(result.current[0]).toEqual(initial);
  });

  it("version mismatch: migrate 제공 시 마이그레이션 결과 채택", () => {
    window.localStorage.setItem(
      KEY,
      JSON.stringify({
        __version: 0,
        data: { ids: [99], name: "legacy", cash: { KRW: 7 } },
      }),
    );

    const migrate = vi.fn((raw: unknown, fromVersion: number): FormShape => {
      const o = raw as Record<string, unknown>;
      return {
        universe_asset_ids: o.ids as number[],
        allocator_name: o.name as string,
        initial_cash: o.cash as Record<string, number>,
      };
    });

    const { result } = renderHook(() =>
      useFormPersistence<FormShape>({
        storageKey: KEY,
        initialValue: initial,
        version: 1,
        migrate,
        debounceMs: 100,
      }),
    );

    expect(migrate).toHaveBeenCalledWith(
      { ids: [99], name: "legacy", cash: { KRW: 7 } },
      0,
    );
    expect(result.current[0]).toEqual({
      universe_asset_ids: [99],
      allocator_name: "legacy",
      initial_cash: { KRW: 7 },
    });
  });

  it("clear: storage key 제거 + state initialValue 복귀", () => {
    const { result } = renderHook(() =>
      useFormPersistence<FormShape>({
        storageKey: KEY,
        initialValue: initial,
        version: 1,
        debounceMs: 100,
      }),
    );

    act(() => {
      result.current[1]({
        universe_asset_ids: [1, 2],
        allocator_name: "equal_weight",
        initial_cash: { KRW: 999 },
      });
    });
    act(() => {
      vi.advanceTimersByTime(150);
    });
    expect(window.localStorage.getItem(KEY)).not.toBeNull();

    act(() => {
      result.current[3](); // clear
    });

    expect(window.localStorage.getItem(KEY)).toBeNull();
    expect(result.current[0]).toEqual(initial);
  });

  it("malformed JSON: silent fallback to initialValue", () => {
    window.localStorage.setItem(KEY, "{not valid json");

    const { result } = renderHook(() =>
      useFormPersistence<FormShape>({
        storageKey: KEY,
        initialValue: initial,
        version: 1,
        debounceMs: 100,
      }),
    );

    expect(result.current[0]).toEqual(initial);
    expect(result.current[2]).toBe(true);
  });
});
