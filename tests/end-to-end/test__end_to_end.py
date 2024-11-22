"""
End-to-end tests for the package.
"""

import pathlib
import re

import pytest

import database_exporter
from database_exporter.exporter import DatabaseConnection

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_query__sql() -> str:
    return (FIXTURES / "simple_query.sql").read_text().strip()


@pytest.fixture
def simple_query__csv() -> str:
    return (FIXTURES / "simple_query.csv").read_text().strip()


@pytest.fixture
def complex_query__sql() -> str:
    return (FIXTURES / "complex_query.sql").read_text().strip()


@pytest.fixture
def complex_query__csv() -> str:
    return (FIXTURES / "complex_query.csv").read_text().strip()


def test__sqlite_simple_result_sets_can_be_exported_to_csv(
    sqlite_connection: DatabaseConnection,
    simple_query__sql: str,
    simple_query__csv: str,
    tmp_path: pathlib.Path,
) -> None:
    """
    The result set from a SQLite query can be exported to a CSV.
    """
    actual_path = tmp_path / "actual.csv"
    database_exporter.query_to_csv(
        conn=sqlite_connection,
        query=simple_query__sql,
        filepath=actual_path,
    )
    actual = actual_path.read_text().strip()

    # The sqlite3 driver returns ints instead of bools
    # fmt: off
    simple_query_csv = (simple_query__csv
        .replace("true", "1")
        .replace("false", "0")
    )
    # fmt: on

    # In CI, the drivers print extra line breaks to the CSV for some reason :shrug:
    actual = re.sub(r"\n+", "\n", actual)

    assert actual == simple_query_csv


@pytest.mark.parametrize(
    "query, csv",
    [
        ("simple_query__sql", "simple_query__csv"),
        ("complex_query__sql", "complex_query__csv"),
    ],
)
def test__duckdb_result_sets_can_be_exported_to_csv(
    duckdb_connection: DatabaseConnection,
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
    query: str,
    csv: str,
) -> None:
    """
    The result set from a DuckDB query can be exported to a CSV.
    """
    actual_path = tmp_path / "actual.csv"
    database_exporter.query_to_csv(
        conn=duckdb_connection,
        query=request.getfixturevalue(query),
        filepath=actual_path,
    )
    actual = actual_path.read_text().strip()

    # In CI, the drivers print extra line breaks to the CSV for some reason :shrug:
    actual = re.sub(r"\n+", "\n", actual)

    assert actual == request.getfixturevalue(csv)
