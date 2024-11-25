"""
End-to-end tests for the package.
"""

import pathlib
import re
from collections.abc import Callable

import pytest

import database_exporter
from database_exporter.exporter import DatabaseConnection

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def _read_fixture(filename: str) -> str:
    return (FIXTURES / filename).read_text().strip()


class QueryFixture:
    sql: str
    csv: str
    jsonl: str

    def __init__(self, name: str):
        self.sql = _read_fixture(f"{name}.sql")
        self.csv = _read_fixture(f"{name}.csv")
        self.jsonl = _read_fixture(f"{name}.jsonl")


@pytest.fixture
def simple_query() -> QueryFixture:
    return QueryFixture("simple_query")


@pytest.fixture
def complex_query() -> QueryFixture:
    return QueryFixture("complex_query")


@pytest.mark.parametrize(
    "query_fixture, result_type, exporter",
    [
        (
            "simple_query",
            "csv",
            database_exporter.query_to_csv,
        ),
        (
            "simple_query",
            "jsonl",
            database_exporter.query_to_jsonl,
        ),
    ],
)
def test__sqlite_result_sets_can_be_exported_to_a_file(
    sqlite_connection: DatabaseConnection,
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
    query_fixture: str,
    result_type: str,
    exporter: Callable,
) -> None:
    """
    The result set from a SQLite query can be exported to a file.
    """
    query: QueryFixture = request.getfixturevalue(query_fixture)
    result = getattr(query, result_type)

    actual_path = tmp_path / "actual.file"
    exporter(
        conn=sqlite_connection,
        query=query.sql,
        filepath=actual_path,
    )

    assert actual_path.exists()
    actual = actual_path.read_text().strip()

    # The sqlite3 driver returns ints instead of bools
    # fmt: off
    result = (
        result
            .replace("true", "1")
            .replace("false", "0")
    )
    # fmt: on

    # In CI, the drivers print extra line breaks to the CSV for some reason :shrug:
    actual = re.sub(r"\n+", "\n", actual)

    assert actual == result


@pytest.mark.parametrize(
    "query_fixture, result_type, exporter",
    [
        (
            "simple_query",
            "csv",
            database_exporter.query_to_csv,
        ),
        (
            "complex_query",
            "csv",
            database_exporter.query_to_csv,
        ),
        (
            "simple_query",
            "jsonl",
            database_exporter.query_to_jsonl,
        ),
        (
            "complex_query",
            "jsonl",
            database_exporter.query_to_jsonl,
        ),
    ],
)
def test__duckdb_result_sets_can_be_exported_to_a_file(
    duckdb_connection: DatabaseConnection,
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
    query_fixture: str,
    result_type: str,
    exporter: Callable,
) -> None:
    """
    The result set from a DuckDB query can be exported to a file.
    """
    query: QueryFixture = request.getfixturevalue(query_fixture)
    actual_path = tmp_path / "actual.file"
    exporter(
        conn=duckdb_connection,
        query=query.sql,
        filepath=actual_path,
    )

    assert actual_path.exists()
    actual = actual_path.read_text().strip()

    # In CI, the drivers print extra line breaks to the CSV for some reason :shrug:
    actual = re.sub(r"\n+", "\n", actual)

    assert actual == getattr(query, result_type)
