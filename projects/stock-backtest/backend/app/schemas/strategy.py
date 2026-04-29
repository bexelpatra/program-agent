"""전략 API Pydantic 스키마.

GET /api/strategies 가 allocator/filter 목록 + 각 전략의 파라미터 JSON Schema 를
노출한다. 프런트는 이 JSON Schema 를 받아 폼을 자동 생성한다 (UI/UX 원칙 1: JSON
직접 노출 금지 — 사용자에게는 폼만 보임).
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class StrategyDescriptor(BaseModel):
    """단일 전략(allocator 또는 filter) 메타데이터 + JSON Schema."""

    model_config = ConfigDict(frozen=True)

    name: str
    type: Literal["allocator", "filter"]
    params_schema: dict[str, Any]
    description: str | None = None


class StrategyListResponse(BaseModel):
    """GET /api/strategies 응답.

    allocators / filters 를 분리해 노출 — 프런트가 전략 빌더 UI 에서
    "비중 결정 규칙" 과 "보유 자격 필터" 두 영역을 나눠 폼을 그리는 데 사용한다.
    """

    model_config = ConfigDict(frozen=True)

    allocators: list[StrategyDescriptor]
    filters: list[StrategyDescriptor]
