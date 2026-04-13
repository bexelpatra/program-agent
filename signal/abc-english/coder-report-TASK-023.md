# Coder Report: TASK-023

## Status: DONE

## 작업 내용
- `projects/abc-english/src/cli.py` 신규 작성
- Click 라이브러리 기반 CLI 구현 (9개 명령어)

## 구현된 명령어
1. `collect` - collector.collect_all 호출, 수집 결과 요약 출력
2. `transcribe` - data/transcripts/*_official.json 스캔 → transcriber.transcribe_all 호출
3. `compare` - official + whisper 양쪽 있는 episode_id 추출 → comparator.compare_all 호출
4. `analyze` - official transcript의 episode_id 추출 → analyzer.analyze_all 호출
5. `llm-analyze` - detect_expressions_for_episode + classify_vocabulary_for_episode 호출
6. `load` - 전체 데이터 수집/분석 후 loader.load_all 호출
7. `run-all` - collect → transcribe → compare → analyze → llm-analyze → load 순차 실행
8. `init-indices` - models.create_indices 호출
9. `delete-indices` - models.delete_indices 호출 (click.confirm 확인 프롬프트 포함)

## 공통 사항
- `--config` 옵션 (기본값: config/settings.yaml)
- logging.basicConfig INFO 레벨 설정
- `@click.group()` + `@cli.command()` 패턴
- `if __name__ == "__main__": cli()` 포함

## 검증
- `python -m src.cli --help` 정상 동작 확인
- 9개 명령어 모두 표시됨

## 생성/수정 파일
- `projects/abc-english/src/cli.py` (신규)
