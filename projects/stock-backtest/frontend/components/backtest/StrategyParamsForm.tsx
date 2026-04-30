"use client";

/**
 * StrategyParamsForm — backend pydantic params_schema 를 React 폼으로
 * 자동 렌더.
 *
 * 각 top-level property 의 `type` 에 따라:
 *   - integer / number → 숫자 Input
 *   - string           → 텍스트 Input (enum 이면 Select)
 *   - boolean          → checkbox
 *   - object / array   → **부모가 주입한 complexFieldRenderer** 또는
 *                        "전용 위젯이 부모 화면에 표시됩니다" 안내.
 *                        절대 raw JSON textarea 를 노출하지 않는다.
 *
 * UI/UX 원칙 1 (JSON / 코드 노출 금지) 강제:
 *   사용자 첫 사용 시 FixedWeight.weights (`dict[int, float]`) 를
 *   임시로 JSON-string 입력으로 받았다가 ticker 키 입력 → 백엔드
 *   422 ValidationError 사고가 발생했다. 그 임시 우회는 영구 제거됐다.
 *   dict / array 파라미터는 반드시 전용 위젯(AssetWeightMap 등) 으로
 *   렌더해야 한다.
 *
 * 부모(예: NewBacktestPage) 가 `complexFieldRenderer` 를 주면 해당
 * 키에 대해 부모의 위젯을 그 자리에 끼워넣을 수 있다. 미주입 시에는
 * "부모 화면 다른 카드에서 입력" 안내 텍스트만 보여준다.
 */
import type { ReactNode } from "react";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import type {
  JsonSchemaObject,
  JsonSchemaProperty,
} from "@/lib/api/types";

export interface ComplexFieldRendererArgs {
  key: string;
  schema: JsonSchemaProperty;
  value: unknown;
  onChange: (next: unknown) => void;
  required: boolean;
}

interface Props {
  schema: JsonSchemaObject;
  value: Record<string, unknown>;
  onChange: (next: Record<string, unknown>) => void;
  /**
   * 부모가 dict/array 같은 복합 필드를 직접 렌더하고 싶을 때 주입.
   * `null` 을 반환하면 안내 메시지만 표시. 함수 자체가 없으면 안내만.
   */
  complexFieldRenderer?: (args: ComplexFieldRendererArgs) => ReactNode | null;
}

export function StrategyParamsForm({
  schema,
  value,
  onChange,
  complexFieldRenderer,
}: Props) {
  const properties = schema.properties ?? {};
  const required = new Set(schema.required ?? []);

  function update(key: string, next: unknown) {
    onChange({ ...value, [key]: next });
  }

  const entries = Object.entries(properties);

  if (entries.length === 0) {
    return (
      <p className="text-sm text-gray-500">이 전략은 추가 파라미터가 없습니다.</p>
    );
  }

  return (
    <div className="space-y-3">
      {entries.map(([key, def]) => {
        const fieldId = `param_${key}`;
        const label = def.title ?? key;
        const isRequired = required.has(key);
        const current = value[key] ?? def.default ?? "";

        // Enum scalar → Select.
        if (Array.isArray(def.enum) && def.enum.length > 0) {
          return (
            <FieldLabel
              key={key}
              id={fieldId}
              label={label}
              description={def.description}
              required={isRequired}
            >
              <Select
                id={fieldId}
                value={String(current)}
                onChange={(e) => update(key, e.target.value)}
              >
                {def.enum.map((opt) => (
                  <option key={String(opt)} value={String(opt)}>
                    {String(opt)}
                  </option>
                ))}
              </Select>
            </FieldLabel>
          );
        }

        if (def.type === "integer" || def.type === "number") {
          return (
            <FieldLabel
              key={key}
              id={fieldId}
              label={label}
              description={def.description}
              required={isRequired}
            >
              <Input
                id={fieldId}
                type="number"
                step={def.type === "integer" ? 1 : "any"}
                value={current === "" ? "" : Number(current)}
                onChange={(e) => {
                  const raw = e.target.value;
                  if (raw === "") {
                    update(key, "");
                    return;
                  }
                  update(
                    key,
                    def.type === "integer" ? parseInt(raw, 10) : parseFloat(raw),
                  );
                }}
              />
            </FieldLabel>
          );
        }

        if (def.type === "boolean") {
          const checked = Boolean(value[key] ?? def.default ?? false);
          return (
            <div key={key} className="flex items-center gap-2">
              <input
                id={fieldId}
                type="checkbox"
                checked={checked}
                onChange={(e) => update(key, e.target.checked)}
                className="h-4 w-4 rounded border-gray-300"
              />
              <Label htmlFor={fieldId}>
                {label}
                {isRequired && <span className="ml-1 text-red-600">*</span>}
                {def.description && (
                  <span className="ml-2 text-xs text-gray-500">
                    ({def.description})
                  </span>
                )}
              </Label>
            </div>
          );
        }

        if (def.type === "object" || def.type === "array") {
          // UI/UX 원칙 1 — JSON textarea 영구 금지.
          // 부모가 전용 위젯을 주입했으면 그 위젯을, 아니면 안내만.
          const rendered = complexFieldRenderer?.({
            key,
            schema: def,
            value: value[key],
            onChange: (next) => update(key, next),
            required: isRequired,
          });
          if (rendered !== undefined && rendered !== null) {
            return (
              <FieldLabel
                key={key}
                id={fieldId}
                label={label}
                description={def.description}
                required={isRequired}
              >
                {rendered}
              </FieldLabel>
            );
          }
          return (
            <FieldLabel
              key={key}
              id={fieldId}
              label={label}
              description={def.description}
              required={isRequired}
            >
              <p className="rounded border border-dashed border-gray-300 p-2 text-xs text-gray-600">
                이 파라미터({label})는 다른 카드의 전용 위젯에서 입력합니다.
              </p>
            </FieldLabel>
          );
        }

        // string + 기타 fallback.
        return (
          <FieldLabel
            key={key}
            id={fieldId}
            label={label}
            description={def.description}
            required={isRequired}
          >
            <Input
              id={fieldId}
              type="text"
              value={String(current)}
              onChange={(e) => update(key, e.target.value)}
            />
          </FieldLabel>
        );
      })}
    </div>
  );
}

interface FieldLabelProps {
  id: string;
  label: string;
  description?: string;
  required: boolean;
  children: React.ReactNode;
}

function FieldLabel({
  id,
  label,
  description,
  required,
  children,
}: FieldLabelProps) {
  return (
    <div>
      <Label htmlFor={id}>
        {label}
        {required && <span className="ml-1 text-red-600">*</span>}
        {description && (
          <span className="ml-2 text-xs text-gray-500">({description})</span>
        )}
      </Label>
      {children}
    </div>
  );
}
