"use client";

/**
 * ThemeList — 테마 카탈로그 목록 카드 (TASK-307).
 *
 * 카드 형태로 테마를 나열한다. 카드 본문 클릭 → `/themes/{theme_id}` 라우팅
 * (TASK-308 의 상세 화면). 편집/삭제 버튼은 카드 우측 footer 에 노출하고,
 * 부모 페이지에서 `onEdit`/`onDelete` 콜백으로 다이얼로그 토글을 처리한다.
 *
 * Pure presentational — fetch/state 는 부모 (themes/page.tsx) 가 보유.
 *
 * UI/UX 원칙 2: 빈 카탈로그는 안내 + 액션 가이드. 멤버 카운트는
 * "{count}개 종목" 한국어 라벨.
 */
import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ko } from "@/lib/i18n/ko";
import type { Theme } from "@/lib/api/types";

interface Props {
  items: Theme[];
  onEdit: (theme: Theme) => void;
  onDelete: (theme: Theme) => void;
}

function formatDate(iso: string): string {
  // 백엔드는 ISO datetime 문자열 (e.g. "2026-05-12T10:30:00Z"). 한국어
  // 로케일 short date 만 표시 (시각은 카드 UI 에서 노이즈).
  try {
    return new Date(iso).toLocaleDateString("ko-KR");
  } catch {
    return iso.slice(0, 10);
  }
}

export function ThemeList({ items, onEdit, onDelete }: Props) {
  if (items.length === 0) {
    return (
      <div
        className="rounded-lg border border-dashed border-gray-300 bg-white p-12 text-center"
        data-testid="theme-list-empty"
      >
        <p className="text-gray-600">{ko.theme.list.empty}</p>
      </div>
    );
  }

  return (
    <div
      className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
      data-testid="theme-list-grid"
    >
      {items.map((theme) => (
        <div
          key={theme.theme_id}
          data-testid={`theme-card-${theme.theme_id}`}
          className="flex flex-col rounded-lg border border-gray-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
        >
          <Link
            href={`/themes/${theme.theme_id}`}
            className="flex-1 space-y-2"
            data-testid={`theme-card-link-${theme.theme_id}`}
          >
            <div className="flex items-start justify-between gap-2">
              <h3 className="text-lg font-semibold text-gray-900">
                {theme.name}
              </h3>
              <Badge variant="secondary">
                {(theme.member_count ?? 0).toLocaleString("ko-KR")}{" "}
                {ko.theme.list.memberCount}
              </Badge>
            </div>
            <p className="text-sm text-gray-600 line-clamp-2 min-h-[2.5rem]">
              {theme.description?.trim() || ko.theme.list.noDescription}
            </p>
            <p className="text-xs text-gray-500">
              {ko.theme.list.createdAt}: {formatDate(theme.created_at)}
            </p>
          </Link>

          <div className="mt-4 flex justify-end gap-2 border-t border-gray-100 pt-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(theme)}
              data-testid={`theme-card-edit-${theme.theme_id}`}
            >
              {ko.theme.edit.action}
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(theme)}
              data-testid={`theme-card-delete-${theme.theme_id}`}
              className="text-red-600 hover:bg-red-50"
            >
              {ko.theme.delete.action}
            </Button>
          </div>
        </div>
      ))}
    </div>
  );
}
