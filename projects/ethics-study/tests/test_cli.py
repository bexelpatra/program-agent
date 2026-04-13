"""test_cli.py -- cli.py 단위 테스트 (CliRunner + mock)."""

from unittest.mock import MagicMock, patch, ANY

import pytest
from click.testing import CliRunner

from src.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_es():
    """get_client와 close_client를 모킹한다."""
    with patch("src.cli.get_client") as mock_get, patch(
        "src.cli.close_client"
    ) as mock_close:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client, mock_get, mock_close


class TestInitCommand:
    """init 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.init_all_indices")
    def test_init_success(self, mock_init, mock_get, mock_close, runner):
        """init 커맨드가 정상 실행되어야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client

        result = runner.invoke(cli, ["init"])

        assert result.exit_code == 0
        assert "초기화" in result.output
        mock_init.assert_called_once_with(mock_client)
        mock_close.assert_called_once_with(mock_client)


class TestLoadCommand:
    """load 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.load_thinker_to_es")
    @patch("src.cli.load_yaml_file")
    def test_load_thinker_yaml(
        self, mock_load_yaml, mock_load_thinker, mock_get, mock_close, runner, tmp_path
    ):
        """사상가 YAML을 로딩해야 한다."""
        yaml_file = tmp_path / "kant.yaml"
        yaml_file.write_text("thinker:\n  id: kant\n")

        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_load_yaml.return_value = {"thinker": {"id": "kant"}}
        mock_load_thinker.return_value = {
            "thinkers": 1,
            "works": 0,
            "claims": 0,
            "keywords": 0,
            "relations": 0,
        }

        result = runner.invoke(cli, ["load", str(yaml_file)])

        assert result.exit_code == 0
        assert "적재 완료" in result.output

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.load_fields_to_es")
    @patch("src.cli.load_yaml_file")
    def test_load_fields_yaml(
        self, mock_load_yaml, mock_load_fields, mock_get, mock_close, runner, tmp_path
    ):
        """fields YAML을 로딩해야 한다."""
        yaml_file = tmp_path / "fields.yaml"
        yaml_file.write_text("fields:\n  - id: western\n")

        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_load_yaml.return_value = {"fields": [{"id": "western"}]}
        mock_load_fields.return_value = 1

        result = runner.invoke(cli, ["load", str(yaml_file)])

        assert result.exit_code == 0
        assert "분야" in result.output

    def test_load_nonexistent_file(self, runner):
        """존재하지 않는 파일은 에러를 출력해야 한다."""
        result = runner.invoke(cli, ["load", "/nonexistent/file.yaml"])

        assert result.exit_code != 0
        assert "찾을 수 없습니다" in result.output


class TestLoadAllCommand:
    """load-all 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.load_all")
    def test_load_all_success(
        self, mock_load_all, mock_get, mock_close, runner, tmp_path
    ):
        """전체 로딩이 정상 동작해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_load_all.return_value = {
            "fields": 3,
            "thinkers": 2,
            "works": 5,
            "claims": 10,
            "keywords": 8,
            "relations": 3,
        }

        result = runner.invoke(cli, ["load-all", "--data-dir", str(tmp_path)])

        assert result.exit_code == 0
        assert "전체 적재 완료" in result.output

    def test_load_all_nonexistent_dir(self, runner):
        """존재하지 않는 디렉토리는 에러를 출력해야 한다."""
        result = runner.invoke(cli, ["load-all", "--data-dir", "/nonexistent/dir"])

        assert result.exit_code != 0
        assert "찾을 수 없습니다" in result.output


class TestStudyCommand:
    """study 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.get_thinker_full")
    @patch("src.cli.search_thinker_by_name")
    def test_study_found(self, mock_search, mock_full, mock_get, mock_close, runner):
        """사상가를 찾으면 종합 정보를 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search.return_value = [{"id": "kant", "name": "칸트"}]
        mock_full.return_value = {
            "thinker": {
                "id": "kant",
                "name": "칸트",
                "birth_year": 1724,
                "death_year": 1804,
                "field": "western",
                "era": "근대",
            },
            "works": [],
            "claims": [],
            "keywords": [],
            "relations": [],
        }

        result = runner.invoke(cli, ["study", "칸트"])

        assert result.exit_code == 0
        assert "칸트" in result.output
        assert "1724" in result.output

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.search_thinker_by_name")
    def test_study_not_found(self, mock_search, mock_get, mock_close, runner):
        """사상가를 찾지 못하면 안내 메시지를 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search.return_value = []

        result = runner.invoke(cli, ["study", "없는사람"])

        assert result.exit_code == 0
        assert "찾을 수 없습니다" in result.output


class TestSearchCommand:
    """search 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.search_by_keyword")
    def test_search_keyword(self, mock_search_kw, mock_get, mock_close, runner):
        """키워드 검색이 정상 동작해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search_kw.return_value = {
            "thinkers": [{"name": "칸트", "era": "근대"}],
            "claims": [],
            "keywords": [],
        }

        result = runner.invoke(cli, ["search", "의무"])

        assert result.exit_code == 0
        assert "칸트" in result.output

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.search_by_field")
    def test_search_by_field(self, mock_search_field, mock_get, mock_close, runner):
        """분야별 검색이 정상 동작해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search_field.return_value = [
            {"name": "칸트", "era": "근대"},
        ]

        result = runner.invoke(cli, ["search", "--field", "western"])

        assert result.exit_code == 0
        assert "칸트" in result.output

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.search_by_keyword")
    def test_search_no_results(self, mock_search_kw, mock_get, mock_close, runner):
        """검색 결과가 없으면 안내 메시지를 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search_kw.return_value = {"thinkers": [], "claims": [], "keywords": []}

        result = runner.invoke(cli, ["search", "없는키워드"])

        assert result.exit_code == 0
        assert "검색 결과가 없습니다" in result.output


class TestRelationsCommand:
    """relations 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.get_relations")
    @patch("src.cli.search_thinker_by_name")
    def test_relations_found(
        self, mock_search, mock_rels, mock_get, mock_close, runner
    ):
        """관계가 있으면 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search.return_value = [{"id": "kant", "name": "칸트"}]
        mock_rels.return_value = {
            "outgoing": [
                {"to_thinker": "hegel", "type": "influenced", "description": "영향"}
            ],
            "incoming": [],
        }

        result = runner.invoke(cli, ["relations", "칸트"])

        assert result.exit_code == 0
        assert "칸트" in result.output
        assert "hegel" in result.output

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.search_thinker_by_name")
    def test_relations_not_found(self, mock_search, mock_get, mock_close, runner):
        """사상가를 찾지 못하면 안내 메시지를 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_search.return_value = []

        result = runner.invoke(cli, ["relations", "없는사람"])

        assert result.exit_code == 0
        assert "찾을 수 없습니다" in result.output


class TestVerifyStatusCommand:
    """verify-status 커맨드 테스트."""

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.get_unverified_claims")
    def test_has_unverified(self, mock_unverified, mock_get, mock_close, runner):
        """미검증 주장이 있으면 목록을 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_unverified.return_value = [
            {"id": "c1", "thinker_id": "kant", "claim": "도덕법칙은 보편적이다"},
        ]

        result = runner.invoke(cli, ["verify-status"])

        assert result.exit_code == 0
        assert "미검증" in result.output
        assert "1건" in result.output

    @patch("src.cli.close_client")
    @patch("src.cli.get_client")
    @patch("src.cli.get_unverified_claims")
    def test_all_verified(self, mock_unverified, mock_get, mock_close, runner):
        """모든 주장이 검증되면 완료 메시지를 출력해야 한다."""
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        mock_unverified.return_value = []

        result = runner.invoke(cli, ["verify-status"])

        assert result.exit_code == 0
        assert "모든 주장이 검증" in result.output
