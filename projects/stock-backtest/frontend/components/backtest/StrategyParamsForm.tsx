"use client";

/**
 * StrategyParamsForm — JSON Schema (pydantic export) → React form.
 *
 * Each backend allocator/filter ships its `params_schema` (TASK-061
 * StrategyDescriptor.params_schema) as a JSON Schema object. We render
 * each top-level property as a labelled input based on its `type`:
 *
 *   - integer / number → numeric Input
 *   - string           → text Input (with optional enum → Select)
 *   - boolean          → checkbox
 *   - object / array   → temporary JSON-string Input (see caveat below)
 *
 * UI/UX 원칙 1 (JSON 노출 금지) — 단순 scalar 필드는 모두 폼 입력으로
 * 노출. 단, allocator 가 dict 파라미터 (FixedWeight 의 weights:
 * {asset_id → weight}) 를 요구하면 전용 위젯이 생기기 전까지 임시로
 * JSON-string 입력을 허용한다. coder-report 의 "다음 제안" 에
 * AssetWeightMap 위젯 발주 항목을 남긴다.
 */
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";

interface JsonSchemaProperty {
  type?: string;
  title?: string;
  description?: string;
  default?: unknown;
  enum?: unknown[];
  // pydantic v2 puts inner schemas under `items` for arrays;
  // we don't dig deeper at MVP — array fields fall back to JSON input.
}

interface JsonSchemaObject {
  type?: string;
  properties?: Record<string, JsonSchemaProperty>;
  required?: string[];
}

interface Props {
  schema: JsonSchemaObject;
  value: Record<string, unknown>;
  onChange: (next: Record<string, unknown>) => void;
}

function isPlainObject(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

export function StrategyParamsForm({ schema, value, onChange }: Props) {
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
          // 임시 JSON 입력 — 전용 위젯이 생길 때까지의 우회.
          // UI/UX 원칙 1 위반이지만 placeholder 로 의도 노출 + report observation.
          const display = isPlainObject(value[key]) || Array.isArray(value[key])
            ? JSON.stringify(value[key])
            : String(value[key] ?? "");
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
                placeholder={
                  def.type === "object"
                    ? '예: {"1": 0.6, "2": 0.4}'
                    : '예: ["1", "2"]'
                }
                value={display}
                onChange={(e) => {
                  const raw = e.target.value;
                  if (raw === "") {
                    update(key, def.type === "object" ? {} : []);
                    return;
                  }
                  try {
                    update(key, JSON.parse(raw));
                  } catch {
                    // Keep the raw string as-is until it parses; avoids
                    // wiping the user's keystrokes mid-edit.
                    update(key, raw);
                  }
                }}
              />
              <p className="mt-1 text-xs text-amber-700">
                전용 입력 위젯이 곧 추가됩니다. 임시로 JSON 형식을
                입력하세요.
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
