"use client";

/**
 * FilterConfigBuilder — signal filter (필터) 다중 선택 + 파라미터 입력 위젯.
 *
 * UI/UX 원칙 1·2 강제 — 사용자에게 raw JSON 입력을 요구하지 않고
 * 필터 종류 드롭다운 → params_schema 기반 폼(StrategyParamsForm 재사용)
 * 으로 구성한다.
 *
 * 백엔드 계약: BacktestCreate.strategy.filter_configs 는
 * `[{name: str, params: dict}, ...]` (FilterConfigSchema). 다중 필터는
 * AND 결합 (Quant Lab CLAUDE.md §2 + architecture.md V3 § "전략 조합").
 *
 * 컨트롤드 컴포넌트 — 부모(NewBacktestPage)가 value/onChange 보유.
 */
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import type { FilterConfig, StrategyDescriptor } from "@/lib/api/schemas";
import { ko } from "@/lib/i18n/ko";

import { StrategyParamsForm } from "./StrategyParamsForm";

interface Props {
  availableFilters: StrategyDescriptor[];
  value: FilterConfig[];
  onChange: (next: FilterConfig[]) => void;
}

/**
 * 필터의 params_schema 에서 default 값을 추출해 초기 params 객체를
 * 만든다. 백엔드 pydantic 이 default 를 보유한 필드는 미입력해도
 * 통과하지만, UI 상에서 사용자가 어떤 값으로 시작했는지 보이게 하려면
 * 미리 채워두는 편이 친절하다.
 */
function buildDefaultParams(schema: StrategyDescriptor["params_schema"]): Record<string, unknown> {
  const properties = (schema?.properties ?? {}) as Record<
    string,
    { default?: unknown }
  >;
  const next: Record<string, unknown> = {};
  for (const [key, def] of Object.entries(properties)) {
    if (def?.default !== undefined) {
      next[key] = def.default;
    }
  }
  return next;
}

export function FilterConfigBuilder({
  availableFilters,
  value,
  onChange,
}: Props) {
  const [adding, setAdding] = useState(false);
  const [pendingName, setPendingName] = useState("");

  function addFilter() {
    if (!pendingName) return;
    const desc = availableFilters.find((f) => f.name === pendingName);
    if (!desc) return;
    const defaults = buildDefaultParams(desc.params_schema);
    onChange([...value, { name: pendingName, params: defaults }]);
    setPendingName("");
    setAdding(false);
  }

  function updateFilterParams(idx: number, params: Record<string, unknown>) {
    onChange(value.map((f, i) => (i === idx ? { ...f, params } : f)));
  }

  function removeFilter(idx: number) {
    onChange(value.filter((_, i) => i !== idx));
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-600">
          시그널 필터
          {value.length > 0 && ` (${value.length}${ko.filter.andCombined})`}
        </span>
        {!adding && (
          <Button
            type="button"
            size="sm"
            variant="ghost"
            onClick={() => setAdding(true)}
            disabled={availableFilters.length === 0}
          >
            {ko.filter.add}
          </Button>
        )}
      </div>

      {value.length > 0 && (
        <div className="space-y-2">
          {value.map((fc, idx) => {
            const desc = availableFilters.find((f) => f.name === fc.name);
            return (
              <Card key={`${fc.name}_${idx}`} className="border-gray-200">
                <CardContent className="space-y-2 p-3 pt-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold">
                      {desc?.description ?? fc.name}
                    </span>
                    <Button
                      type="button"
                      size="sm"
                      variant="ghost"
                      onClick={() => removeFilter(idx)}
                    >
                      {ko.filter.remove}
                    </Button>
                  </div>
                  {desc ? (
                    <StrategyParamsForm
                      schema={desc.params_schema}
                      value={fc.params}
                      onChange={(params) => updateFilterParams(idx, params)}
                    />
                  ) : (
                    <p className="text-xs text-amber-700">
                      알 수 없는 필터 종류 ({fc.name}). 백엔드 전략 등록을
                      확인하세요.
                    </p>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {adding && (
        <Card className="border-blue-200 bg-blue-50">
          <CardContent className="space-y-2 p-3 pt-3">
            <Label htmlFor="filter_pending_name">추가할 필터 선택</Label>
            <Select
              id="filter_pending_name"
              value={pendingName}
              onChange={(e) => setPendingName(e.target.value)}
            >
              <option value="">선택하세요</option>
              {availableFilters.map((f) => (
                <option key={f.name} value={f.name}>
                  {f.description ?? f.name}
                </option>
              ))}
            </Select>
            <div className="flex justify-end gap-2">
              <Button
                type="button"
                size="sm"
                variant="ghost"
                onClick={() => {
                  setAdding(false);
                  setPendingName("");
                }}
              >
                취소
              </Button>
              <Button
                type="button"
                size="sm"
                onClick={addFilter}
                disabled={!pendingName}
              >
                추가
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {value.length === 0 && !adding && (
        <p className="text-xs text-gray-500">{ko.filter.noFilters}</p>
      )}
    </div>
  );
}
