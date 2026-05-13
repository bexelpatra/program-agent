/**
 * Zod 스키마 round-trip 테스트 (TASK-306).
 *
 * 백엔드 `app/schemas/theme.py` 의 직렬화 출력 (FastAPI Pydantic JSON) 을
 * 프런트 Zod 스키마가 손실 없이 받아내는지 검증. STOCK enum 회귀 점검 포함.
 */
import { describe, expect, it } from "vitest";

import {
  AssetTypeEnum,
  SeriesPointSchema,
  ThemeChartResponseSchema,
  ThemeCreateSchema,
  ThemeReadSchema,
} from "../schemas";

describe("AssetTypeEnum — STOCK enum (TASK-300 회귀)", () => {
  it("STOCK 을 허용한다", () => {
    expect(AssetTypeEnum.parse("STOCK")).toBe("STOCK");
  });

  it("기존 5종 (EQUITY_INDEX/ETF/BOND/COMMODITY/CRYPTO) 도 유지된다", () => {
    for (const t of ["EQUITY_INDEX", "ETF", "BOND", "COMMODITY", "CRYPTO"]) {
      expect(AssetTypeEnum.parse(t)).toBe(t);
    }
  });
});

describe("ThemeRead — round-trip", () => {
  it("정상 JSON 을 parse 한 결과는 원본과 동등하다", () => {
    const wire = {
      theme_id: 7,
      name: "정치 테마 A",
      slug: "political-a",
      description: "2024 대선 관련",
      user_id: "local",
      created_at: "2025-11-01T09:00:00",
      member_count: 5,
    };
    const parsed = ThemeReadSchema.parse(wire);
    expect(parsed).toEqual(wire);
  });

  it("description / member_count 가 null 이어도 통과한다", () => {
    const wire = {
      theme_id: 1,
      name: "X",
      slug: "x",
      description: null,
      user_id: "local",
      created_at: "2025-11-01T09:00:00",
      member_count: null,
    };
    const parsed = ThemeReadSchema.parse(wire);
    expect(parsed.theme_id).toBe(1);
    expect(parsed.description).toBeNull();
  });
});

describe("ThemeCreate — 필수 필드 검증", () => {
  it("name 누락 시 ZodError 를 throw 한다", () => {
    expect(() =>
      ThemeCreateSchema.parse({
        // name 의도적 누락
        slug: "x",
        user_id: "local",
      }),
    ).toThrow();
  });

  it("name 만 있어도 통과한다 (slug/description/user_id 는 옵션)", () => {
    const parsed = ThemeCreateSchema.parse({ name: "정치 테마" });
    expect(parsed.name).toBe("정치 테마");
  });
});

describe("ThemeChartResponse — round-trip (Decimal string + dict key 문자열화)", () => {
  it("members/aggregate/universe_meta 가 정상 parse 되고 시리즈 길이가 일치한다", () => {
    // 백엔드 직렬화 가정:
    //   - dict[int, ...] → JSON object 의 key 는 string ("101")
    //   - Decimal → string ("100.000000") 또는 number — 둘 다 수용
    const wire = {
      members: {
        "101": [
          { time: "2024-01-02T00:00:00", value: "100.000000" },
          { time: "2024-01-03T00:00:00", value: "101.500000" },
          { time: "2024-01-04T00:00:00", value: 99.75 },
        ],
        "102": [
          { time: "2024-01-02T00:00:00", value: "100.000000" },
          { time: "2024-01-03T00:00:00", value: "98.250000" },
        ],
      },
      aggregate: [
        { time: "2024-01-02T00:00:00", value: "100.000000" },
        { time: "2024-01-03T00:00:00", value: "99.875000" },
      ],
      universe_meta: {
        adjusted_start: "2024-01-02",
        adjusted_end: "2024-01-04",
        affected_assets: [103],
        reason: "universe_start_later",
        message:
          "asset_id=103 의 데이터 시작이 늦어 공통 기간이 2024-01-02 로 조정되었습니다.",
      },
    };

    const parsed = ThemeChartResponseSchema.parse(wire);

    // members: string key 유지 + 시리즈 길이 일치
    expect(Object.keys(parsed.members).sort()).toEqual(["101", "102"]);
    expect(parsed.members["101"]).toHaveLength(3);
    expect(parsed.members["102"]).toHaveLength(2);

    // value 는 Decimal string → number 로 coerce 됨
    expect(parsed.members["101"][0].value).toBe(100);
    expect(parsed.members["101"][1].value).toBeCloseTo(101.5, 6);
    expect(parsed.members["101"][2].value).toBe(99.75);

    // aggregate
    expect(parsed.aggregate).toHaveLength(2);
    expect(parsed.aggregate[0].value).toBe(100);

    // universe_meta
    expect(parsed.universe_meta.adjusted_start).toBe("2024-01-02");
    expect(parsed.universe_meta.affected_assets).toEqual([103]);
    expect(parsed.universe_meta.reason).toBe("universe_start_later");
  });

  it("SeriesPoint.value 가 number 로 직접 와도 parse 된다", () => {
    const parsed = SeriesPointSchema.parse({
      time: "2024-01-02T00:00:00",
      value: 100.5,
    });
    expect(parsed.value).toBe(100.5);
  });
});
