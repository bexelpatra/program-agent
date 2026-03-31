"""CLI 엔트리포인트 — click 기반 ethics-guide 커맨드."""

import os
import sys

import click

from src.es_client import get_client, close_client
from src.models import init_all_indices
from src.loader import load_yaml_file, load_thinker_to_es, load_fields_to_es, load_all
from src.search import (
    get_relations,
    get_thinker_full,
    get_unverified_claims,
    search_by_field,
    search_by_keyword,
    search_thinker_by_name,
)
from src.exporter import export_thinker, export_all_thinkers


@click.group()
def cli():
    """윤리 임용시험 학습 가이드 CLI"""
    pass


# ── init ─────────────────────────────────────────────────────


@cli.command()
def init():
    """ES 인덱스를 초기화한다."""
    client = get_client()
    try:
        init_all_indices(client)
        click.echo("모든 인덱스가 초기화되었습니다.")
    finally:
        close_client(client)


# ── load ─────────────────────────────────────────────────────


@cli.command()
@click.argument("yaml_path")
def load(yaml_path):
    """단일 YAML 파일을 ES에 로딩한다."""
    if not os.path.exists(yaml_path):
        click.echo(f"파일을 찾을 수 없습니다: {yaml_path}", err=True)
        sys.exit(1)

    client = get_client()
    try:
        data = load_yaml_file(yaml_path)

        # fields.yaml인 경우
        if "fields" in data:
            count = load_fields_to_es(client, yaml_path)
            click.echo(f"분야 {count}개 적재 완료")
        else:
            counts = load_thinker_to_es(client, data)
            click.echo("적재 완료:")
            for key, val in counts.items():
                if val > 0:
                    click.echo(f"  {key}: {val}")
    finally:
        close_client(client)


# ── load-all ─────────────────────────────────────────────────


@cli.command("load-all")
@click.option("--data-dir", default="data", help="데이터 디렉토리 경로")
def load_all_cmd(data_dir):
    """data/ 디렉토리의 모든 YAML을 ES에 로딩한다."""
    if not os.path.isdir(data_dir):
        click.echo(f"디렉토리를 찾을 수 없습니다: {data_dir}", err=True)
        sys.exit(1)

    client = get_client()
    try:
        totals = load_all(client, data_dir)
        click.echo("전체 적재 완료:")
        for key, val in totals.items():
            click.echo(f"  {key}: {val}")
    finally:
        close_client(client)


# ── study ────────────────────────────────────────────────────


@cli.command()
@click.argument("name")
def study(name):
    """사상가 종합 조회 (보기 좋게 포맷팅)."""
    client = get_client()
    try:
        # 이름으로 사상가 검색
        thinkers = search_thinker_by_name(client, name)
        if not thinkers:
            click.echo(f"'{name}'에 해당하는 사상가를 찾을 수 없습니다.")
            return

        thinker = thinkers[0]
        thinker_id = thinker["id"]

        # 종합 정보 조회
        full = get_thinker_full(client, thinker_id)
        _print_study(full)
    finally:
        close_client(client)


def _print_study(full: dict):
    """사상가 종합 정보를 보기 좋게 출력한다."""
    t = full["thinker"]
    if not t:
        click.echo("사상가 정보를 찾을 수 없습니다.")
        return

    name = t.get("name", "")
    birth = t.get("birth_year", "?")
    death = t.get("death_year", "?")
    field = t.get("field", "")
    era = t.get("era", "")

    click.echo(f"\n=== {name} ({birth}-{death}) ===")
    click.echo(f"분야: {field} ({era})")

    if t.get("background"):
        click.echo(f"\n[배경] {t['background']}")
    if t.get("philosophical_journey"):
        click.echo(f"\n[사상 형성 과정] {t['philosophical_journey']}")
    if t.get("core_philosophy"):
        click.echo(f"\n[핵심 사상] {t['core_philosophy']}")

    # 주요 저서
    works = full.get("works", [])
    if works:
        click.echo("\n주요 저서")
        for i, w in enumerate(works, 1):
            title = w.get("title", "")
            year = w.get("year", "")
            click.echo(f"  {i}. {title} ({year})")
            if w.get("significance"):
                click.echo(f"     의의: {w['significance']}")

    # 핵심 주장
    claims = full.get("claims", [])
    if claims:
        click.echo("\n핵심 주장")
        for c in claims:
            kws = ", ".join(c.get("keywords", []))
            label = f"[{kws}]" if kws else ""
            click.echo(f"  {label} {c.get('claim', '')}")
            if c.get("work_id") or c.get("source_detail"):
                source_parts = []
                if c.get("work_id"):
                    source_parts.append(c["work_id"])
                if c.get("source_detail"):
                    source_parts.append(c["source_detail"])
                click.echo(f"    출처: {', '.join(source_parts)}")
            if c.get("original_text"):
                click.echo(f"    원문: {c['original_text']}")
            if c.get("argument"):
                click.echo(f"    논증: {c['argument']}")
            if c.get("counterpoint"):
                click.echo(f"    반론: {c['counterpoint']}")

    # 사상적 관계
    relations = full.get("relations", [])
    if relations:
        click.echo("\n사상적 관계")
        for r in relations:
            from_t = r.get("from_thinker", "")
            to_t = r.get("to_thinker", "")
            rel_type = r.get("type", "")
            desc = r.get("description", "")
            thinker_id = full["thinker"]["id"]
            if from_t == thinker_id:
                click.echo(f"  -> {to_t} ({rel_type}): {desc}")
            else:
                click.echo(f"  <- {from_t} ({rel_type}): {desc}")

    # 핵심 키워드
    keywords = full.get("keywords", [])
    if keywords:
        click.echo("\n핵심 키워드")
        for kw in keywords:
            term = kw.get("term", "")
            definition = kw.get("definition", "")
            click.echo(f"  - {term}: {definition}")

    click.echo()


# ── search ───────────────────────────────────────────────────


@cli.command()
@click.argument("keyword", required=False)
@click.option("--field", "field_id", default=None, help="분야별 조회")
def search(keyword, field_id):
    """키워드 또는 분야로 검색한다."""
    client = get_client()
    try:
        if field_id:
            thinkers = search_by_field(client, field_id)
            if not thinkers:
                click.echo(f"'{field_id}' 분야의 사상가가 없습니다.")
                return
            click.echo(f"\n[{field_id}] 분야 사상가:")
            for t in thinkers:
                click.echo(f"  - {t.get('name', '')} ({t.get('era', '')})")
            click.echo()
            return

        if not keyword:
            click.echo("검색어 또는 --field 옵션을 입력하세요.", err=True)
            sys.exit(1)

        results = search_by_keyword(client, keyword)

        if results["thinkers"]:
            click.echo(f"\n관련 사상가:")
            for t in results["thinkers"]:
                click.echo(f"  - {t.get('name', '')} ({t.get('era', '')})")

        if results["claims"]:
            click.echo(f"\n관련 주장:")
            for c in results["claims"]:
                tid = c.get("thinker_id", "")
                claim = c.get("claim", "")
                click.echo(f"  [{tid}] {claim[:80]}")

        if results["keywords"]:
            click.echo(f"\n관련 키워드:")
            for kw in results["keywords"]:
                click.echo(f"  - {kw.get('term', '')}: {kw.get('definition', '')[:60]}")

        if not any(results.values()):
            click.echo(f"'{keyword}'에 대한 검색 결과가 없습니다.")

        click.echo()
    finally:
        close_client(client)


# ── relations ────────────────────────────────────────────────


@cli.command()
@click.argument("name")
def relations(name):
    """사상가의 영향 관계를 조회한다."""
    client = get_client()
    try:
        thinkers = search_thinker_by_name(client, name)
        if not thinkers:
            click.echo(f"'{name}'에 해당하는 사상가를 찾을 수 없습니다.")
            return

        thinker = thinkers[0]
        thinker_id = thinker["id"]
        thinker_name = thinker.get("name", thinker_id)

        rels = get_relations(client, thinker_id)

        click.echo(f"\n=== {thinker_name}의 사상적 관계 ===")

        if rels["incoming"]:
            click.echo("\n영향 받은 관계 (incoming):")
            for r in rels["incoming"]:
                click.echo(
                    f"  <- {r.get('from_thinker', '')} ({r.get('type', '')}): "
                    f"{r.get('description', '')}"
                )

        if rels["outgoing"]:
            click.echo("\n영향 준 관계 (outgoing):")
            for r in rels["outgoing"]:
                click.echo(
                    f"  -> {r.get('to_thinker', '')} ({r.get('type', '')}): "
                    f"{r.get('description', '')}"
                )

        if not rels["incoming"] and not rels["outgoing"]:
            click.echo("등록된 관계가 없습니다.")

        click.echo()
    finally:
        close_client(client)


# ── verify-status ────────────────────────────────────────────


@cli.command("verify-status")
def verify_status():
    """미검증 데이터 목록을 출력한다."""
    client = get_client()
    try:
        claims = get_unverified_claims(client)
        if not claims:
            click.echo("모든 주장이 검증되었습니다.")
            return

        click.echo(f"\n미검증 주장: {len(claims)}건\n")
        for c in claims:
            tid = c.get("thinker_id", "")
            cid = c.get("id", "")
            claim_text = c.get("claim", "")
            click.echo(f"  [{tid}] {cid}")
            click.echo(f"    {claim_text[:100]}")
            click.echo()
    finally:
        close_client(client)


# ── export ───────────────────────────────────────────────────


@cli.command()
@click.argument("thinker_id")
@click.option("--data-dir", default="data", help="출력 데이터 디렉토리 경로")
def export(thinker_id, data_dir):
    """특정 사상가의 데이터를 ES에서 YAML로 export한다."""
    client = get_client()
    try:
        path = export_thinker(client, thinker_id, data_dir)
        if path is None:
            click.echo(f"'{thinker_id}'에 해당하는 사상가를 찾을 수 없습니다.", err=True)
            sys.exit(1)
        click.echo(f"export 완료: {path}")
    finally:
        close_client(client)


# ── export-all ────────────────────────────────────────────────


@cli.command("export-all")
@click.option("--data-dir", default="data", help="출력 데이터 디렉토리 경로")
def export_all_cmd(data_dir):
    """ES에 등록된 모든 사상가를 YAML로 export한다."""
    client = get_client()
    try:
        results = export_all_thinkers(client, data_dir)
        if not results:
            click.echo("export할 사상가가 없습니다.")
            return
        click.echo(f"export 완료: {len(results)}명")
        for thinker_id, path in sorted(results.items()):
            click.echo(f"  {thinker_id}: {path}")
    finally:
        close_client(client)


if __name__ == "__main__":
    cli()
