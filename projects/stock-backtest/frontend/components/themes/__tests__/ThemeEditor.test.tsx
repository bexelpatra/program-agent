/**
 * ThemeEditor — 단위 테스트 (TASK-307 DoD #2).
 *
 * 검증 영역:
 *   1. mode='create' + name 빈 값 → submit 시 한국어 에러 (nameRequired)
 *      가 표시되고 api.createTheme 는 호출되지 않는다.
 *   2. mode='create' + 정상 입력 → api.createTheme 가 trim 된 payload 로
 *      호출되고 onSaved + onOpenChange(false) 가 trigger 된다.
 *   3. mode='edit' + 정상 입력 → api.updateTheme 가 initial.theme_id 와
 *      payload 로 호출된다.
 *
 * api 모듈은 vi.mock 으로 부분 대체. toast 는 ToastProvider 래핑으로
 * 실제 hook 을 사용 (DOM 에 노출되지만 본 테스트의 assertion 대상은 아님).
 */
import { describe, it, expect, vi, afterEach, beforeEach } from "vitest";
import {
  render,
  screen,
  fireEvent,
  cleanup,
  waitFor,
} from "@testing-library/react";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

vi.mock("@/lib/api/client", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api/client")>(
    "@/lib/api/client",
  );
  return {
    ...actual,
    api: {
      createTheme: vi.fn(),
      updateTheme: vi.fn(),
    },
  };
});

import { api } from "@/lib/api/client";
import { ToastProvider } from "@/components/ui/toast";
import { ThemeEditor } from "@/components/themes/ThemeEditor";
import type { Theme } from "@/lib/api/types";

const initialTheme: Theme = {
  theme_id: 42,
  name: "원본",
  slug: "orig",
  description: "원본 설명",
  user_id: "local",
  created_at: "2026-05-01T00:00:00Z",
  member_count: 0,
};

function renderEditor(
  props: Partial<React.ComponentProps<typeof ThemeEditor>> = {},
) {
  const onOpenChange = vi.fn();
  const onSaved = vi.fn();
  const utils = render(
    <ToastProvider>
      <ThemeEditor
        open={true}
        mode="create"
        onOpenChange={onOpenChange}
        onSaved={onSaved}
        {...props}
      />
    </ToastProvider>,
  );
  return { ...utils, onOpenChange, onSaved };
}

describe("ThemeEditor", () => {
  beforeEach(() => {
    (api.createTheme as ReturnType<typeof vi.fn>).mockResolvedValue({
      theme_id: 1,
      name: "신규",
      slug: "new",
      description: null,
      user_id: "local",
      created_at: "2026-05-12T10:00:00Z",
    });
    (api.updateTheme as ReturnType<typeof vi.fn>).mockResolvedValue({
      ...initialTheme,
      name: "수정됨",
    });
  });

  it("create + name 빈 값 → 한국어 에러 표시 + createTheme 미호출", async () => {
    const { onSaved } = renderEditor();
    // 이름 미입력 상태로 저장 클릭
    fireEvent.click(screen.getByRole("button", { name: /^저장$/ }));

    expect(screen.getByRole("alert").textContent).toMatch(/필수/);
    expect(api.createTheme).not.toHaveBeenCalled();
    expect(onSaved).not.toHaveBeenCalled();
  });

  it("create + 정상 입력 → createTheme 호출 + onSaved + close", async () => {
    const { onSaved, onOpenChange } = renderEditor();

    const nameInput = screen.getByLabelText(/테마 이름/) as HTMLInputElement;
    fireEvent.change(nameInput, { target: { value: "  새 테마  " } });

    const descInput = screen.getByLabelText(/^설명$/) as HTMLInputElement;
    fireEvent.change(descInput, { target: { value: "테마 설명" } });

    fireEvent.click(screen.getByRole("button", { name: /^저장$/ }));

    await waitFor(() => {
      expect(api.createTheme).toHaveBeenCalledTimes(1);
    });
    expect(api.createTheme).toHaveBeenCalledWith({
      name: "새 테마",
      description: "테마 설명",
    });
    await waitFor(() => {
      expect(onSaved).toHaveBeenCalledTimes(1);
      expect(onOpenChange).toHaveBeenCalledWith(false);
    });
  });

  it("edit + 정상 입력 → updateTheme(themeId, payload) 호출", async () => {
    const { onSaved } = renderEditor({
      mode: "edit",
      initial: initialTheme,
    });

    const nameInput = screen.getByLabelText(/테마 이름/) as HTMLInputElement;
    expect(nameInput.value).toBe("원본");
    fireEvent.change(nameInput, { target: { value: "수정됨" } });

    fireEvent.click(screen.getByRole("button", { name: /^저장$/ }));

    await waitFor(() => {
      expect(api.updateTheme).toHaveBeenCalledTimes(1);
    });
    expect(api.updateTheme).toHaveBeenCalledWith(42, {
      name: "수정됨",
      description: "원본 설명",
    });
    await waitFor(() => {
      expect(onSaved).toHaveBeenCalledTimes(1);
    });
  });
});
