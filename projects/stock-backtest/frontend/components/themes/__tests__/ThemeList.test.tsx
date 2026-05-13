/**
 * ThemeList — 단위 테스트 (TASK-307 DoD #1).
 *
 * 검증 영역:
 *   1. items 가 비어있으면 안내 문구 (`theme.list.empty`) 렌더.
 *   2. items 가 N 개면 카드 N 개 + 멤버 카운트 배지 + 카드 클릭 라우팅용
 *      `<Link href="/themes/{id}">` 존재.
 *   3. 편집/삭제 버튼 클릭 시 onEdit/onDelete 콜백이 해당 theme 객체로
 *      호출된다 (이벤트 버블링이 Link 라우팅을 trigger 하지 않는지 확인 —
 *      stopPropagation 은 Button 의 기본 동작에 의존하지 않으므로 별도
 *      assertion).
 *
 * Next `Link` 는 jsdom 에서 `<a href>` 로 풀려 렌더되므로, 라우팅 검증은
 * href 속성 확인으로 충분 (실제 navigation 은 next/router mock 없이는
 * 일어나지 않음).
 */
import { describe, it, expect, vi, afterEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";

afterEach(() => {
  cleanup();
});

import { ThemeList } from "@/components/themes/ThemeList";
import type { Theme } from "@/lib/api/types";

const fixture: Theme[] = [
  {
    theme_id: 1,
    name: "정치 테마주",
    slug: "politics",
    description: "한국 정치 사이클 민감주",
    user_id: "local",
    created_at: "2026-05-12T10:00:00Z",
    member_count: 7,
  },
  {
    theme_id: 2,
    name: "반도체 장비",
    slug: "semicon",
    description: null,
    user_id: "local",
    created_at: "2026-05-10T09:00:00Z",
    member_count: 3,
  },
];

describe("ThemeList", () => {
  it("items 비어있으면 empty hint 렌더", () => {
    render(<ThemeList items={[]} onEdit={() => {}} onDelete={() => {}} />);
    expect(screen.getByTestId("theme-list-empty")).toBeTruthy();
  });

  it("items N 개 → 카드 N 개 + 멤버 카운트 + 라우팅 href 존재", () => {
    render(
      <ThemeList items={fixture} onEdit={() => {}} onDelete={() => {}} />,
    );

    expect(screen.getByTestId("theme-card-1")).toBeTruthy();
    expect(screen.getByTestId("theme-card-2")).toBeTruthy();

    const link1 = screen.getByTestId("theme-card-link-1") as HTMLAnchorElement;
    expect(link1.getAttribute("href")).toBe("/themes/1");
    const link2 = screen.getByTestId("theme-card-link-2") as HTMLAnchorElement;
    expect(link2.getAttribute("href")).toBe("/themes/2");

    // 멤버 카운트 라벨 — "7 종목" / "3 종목"
    expect(screen.getByText(/7\s+종목/)).toBeTruthy();
    expect(screen.getByText(/3\s+종목/)).toBeTruthy();
  });

  it("편집/삭제 버튼 클릭 시 콜백이 해당 theme 으로 호출", () => {
    const onEdit = vi.fn();
    const onDelete = vi.fn();
    render(
      <ThemeList items={fixture} onEdit={onEdit} onDelete={onDelete} />,
    );

    fireEvent.click(screen.getByTestId("theme-card-edit-1"));
    expect(onEdit).toHaveBeenCalledTimes(1);
    expect(onEdit.mock.calls[0][0]).toMatchObject({
      theme_id: 1,
      name: "정치 테마주",
    });

    fireEvent.click(screen.getByTestId("theme-card-delete-2"));
    expect(onDelete).toHaveBeenCalledTimes(1);
    expect(onDelete.mock.calls[0][0]).toMatchObject({
      theme_id: 2,
      name: "반도체 장비",
    });
  });
});
